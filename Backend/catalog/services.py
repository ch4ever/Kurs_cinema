from django.db import transaction
from .models import Movie,Franchise, Genre, Actor
from datetime import datetime

def create_franchise(name: str) -> Franchise:
    with transaction.atomic():
        if not Franchise.objects.filter(name=name).exists():
            franchise = Franchise.objects.create(name=name)
            return franchise
        else:
            raise ValueError("Franchise with this name already exists")

def create_actor(name: str, surname: str) -> Actor:
    with transaction.atomic():
        if not Actor.objects.filter(name=name, surname=surname).exists():
            actor = Actor.objects.create(name=name, surname=surname)
            return actor
        else:
            raise ValueError("Actor with this name and surname already exists")

def create_genre(name: str):
    with transaction.atomic():
        if not Actor.objects.filter(name=name).exists():
            actor = Actor.objects.create(name=name)
            return actor
        else:
            raise ValueError("Genre already exists")

def create_movie(title: str, description:str, release_date: datetime, franchise: int=None, 
    actor_ids: list[int] = None, genre_ids: list[int] = None,) -> Movie:
    with transaction.atomic():
        movie = Movie.objects.create(
            title=title,
            description=description,
            release_date=release_date,
            franchise=franchise
        )
        movie.actors.set(actor_ids or [])
        movie.genres.set(genre_ids or [])
    return movie

