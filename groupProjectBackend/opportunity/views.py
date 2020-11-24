from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Opportunity 
from .serializers import OpportunitySerializer, OpportunityDetailSerializer
from django.http import Http404
from rest_framework import status, permissions
from .permissions import IsOwnerOrReadOnly


class OpportunityList(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        # IsOwnerOrReadOnly
    ]

    def get(self, request):
        opportunities = Opportunity.objects.all()
        serializer = OpportunitySerializer(opportunities, many=True)
        return Response(serializer.data)

    
    def post(self, request):
        serializer = OpportunitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class OpportunityDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        # IsOwnerOrReadOnly
    ]

    def get_object(self, pk):
        try:
            opportunity = Opportunity.objects.get(pk=pk)
            self.check_object_permissions(self.request, opportunity)
            return opportunity
        except Opportunity.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        opportunity = self.get_object(pk)
        serializer = OpportunityDetailSerializer(opportunity)
        return Response(serializer.data)

    def put(self, request, pk):
        opportunity = self.get_object(pk)
        data = request.data
        serializer = OpportunityDetailSerializer(
            instance = opportunity,
            data = data, 
            partial = True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        opportunity = self.get_object(pk)
        opportunity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        


class OpportunityLatest(APIView):
    # Return 5 ?
    def get(self, request):
        latest = Opportunity.objects.all().order_by('-date_updated')[:5]
        serializer = OpportunityDetailSerializer(latest, many=True)
        return Response(serializer.data)

