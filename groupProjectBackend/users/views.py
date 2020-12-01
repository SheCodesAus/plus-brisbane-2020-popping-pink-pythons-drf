from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserDetailSerializer
from opportunity.serializers import FaveOpportunitySerializer
from django.db import transaction
from opportunity.models import Opportunity
from .permissions import IsUserOrReadOnly

class CustomUserList(APIView):

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class CustomUserDetail(APIView):
    permission_classes = [IsUserOrReadOnly
    ]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
        
    def put(self, request, pk):
        user = self.get_object(pk)
        data = request.data
        serializer = CustomUserDetailSerializer(
            instance=user,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        try:
            user_to_delete = self.get_object(pk)    
            user_to_delete.delete()    
            return Response(status=status.HTTP_204_NO_CONTENT)    
        except Http404:   
            return Http404
    

class CurrentUserView(APIView):
    def get(self, request):
        serializer = CustomUserDetailSerializer(request.user)
        if request.user.is_authenticated:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            status = status.HTTP_401_UNAUTHORIZED
        )


class UserFavouriteView(APIView):
    permission_classes = [IsUserOrReadOnly
    ]

    # def get_queryset():
    #     user = request.user
    #     queryset = user.favourites.all()

    # def get(self, request, pk):
    #     user = self.get_object(pk)
    #     serializer = CustomUserDetailSerializer(user)
    #     return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = FaveOpportunitySerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                print('pk', serializer.validated_data)
                opportunity = Opportunity.objects.get(pk=serializer.validated_data.get('id'))
                user.favourites.add(opportunity)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )

