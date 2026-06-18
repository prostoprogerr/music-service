from django.shortcuts import render, redirect, get_object_or_404
from .models import Track, Similarity, Playlist
from .deezer_client import get_similar_tracks, get_preview_url
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'similarity/index.html')


def add_track(request):
    # 1. НОВЫЙ БЛОК: добавление выбранных треков в плейлист (из формы на странице результатов)
    if request.method == 'POST' and 'add_to_playlist' in request.POST:
        track_ids = request.POST.getlist('track_ids')
        playlist_id = request.POST.get('playlist_id')
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        # Определяем, какой плейлист использовать
        if playlist_id == 'new':
            new_name = request.POST.get('new_playlist_name')
            if not new_name:
                return render(request, 'similarity/add.html', {'error': 'Укажите название нового плейлиста'})
            playlist = Playlist.objects.create(name=new_name, session_key=session_key)
        else:
            try:
                playlist = Playlist.objects.get(id=playlist_id, session_key=session_key)
            except Playlist.DoesNotExist:
                return render(request, 'similarity/add.html', {'error': 'Плейлист не найден'})

        # Добавляем треки в плейлист (ManyToMany сам избегает дубликатов)
        playlist.tracks.add(*track_ids)
        return redirect('my_playlists')

    # 2. СТАРЫЙ БЛОК: создание плейлиста из формы на странице результатов (create_playlist)
    if request.method == 'POST' and 'create_playlist' in request.POST:
        playlist_name = request.POST.get('playlist_name')
        track_ids = request.POST.getlist('track_ids')
        if playlist_name and track_ids:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            playlist = Playlist.objects.create(name=playlist_name, session_key=session_key)
            playlist.tracks.add(*track_ids)
            return redirect('my_playlists')
        else:
            return render(request, 'similarity/add.html', {'error': 'Выберите хотя бы один трек и укажите название плейлиста'})

    # 3. ОСНОВНОЙ ПОИСК ПОХОЖИХ ТРЕКОВ
    if request.method == 'POST':
        artist = request.POST['artist']
        title = request.POST['title']
        similar_list = get_similar_tracks(artist, title)
        if not similar_list:
            return render(request, 'similarity/add.html', {'error': 'Трек не найден или нет рекомендаций'})

        # ---- ИСПРАВЛЕНИЕ: обновляем preview_url для исходного трека ПРИ КАЖДОМ поиске ----
        track, created = Track.objects.get_or_create(artist=artist, name=title)
        # Если у трека нет preview_url, пытаемся получить его (даже если трек уже существовал)
        if not track.preview_url:
            preview = get_preview_url(artist, title)
            if preview:
                track.preview_url = preview
                track.save()

        # Сохраняем похожие треки с preview_url
        similar_tracks = []
        for sim in similar_list:
            sim_track, _ = Track.objects.get_or_create(
                artist=sim['artist'],
                name=sim['name'],
                defaults={'preview_url': sim.get('preview_url', '')}
            )
            similar_tracks.append(sim_track)
            Similarity.objects.get_or_create(
                from_track=track,
                to_track_name=sim['name'],
                to_track_artist=sim['artist'],
                defaults={'score': sim['match_score'], 'preview_url': sim.get('preview_url', '')}
            )

        # Получаем список плейлистов пользователя для выпадающего списка
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        user_playlists = Playlist.objects.filter(session_key=session_key)

        return render(request, 'similarity/results.html', {
            'track': track,
            'similar_tracks': similar_tracks,
            'playlists': user_playlists,
        })

    return render(request, 'similarity/add.html')


def my_playlists(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    playlists = Playlist.objects.filter(session_key=session_key)
    return render(request, 'similarity/playlists.html', {'playlists': playlists})


def create_playlist(request):
    if request.method == 'POST':
        name = request.POST['name']
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        playlist = Playlist.objects.create(name=name, session_key=session_key)
        track_ids = request.POST.getlist('tracks')
        playlist.tracks.add(*track_ids)
        return redirect('my_playlists')
    tracks = Track.objects.all()
    return render(request, 'similarity/create_playlist.html', {'tracks': tracks})


def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    tracks = playlist.tracks.all()
    return render(request, 'similarity/playlist_detail.html', {'playlist': playlist, 'tracks': tracks})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'similarity/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'similarity/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')