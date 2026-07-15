from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import include
from .views import (
    FranchiseViewset,
    ActorViewset,
    GenreViewset,
    MovieViewset,
)


router = DefaultRouter()
router.register('movies', MovieViewset, basename='movies')
router.register('franchise',FranchiseViewset, basename='franchise')
router.register('actors',ActorViewset, basename='actor'),
router.register('genres',GenreViewset, basename='genres'),


urlpatterns = [
    path('api/', include(router.urls)),
]