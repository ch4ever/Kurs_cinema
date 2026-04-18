import pytest
from .services import create_movie
from .models import *


@pytest.mark.django_db
def test_create_movie_success():
    actor1= Actor.objects.create(name='Киану',surname='Ривз')
    actor2 = Actor.objects.create(name='Anna', surname = 'Fox')
    fran = Franchise.objects.create(name='Sonic Universe')
    genre_fan = Genre.objects.create(name="Fantasy")
     
    movie = create_movie(title="Super Sonic 4",description='Sonic investigates something inavadable', 
            release_date='2025-12-12', actor_ids=[actor1.id, actor2.id], genre_ids=[genre_fan.id],franchise=fran.id)

    assert Movie.objects.count() == 1
    assert movie.actors.count() == 2
    assert movie.title == 'Super Sonic 4'
    assert movie.franchise.name == 'Sonic Universe'
