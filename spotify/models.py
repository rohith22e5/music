from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    mobile = models.CharField(max_length=10)
    image = models.ImageField(upload_to='spotify/profile_pics',default='default_user.jpg')
    dob = models.DateField(default=timezone.now)
    def __str__(self):
        return self.username

class Artist(models.Model):
    artist_id = models.BigIntegerField()
    name = models.CharField(max_length=200) 
    followers = models.IntegerField()
    popularity = models.IntegerField()
    image = models.ImageField(upload_to='spotify/artist_pics',default='default_artist.jpg')
    genres = models.CharField(max_length=200,blank=True)
    albums = models.ManyToManyField('Album',related_name='artist',blank=True)
    tracks = models.ManyToManyField('Track',related_name='artist',blank=True)

    def __str__(self):
        return self.name
    
class Album(models.Model):
    album_id = models.BigIntegerField()
    name = models.CharField(max_length=200)
    artists = models.ManyToManyField(Artist,related_name='album')
    image = models.ImageField(upload_to='spotify/album_pics',default='default_album.jpg')
    release_date = models.DateField()
    popularity = models.IntegerField()
    tracks = models.ManyToManyField('Track',related_name='album',blank=True)


    def __str__(self):
        return self.name
    
class Track(models.Model):
    name = models.CharField(max_length=200)
    track_id = models.BigIntegerField()
    artists = models.ManyToManyField(Artist,related_name='track')
    albums = models.ManyToManyField(Album,related_name='track',blank=True)
    popularity = models.IntegerField()
    image = models.ImageField(upload_to='spotify/track_pics',default='default_track.jpg')
    audio_file = models.FileField(upload_to='spotify/tracks',default='default_track.mp3')
    length = models.DurationField()
    
    def __str__(self):
        return self.name
    
class Playlist(models.Model):
    name = models.CharField(max_length=200)
    playlist_id = models.BigIntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='spotify/playlist_pics',default='default_playlist.jpg')
    description = models.TextField()
    tracks = models.ManyToManyField(Track,related_name='playlist',blank=True)
    public = models.BooleanField(default=False)
    followers = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    liked_tracks = models.ManyToManyField(Track, related_name='liked_by',blank=True,null=True)
    liked_artists = models.ManyToManyField(Artist, related_name='liked_by',blank=True,null=True)
    liked_albums = models.ManyToManyField(Album, related_name='liked_by',blank=True,null=True)
    liked_playlists = models.ManyToManyField(Playlist, related_name='liked_by',blank=True,null=True)
    audio_quality = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='high')
    crossfade = models.BooleanField(default=False)
    autoplay = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username   

class Library(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tracks = models.ManyToManyField(Track, related_name='library',blank=True)
    artists = models.ManyToManyField(Artist, related_name='library',blank=True)
    albums = models.ManyToManyField(Album, related_name='library',blank=True)
    playlists = models.ManyToManyField(Playlist, related_name='library',blank=True,null=True)
    
    def __str__(self):
        return self.user.username



    

    
