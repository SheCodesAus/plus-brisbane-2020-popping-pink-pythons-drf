from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserDetailSerializer
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
        serializer = OpportunitySerializer(data = request.data)
        if serializer.is_valid():
            with transaction.atomic():
                opportunity = Opportunity.objects.get(pk=validated_data.get('pk'))
                user.favourites.add(opportunity)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )