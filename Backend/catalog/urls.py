from django.urls import path
from .views import MovieViewSet
from rest_framework.routers import DefaultRouter
from django.urls import include

router = DefaultRouter()
router.register('movies', MovieViewSet, basename='movies')


urlpatterns =[
    path('api/', include(router.urls)),
]