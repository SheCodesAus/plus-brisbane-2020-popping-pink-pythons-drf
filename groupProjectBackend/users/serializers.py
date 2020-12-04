from rest_framework import serializers 
from .models import CustomUser
from opportunity.models import Opportunity
from django.utils import timezone
from opportunity.serializers import OpportunitySerializer

class CustomUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(max_length=200)
    bio = serializers.CharField(max_length=None, default="")
    image = serializers.URLField(default="https://robohash.org/YOUR-TEXT.png")
    opportunity_owner = serializers.BooleanField(default=False)
    date_created = serializers.DateTimeField(default = timezone.now)
    num_fav = serializers.SerializerMethodField()
    
    favourites = OpportunitySerializer(many=True, read_only=True)
   
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def get_num_fav(self, obj):
        favs = obj.favourites.all()
        fav_list = len(favs) 
        return fav_list

class CustomUserDetailSerializer(CustomUserSerializer):

    favourites = OpportunitySerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.image = validated_data.get('image', instance.image)
        instance.opportunity_owner = validated_data.get('opportunity_owner', instance.opportunity_owner)
        # instance.country = validated_data.get('country', instance.country)
        # instance.project_owner = validated_data.get('is_open', instance.project_owner)
        instance.save()
        return instance