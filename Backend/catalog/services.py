from django.db import transaction
from .models import Movie,Franchise, Genre, Actor
from datetime import datetime

def create_franchise(name: str) -> Franchise:
    with transaction.atomic():
        franchise = Franchise.objects.create(name=name)
        return franchise

def create_genre(name: str) -> Genre:
    with transaction.atomic():
        genre = Genre.objects.create(name=name)
        return genre

def create_actor(name: str, surname: str) -> Actor:
    with transaction.atomic():
        actor = Actor.objects.create(name=name, surname=surname)
        return actor

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

