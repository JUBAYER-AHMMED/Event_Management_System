from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images', blank=True, default='profile_images/def_img.jpg')
    bio = models.TextField(blank = True)
    phone_no = models.CharField(max_length=20, blank=True, null=True, unique=True)
    
    def __str__(self):
        return self.username