from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.http import JsonResponse
import requests
import json
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.urls import reverse
from django.db import IntegrityError


def index(request):
    popular_artists = Artist.objects.all().order_by('-popularity')
    popular_albums = Album.objects.all().order_by('-popularity')
    popular_playlists = Playlist.objects.filter(public=True).order_by('-followers')
    popular_tracks = Track.objects.all().order_by('-popularity')

    p1 = Paginator(popular_artists, 5)
    p2 = Paginator(popular_albums, 5)
    p3 = Paginator(popular_playlists, 5)
    p4 = Paginator(popular_tracks, 5)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        section = request.GET.get('section')
        page_number = request.GET.get('page')
        if section == 'artist':    
            artists_page = p1.get_page(page_number)
            artists_html = render_to_string('spotify/partials/artists.html', {'artists': artists_page})
            return JsonResponse({'html': artists_html})
        elif section == 'album':
            albums_page = p2.get_page(page_number)
            albums_html = render_to_string('spotify/partials/albums.html', {'albums': albums_page})
            return JsonResponse({'html': albums_html})
        elif section == 'playlist':
            playlists_page = p3.get_page(page_number)
            playlists_html = render_to_string('spotify/partials/playlists.html', {'playlists': playlists_page})
            return JsonResponse({'html': playlists_html})
    else:
        artists_page = p1.get_page(1)
        albums_page = p2.get_page(1)
        playlists_page = p3.get_page(1)
        tracks_page = p4.get_page(1)

        context = {
            'popular_artists': artists_page,
            'popular_albums': albums_page,
            'popular_playlists': playlists_page,
            'popular_tracks': tracks_page,
        }
        return render(request, 'spotify/index.html', context)


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"] # username is the name of the input field in the form
        password = request.POST["password"] # password is the name of the input field in the form
        user = authenticate(request, username=username, password=password) # authenticate() is a built-in function provided by Django
        # If authentication successful, log user in
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # Else, return login page again with new context
        else:
            return render(request, "spotify/login.html", {
                "message": "Invalid username or password !!"
            })
    # If method is GET, return login page
    else:
        return render(request, "spotify/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        # Get username, email, password and confirmation password from the form
        username = request.POST["username"] # username is the name of the input field in the form
        email = request.POST["email"] # email is the name of the input field in the form
        password = request.POST["password"] # password is the name of the input field in the form
        confirmation = request.POST["confirmation"] # confirmation is the name of the input field in the form
        # Ensure password matches confirmation
        if 'mobile' in request.POST:
            mobile = request.POST['mobile']

        if 'image' in request.FILES:
            image = request.FILES['image']
        dob = request.POST.get('dob',None)
        if password != confirmation:
            return render(request, "spotify/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            if mobile and image:
                user = User.objects.create_user(username, email, password,mobile=mobile,image=image,dob=dob)
            elif mobile:
                user = User.objects.create_user(username, email, password,mobile=mobile,dob=dob)
            elif image:
                user = User.objects.create_user(username, email, password,image=image,dob=dob)
            else:
                user = User.objects.create_user(username, email, password,dob = dob) # create_user() is a built-in function provided by Django
            user.save()
        except IntegrityError:
            return render(request, "spotify/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    # If method is GET, return register page
    else:
        return render(request, "spotify/register.html")
    
def search(request):
    if request.method =="POST":
        query = request.POST.get('q')
        if query:
            artists = Artist.objects.filter(name__icontains=query)
            albums = Album.objects.filter(name__icontains=query)
            tracks = Track.objects.filter(name__icontains=query)
            playlists = Playlist.objects.filter(name__icontains=query)
            p1 = Paginator(artists,5)
            p2 = Paginator(albums,5)
            p3 = Paginator(tracks,5)
            p4 = Paginator(playlists,5)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                page_number = request.GET.get('page')
                section = request.GET.get('section')
                if section == 'artist':
                    artists = p1.get_page(page_number)
                    artists_html = render_to_string('spotify/partials/artists.html', {'artists': artists})
                    return JsonResponse({'artists': artists_html})
                elif section == 'album':
                    albums = p2.get_page(page_number)
                    albums_html = render_to_string('spotify/partials/albums.html', {'albums': albums})
                    return JsonResponse({'albums': albums_html})
                elif section == 'track':
                    tracks = p3.get_page(page_number)
                    tracks_html = render_to_string('spotify/partials/tracks.html', {'tracks': tracks})
                    return JsonResponse({'tracks': tracks_html})
                elif section == 'playlist':
                    playlists = p4.get_page(page_number)
                    playlists_html = render_to_string('spotify/partials/playlists.html', {'playlists': playlists})
                    return JsonResponse({'playlists': playlists_html})
            else:               
                page_number = 1
                artists = p1.get_page(page_number)
                albums = p2.get_page(page_number)
                tracks = p3.get_page(page_number)
                playlists = p4.get_page(page_number)

                context = {
                    'artists':artists,
                    'albums':albums,
                    'tracks':tracks,
                    'playlists':playlists,
                    'search':True,
                }
                return render(request,'spotify/search.html',context)
        else:
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request,'spotify/search.html')
    
@login_required
def profile(request):
    if request.method =="GET":
        user = request.user
        
        playlists = Playlist.objects.filter(user=user)
        if UserProfile.objects.filter(user=user).exists():
            liked_playlists = UserProfile.objects.get(user=user).liked_playlists.all()
            liked_tracks = UserProfile.objects.get(user=user).liked_tracks.all()
            liked_artists = UserProfile.objects.get(user=user).liked_artists.all()
            p4 = Paginator(liked_playlists,5)
            p2 = Paginator(liked_tracks,5)
            p3 = Paginator(liked_artists,5)
            p1 = Paginator(playlists,5)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                page_number = request.GET.get('page')
                section = request.GET.get('section')
                if section == 'playlist':
                    playlists = p1.get_page(page_number)
                    playlists_html = render_to_string('spotify/partials/playlists.html', {'playlists': playlists})
                    return JsonResponse({'playlists': playlists_html})
                elif section == 'liked_playlist':
                    liked_playlists = p4.get_page(page_number)
                    liked_playlists_html = render_to_string('spotify/partials/liked_playlists.html', {'liked_playlists': liked_playlists})
                    return JsonResponse({'liked_playlists': liked_playlists_html})
                elif section == 'liked_track':
                    liked_tracks = p2.get_page(page_number)
                    liked_tracks_html = render_to_string('spotify/partials/liked_tracks.html', {'liked_tracks': liked_tracks})
                    return JsonResponse({'liked_tracks': liked_tracks_html})
                elif section == 'liked_artist':
                    liked_artists = p3.get_page(page_number)
                    liked_artists_html = render_to_string('spotify/partials/liked_artists.html', {'liked_artists': liked_artists})
                    return JsonResponse({'liked_artists': liked_artists_html})
            else: 
                page_number = 1
                playlists = p1.get_page(page_number)
                liked_playlists = p4.get_page(page_number)
                liked_tracks = p2.get_page(page_number)
                liked_artists = p3.get_page(page_number)
                context = {
                    'user':user,
                    'playlists':playlists,
                    'liked_playlists':liked_playlists,
                    'liked_tracks':liked_tracks,
                    'liked_artists':liked_artists,
                    'profile':True,
                }
                return render(request,'spotify/profile.html',context)
        else:
            p1 = Paginator(playlists,5)
            page_number = request.GET.get('page')
            playlists = p1.get_page(page_number)
            context = {
                'user':user,
                'playlists':playlists,
                'profile':False,
            }
            return render(request,'spotify/profile.html',context)

@login_required
def settings(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        if 'image' in request.FILES:
            user.image = request.FILES['image']
        if 'mobile' in request.POST:
            user.mobile = request.POST['mobile']
        if 'dob' in request.POST:
            user.dob = request.POST['dob']
        user.save()
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.audio_quality = request.POST.get('audio_quality')
        user_profile.crossfade = 'crossfade' in request.POST
        user_profile.autoplay = 'autoplay' in request.POST
        user_profile.save()

        return redirect('settings')

    else:
        user = request.user
        user_profile, created = UserProfile.objects.get_or_create(user=user)

    return render(request, 'spotify/settings.html', {
        'user': user,
        'user_profile': user_profile
    })



def artist_detail(request, artist_id):
    if request.user.is_authenticated:
        artist = get_object_or_404(Artist, artist_id=artist_id)
        tracks = artist.tracks.all()
        return render(request, 'spotify/artist_detail.html', {'artist': artist, 'tracks': tracks})
    else:
        return redirect('login')
def album_detail(request, album_id):
    if request.user.is_authenticated:
        album = get_object_or_404(Album, album_id=album_id)
        tracks = album.tracks.all()
        return render(request, 'spotify/album_detail.html', {'album': album, 'tracks': tracks})
    else:
        return redirect('login')

def track_detail(request, track_id):
    if request.user.is_authenticated:
        track = get_object_or_404(Track, track_id=track_id)
        return render(request, 'spotify/track_detail.html', {'track': track})
    else:
        return redirect('login')

def playlist_detail(request, playlist_id):
    if request.user.is_authenticated:
        playlist = get_object_or_404(Playlist, playlist_id=playlist_id)
        tracks = playlist.tracks.all()
        return render(request, 'spotify/playlist_detail.html', {'playlist': playlist, 'tracks': tracks})
    else:
        return redirect('login')