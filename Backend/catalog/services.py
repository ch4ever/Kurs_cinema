from django.db import transaction
from .models import Movie,Franchise, Genre, Actor
from datetime import datetime

def create_franchise(name: str, description : str = '') -> Franchise:
    with transaction.atomic():
        if not Franchise.objects.filter(name=name).exists():
            franchise = Franchise.objects.create(name=name, description=description or '')
            return franchise
        

def create_actor(name: str, surname: str, description: str = '') -> Actor:
    with transaction.atomic():
        if not Actor.objects.filter(name=name, surname=surname).exists():
            actor = Actor.objects.create(name=name, surname=surname, description= description or '')
            return actor
        else:
            return None

def create_genre(name: str) -> Genre:
    with transaction.atomic():
        if not Genre.objects.filter(name=name).exists():
            actor = Genre.objects.create(name=name)
            return actor
        else:
            raise ValueError("Genre already exists")

def create_movie(
    title: str,
    description: str,
    release_date: datetime,
    franchise: Franchise | None = None,
    actors: list[Actor] | None = None,
    genres: list[Genre] | None = None,
    poster=None,
) -> Movie:
    with transaction.atomic():
        movie = Movie.objects.create(
            title=title,
            description=description,
            release_date=release_date,
            franchise_id=franchise.id if franchise else None,
            poster=poster,
        )
        movie.actors.set(actors or [])
        movie.genres.set(genres or [])
    return movie

