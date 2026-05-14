from django.urls import path
from .views import (
    MovieViewSet,
    CreateFranchiseView,
    CreateActorView,
    CreateGenreView,
    BookMovieView,
    MovieBookedSeatsView,
    MyTicketsView,
)
from rest_framework.routers import DefaultRouter
from django.urls import include

router = DefaultRouter()
router.register('movies', MovieViewSet, basename='movies')


urlpatterns = [
    path('api/movies/<int:movie_id>/seats/', MovieBookedSeatsView.as_view(), name='movie-seats'),
    path('api/movies/<int:movie_id>/book/', BookMovieView.as_view(), name='book-movie'),
    path('api/my-tickets/',MyTicketsView.as_view(),name='my_tickets'),
    path('api/', include(router.urls)),
    path('franchise/', CreateFranchiseView.as_view(), name='create-franchise'),
    path('actors/', CreateActorView.as_view(), name='create-actor'),
    path('genres/', CreateGenreView.as_view(), name='create-genre'),
]