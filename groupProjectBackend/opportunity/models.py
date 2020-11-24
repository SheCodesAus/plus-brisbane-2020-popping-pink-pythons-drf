from django.conf import settings
from django.db import models

class Opportunity(models.Model):
    title = models.CharField(max_length=200)
    location = models.TextField()
    organisation = models.TextField()
    description = models.TextField()
    objectives = models.TextField()
    image = models.URLField(null=True)
    start_date = models.DateField()
    close_date = models.DateField()
    amount = models.IntegerField()
    opp_type = models.TextField()
    opp_link = models.URLField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # allow for owner to delete themselves - not to be deleted. 
        related_name='owner_opportunity'
    )
    