from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("register",views.register,name="register"),
    path("search",views.search,name="search"),
    path("profile",views.profile,name="profile"),
    path("settings",views.settings,name="settings"),
    path('artist/<int:artist_id>/', views.artist_detail, name='artist_detail'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('track/<int:track_id>/', views.track_detail, name='track_detail'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),

]
