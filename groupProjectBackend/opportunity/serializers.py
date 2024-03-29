from rest_framework import serializers
from .models import Opportunity
from django.utils import timezone

class OpportunitySerializer(serializers.Serializer):
    id=serializers.ReadOnlyField()
    title=serializers.CharField(max_length = 200)
    location = serializers.CharField(max_length = 200)
    organisation = serializers.CharField(max_length = 200)
    description = serializers.CharField(max_length=None)
    objectives = serializers.CharField(max_length=None)
    image = serializers.URLField(allow_blank=True)
    duration = serializers.SerializerMethodField()
    start_date = serializers.DateField()
    close_date = serializers.DateField()
    amount = serializers.IntegerField()
    opp_type = serializers.CharField(max_length = 200)
    opp_link = serializers.URLField(allow_blank=True)
    owner = serializers.ReadOnlyField(source="owner.id")
    date_created = serializers.DateTimeField(read_only=True)
    date_updated = serializers.DateTimeField(read_only=True)

    def get_duration(self, obj):
        duration = (obj.close_date - obj.start_date).days
        return duration
    
    def create(self, validated_data):
        return Opportunity.objects.create(**validated_data)
    

class OpportunityDetailSerializer(OpportunitySerializer):
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.location = validated_data.get('location', instance.location)
        instance.organisation = validated_data.get('organization', instance.organisation)
        instance.description = validated_data.get('description', instance.description)
        instance.objectives = validated_data.get('objectives', instance.objectives)
        instance.image = validated_data.get('image', instance.image)
        instance.start_date = validated_data.get('start_date',instance.start_date)
        instance.close_date = validated_data.get('close_date',instance.close_date) 
        instance.amount = validated_data.get('amount', instance.amount)
        instance.opp_type = validated_data.get('opp_type', instance.opp_type)
        instance.opp_link = validated_data.get('opp_link', instance.opp_link)
        instance.save()
        return instance


class FaveOpportunitySerializer(serializers.Serializer):
    id=serializers.IntegerField()
        