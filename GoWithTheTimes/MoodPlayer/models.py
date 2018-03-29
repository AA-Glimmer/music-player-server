from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class usermodel(models.Model):
    user_id = models.OneToOneField(User)
    happy = models.FloatField(default = 0.5, null=False, blank=False)
    sad = models.FloatField(default = 0.5, null=False, blank=False)
    angry = models.FloatField(default = 0.5, null=False, blank=False)
    anxious = models.FloatField(default = 0.5, null=False, blank=False)
    loving = models.FloatField(default = 0.5, null=False, blank=False)
    fearful = models.FloatField(default = 0.5, null=False, blank=False)
    updaterate = models.FloatField(default = 0.0, null=False, blank=False)

    def __str__(self):
        return str(self.user_id)

class user_preference(models.Model):
    user_id = models.OneToOneField(usermodel)
    rap = models.FloatField(default = 1, null=False, blank=False)
    pop = models.FloatField(default = 1, null=False, blank=False)
    rock = models.FloatField(default = 1, null=False, blank=False)
    counter = models.IntegerField(default=0,null=False, blank=False)

    def __str__(self):
        return str(self.user_id)

class song_metadata(models.Model):
    song_id = models.CharField(default = 'song_100',max_length = 15)
    title = models.CharField(default = 'abc',max_length = 100)
    song_length = models.IntegerField(default=0,null=False, blank=False)
    size = models.IntegerField(default=0,null=False, blank=False)
    path = models.CharField(default = '/Users/WolfDen/Desktop/songs/',max_length = 100)
    genre = models.CharField(default='pop', max_length = 5)
    mood = models.CharField(default='happy', max_length = 10)
    def __str__(self):
        return str(self.id)

class like_song(models.Model):
    user_id = models.ForeignKey(usermodel)
    song_id = models.ForeignKey(song_metadata)
    def __str__(self):
        return str(self.user_id)

class hate_song(models.Model):
    user_id = models.ForeignKey(usermodel)
    song_id = models.ForeignKey(song_metadata)
    def __str__(self):
        return str(self.user_id)
