from django.urls import path
from .views import MovieViewSet, CreateFranchiseView,CreateActorView, CreateGenreView
from rest_framework.routers import DefaultRouter
from django.urls import include

router = DefaultRouter()
router.register('movies', MovieViewSet, basename='movies')


urlpatterns =[
    path('api/', include(router.urls)),
    path('franchise/', CreateFranchiseView.as_view(), name='create-franchise'),
    path('actors/', CreateActorView.as_view(), name='create-actor'),
    path('genres/', CreateGenreView.as_view(), name='create-genre'),
]