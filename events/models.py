from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

class Category(models.Model):
    name = models.CharField( max_length = 100)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField( max_length = 100)
    description = models.TextField(blank=True,null = True)
    date = models.DateField()
    time = models.TimeField()
    location = models.TextField()
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE ,
                                related_name='events' )
    participants_users = models.ManyToManyField(
        User,
        related_name="events_joined",
        blank=True
    )
    asset = models.ImageField(upload_to="events_asset",blank= True, null = True, default="default.jpg")

    
    def __str__(self):
        return self.name
    
# class Participant(models.Model):
#     name = models.CharField( max_length = 100)
#     email = models.EmailField(unique = True)
#     events = models.ManyToManyField(Event,related_name='participants')
#     is_confirmed = models.BooleanField(default=False)
    
#     def __str__(self):
#         return self.name