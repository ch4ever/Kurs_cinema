from django.urls import path
from .views import MovieViewSet, CreateFranchiseView,CreateActorView, CreateGenreView
from rest_framework.routers import DefaultRouter
from django.urls import include

router = DefaultRouter()
router.register('movies', MovieViewSet, basename='movies')
router.register('franchise', CreateFranchiseView.as_view(),basename='franchise')
router.register('actor', CreateActorView.as_view(),basename='actor')
router.register('genre', CreateGenreView.as_view(),basename='genre')


urlpatterns =[
    path('api/', include(router.urls)),
]