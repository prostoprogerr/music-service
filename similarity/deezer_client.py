import requests


def get_similar_artists(artist_name):
    search_url = "https://api.deezer.com/search/artist"
    params = {"q": artist_name, "limit": 1}
    resp = requests.get(search_url, params=params)
    if resp.status_code != 200:
        return []
    data = resp.json()
    if not data.get("data"):
        return []
    artist_id = data["data"][0]["id"]

    related_url = f"https://api.deezer.com/artist/{artist_id}/related"
    related_resp = requests.get(related_url)
    if related_resp.status_code != 200:
        return []
    related_data = related_resp.json()
    similar = [artist["name"] for artist in related_data.get("data", [])[:5]]
    return similar


def get_top_tracks(artist_name, limit=3):
    search_url = "https://api.deezer.com/search/artist"
    params = {"q": artist_name, "limit": 1}
    resp = requests.get(search_url, params=params)
    if resp.status_code != 200:
        return []
    data = resp.json()
    if not data.get("data"):
        return []
    artist_id = data["data"][0]["id"]

    tracks_url = f"https://api.deezer.com/artist/{artist_id}/top"
    tracks_resp = requests.get(tracks_url, params={"limit": limit})
    if tracks_resp.status_code != 200:
        return []
    tracks_data = tracks_resp.json()

    result = []
    for idx, track in enumerate(tracks_data.get("data", [])):
        result.append({
            "name": track["title"],
            "artist": artist_name,
            "match_score": round(1.0 - idx * 0.2, 2),
            "preview_url": track.get("preview"),
            "track_id": track.get("id")
        })
    return result


def get_similar_tracks(artist, track, limit=5):
    similar_artists = get_similar_artists(artist)
    if not similar_artists:
        return []
    all_tracks = []
    for similar_artist in similar_artists[:3]:
        top = get_top_tracks(similar_artist, limit=2)
        all_tracks.extend(top)
    return all_tracks[:limit]

def get_preview_url(artist, track_name):
    search_url = "https://api.deezer.com/search"
    params = {"q": f'artist:"{artist}" track:"{track_name}"', "limit": 1}
    resp = requests.get(search_url, params=params)
    if resp.status_code != 200:
        return None
    data = resp.json()
    if data.get("data"):
        return data["data"][0].get("preview")
    return None