from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class videodisplayer(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='imgs')
    likes = models.IntegerField()
    desc = models.TextField(null=True,blank=True)
    owner = models.CharField(max_length=50)
    comments = models.TextField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class usermodellikedvideoslist(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    likedvids = models.TextField(null=True,blank=True)