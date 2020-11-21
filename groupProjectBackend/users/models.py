from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from opportunity.models import Opportunity

class CustomUser(AbstractUser):
    name = models.CharField(max_length=200)
    bio = models.TextField()
    image = models.URLField(default="")
    opportunity_owner = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    num_fav = models.IntegerField(default=0)
    favourites = models.ManyToManyField(
        Opportunity,
        related_name='user_favourites'
    )
    
    def __str__(self):
        return self.username
