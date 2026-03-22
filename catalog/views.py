from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import MovieCreateSerializer, MovieSerializer
from .models import Movie
from siteuser.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication, JWTAuthentication, SessionAuthentication

# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,JWTAuthentication,SessionAuthentication]
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return MovieCreateSerializer
        return MovieSerializer
        #LATER: add other serializers for other actions

    def get_queryset(self):
        movie = super().get_queryset()

        if self.action in ['list','retrieve']:
            movie = movie.select_related('franchise').prefetch_related('actors','genres')
        return movie

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action == 'list' or self.action == 'retrieve':
            return [AllowAny()]
        return super().get_permissions()
