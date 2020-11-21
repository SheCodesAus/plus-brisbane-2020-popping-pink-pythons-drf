from django.conf import settings
from django.db import models

class Opportunity(models.Model):
    title = models.CharField(max_length=200)
    location = models.TextField()
    organisation = models.TextField()
    description = models.TextField()
    objectives = models.TextField()
    image = models.URLField(null=True)
    duration = models.IntegerField()
    start_date = models.DateTimeField()
    close_date = models.DateTimeField()
    amount = models.IntegerField()
    opp_type = models.TextField()
    opp_link = models.URLField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owner_opportunity'
    )
    