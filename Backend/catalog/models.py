from django.db import models
from django.conf import settings


# Create your models here.
class Franchise(models.Model):
    name = models.CharField(max_length = 50)
    description = models.TextField(blank = True)
    def __str__(self):
        return f"{self.name} {self.description}".strip()


class Actor(models.Model):
    name = models.CharField(max_length = 50)
    surname = models.CharField(max_length = 50)
    description = models.TextField(blank = True,default='')


class Genre(models.Model):
    name = models.CharField(max_length = 50,unique = True)


class Movie(models.Model):
    title = models.CharField(max_length = 150,)
    description = models.TextField()
    release_date = models.DateField()
    poster = models.ImageField(upload_to='posters/', null=True, blank=True, verbose_name="Poster")

    franchise = models.ForeignKey(Franchise, 
                            blank = True, null = True, 
                            on_delete=models.SET_NULL, 
                            related_name='movies')
    actors = models.ManyToManyField(Actor, related_name="movies")
    genres = models.ManyToManyField(Genre, related_name="movies")


class Review(models.Model):
    RATING_CHOICES = (
        ('0.5', '0.5'), ('1', '1'), ('1.5', '1.5'), 
        ('2', '2'), ('2.5', '2.5'), ('3', '3'), 
        ('3.5', '3.5'), ('4', '4'), ('4.5', '4.5'), ('5', '5')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews",
                            on_delete=models.CASCADE,null=True, blank=True)
    movie = models.ForeignKey(Movie, related_name="reviews",
                            on_delete=models.CASCADE,null=True, blank=True)
    rating = models.CharField(choices=RATING_CHOICES)
    text = models.TextField(blank=True,null=True)
    created_at = models.DateField(auto_now_add=True)

class MovieBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    seats = models.JSONField(default=list) 
    created_at = models.DateTimeField(auto_now_add=True)