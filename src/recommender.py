from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Recommends top-k songs for the given user profile."""
        # Convert UserProfile to dict for score_song
        user_prefs = {
            'genre': user.favorite_genre,
            'mood': user.favorite_mood,
            'energy': user.target_energy,
            'likes_acoustic': user.likes_acoustic
        }
        
        # Score all songs
        scored = []
        for song in self.songs:
            song_dict = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'genre': song.genre,
                'mood': song.mood,
                'energy': song.energy,
                'tempo_bpm': song.tempo_bpm,
                'valence': song.valence,
                'danceability': song.danceability,
                'acousticness': song.acousticness
            }
            score, _ = score_song(user_prefs, song_dict)
            scored.append((song, score))
        
        # Sort descending
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k Song objects
        return [s[0] for s in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generates a plain-language explanation for why this song was recommended."""
        user_prefs = {
            'genre': user.favorite_genre,
            'mood': user.favorite_mood,
            'energy': user.target_energy,
            'likes_acoustic': user.likes_acoustic
        }
        song_dict = {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'genre': song.genre,
            'mood': song.mood,
            'energy': song.energy,
            'tempo_bpm': song.tempo_bpm,
            'valence': song.valence,
            'danceability': song.danceability,
            'acousticness': song.acousticness
        }
        _, reasons = score_song(user_prefs, song_dict)
        return ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file and returns a list of dictionaries."""
    import csv
    songs = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness'])
            })
    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences and returns (score, reasons)."""
    score = 0.0
    reasons = []
    
    # Genre match: +2.0
    if song['genre'] == user_prefs.get('genre'):
        score += 2.0
        reasons.append("genre match (+2.0)")
    
    # Mood match: +1.0
    if song['mood'] == user_prefs.get('mood'):
        score += 1.0
        reasons.append("mood match (+1.0)")
    
    # Energy similarity: 1 - |song.energy - target_energy| → 0 to +1.0
    target_energy = user_prefs.get('energy', 0.5)
    energy_score = 1.0 - abs(song['energy'] - target_energy)
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score:.2f})")
    
    # Acoustic bonus: +0.5 if likes_acoustic is True and song is highly acoustic
    if user_prefs.get('likes_acoustic') and song['acousticness'] > 0.6:
        score += 0.5
        reasons.append("acoustic bonus (+0.5)")
    
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Functional implementation: scores all songs, ranks, and returns top-k with explanations."""
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored_songs.append((song, score, explanation))
    
    # Sort descending by score
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    return scored_songs[:k]