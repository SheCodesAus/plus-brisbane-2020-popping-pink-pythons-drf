from django.contrib.auth import get_user_model
from django.db import models

class Opportunity(models.Model):
    title = models.CharField(max_lenght=200)
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
    owner = owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owner_opportunity'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    


