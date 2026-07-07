from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import include
from .views import (
    FranchiseViewset,
    ActorViewset,
    GenreViewset,
    MovieViewset,
    BookMovieView,
    MovieBookedSeatsView,
    MyTicketsView,
)


router = DefaultRouter()
router.register('movies', MovieViewset, basename='movies')
router.register('franchise',FranchiseViewset, basename='franchise')
router.register('actors',ActorViewset, basename='actor'),
router.register('genres',GenreViewset, basename='genres'),


urlpatterns = [
    path('api/movies/<int:movie_id>/seats/', MovieBookedSeatsView.as_view(), name='movie-seats'),
    path('api/movies/<int:movie_id>/book/', BookMovieView.as_view(), name='book-movie'),
    path('api/my-tickets/',MyTicketsView.as_view(),name='my_tickets'),
    path('api/', include(router.urls)),
]