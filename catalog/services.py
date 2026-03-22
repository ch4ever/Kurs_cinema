from django.db import transaction
from .models import Movie

def create_movie(title: str, description:str, release_date, franchise: str, 
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