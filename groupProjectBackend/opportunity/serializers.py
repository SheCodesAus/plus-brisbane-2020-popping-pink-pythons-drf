from rest_framework import serializers
from .models import Opportunity

class OpportunitySerializer(serializers.Serializer):
    id=serializers.ReadOnlyField()
    title=serializers.CharField(max_length = 200)
    location = serializers.CharField(max_length = 200)
    organization = serializers.CharField(max_length = 200, required=False)
    description = serializers.CharField(max_length = 200, required=False)
    objectives = serializers.CharField(max_length = 200, required=False)
    image = serializers.URLField(required=False)
    duration = serializers.SerializerMethodField()
    start_date = serializers.DateTimeField()
    close_date = serializers.DateTimeField()
    amount = serializers.IntegerField(required=False)
    opp_type = serializers.CharField(max_length = 200)
    opp_link = serializers.URLField(required=False)
    owner = serializers.ReadOnlyField(source="owner.id")
    date_created = serializers.DateTimeField(read_only=True)
    date_updated = serializers.DateTimeField(read_only=True)

    def get_duration(self, obj):
        duration = (obj.close_date - obj.start_date).days
        return duration
    