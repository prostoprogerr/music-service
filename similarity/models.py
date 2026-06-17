from django.db import models

class Track(models.Model):
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    preview_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.artist} - {self.name}"

class Similarity(models.Model):
    from_track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='similarities')
    to_track_name = models.CharField(max_length=200)
    to_track_artist = models.CharField(max_length=200)
    score = models.FloatField()

    def __str__(self):
        return f"{self.from_track} → {self.to_track_artist} - {self.to_track_name}"

class Playlist(models.Model):
    name = models.CharField(max_length=100)
    session_key = models.CharField(max_length=50)
    tracks = models.ManyToManyField(Track)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Similarity(models.Model):
    from_track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='similarities')
    to_track_name = models.CharField(max_length=200)
    to_track_artist = models.CharField(max_length=200)
    score = models.FloatField()
    preview_url = models.URLField(blank=True, null=True)