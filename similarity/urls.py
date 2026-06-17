from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_track, name='add_track'),
    path('playlists/', views.my_playlists, name='my_playlists'),
    path('create_playlist/', views.create_playlist, name='create_playlist'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
]