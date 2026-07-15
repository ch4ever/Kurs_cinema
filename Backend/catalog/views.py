from django.db.models.base import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ActorSerializer, GenreSerializer, MovieCreateSerializer, MovieSerializer, FranchiseSerializer,MovieBookingSerializer
from .models import Actor, Franchise, Genre, Movie, MovieBooking
from siteuser.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class MovieViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication,]
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action in ('create','partial_update','update'):
            return MovieCreateSerializer
        return MovieSerializer

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



@extend_schema_view(
    list = extend_schema(
        summary="Franchise list",
        tags=["Franchise"],
        responses={
            status.HTTP_200_OK: FranchiseSerializer(many=True)},
    ),
    retrieve = extend_schema(
        summary="Franchise retrieve",
        tags=["Franchise"],
        responses={
            status.HTTP_200_OK: FranchiseSerializer()},
    ),
    create = extend_schema(
        summary="Franchise create",
        tags=["Franchise"],
        responses={
            status.HTTP_201_CREATED: FranchiseSerializer}
    ),
    destroy = extend_schema(
        summary="Franchise delete",
        tags=["Franchise"],
        responses= {status.HTTP_204_NO_CONTENT: None}
    ),
    partial_update = extend_schema(
        summary="Franchise patch",
        tags=["Franchise"],
        responses={
            status.HTTP_200_OK:FranchiseSerializer() }
    ),
    update = extend_schema(
        summary="Franchise update",
        tags=["Franchise"],
        responses={
            status.HTTP_200_OK: FranchiseSerializer() }
    ),
)
class FranchiseViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = FranchiseSerializer
    queryset = Franchise.objects.all()

    def get_queryset(self):
        query = super().get_queryset()
        if self.action in ['retrieve','list']:
            return query.prefetch_related('movies')
        return query 

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action in ['list','retrieve']:
            return [AllowAny()]
        return super().get_permissions()


@extend_schema_view(
    list = extend_schema(
        summary="Actors list",
        tags=["Actor"],
        responses={
            status.HTTP_200_OK: ActorSerializer(many=True)},
    ),
    retrieve = extend_schema(
        summary="Actor retrieve",
        tags=["Actor"],
        responses={
            status.HTTP_200_OK: ActorSerializer()},
    ),
    create = extend_schema(
        summary="Actor create",
        tags=["Actor"],
        responses={
            status.HTTP_201_CREATED: ActorSerializer}
    ),
    destroy = extend_schema(
        summary="Actors delete",
        tags=["Actor"],
        responses= {status.HTTP_204_NO_CONTENT: None}
    ),
    partial_update = extend_schema(
        summary="Actor patch",
        tags=["Actor"],
        responses={
            status.HTTP_200_OK:ActorSerializer() }
    ),
    update = extend_schema(
        summary="Actor update",
        tags=["Actor"],
        responses={
            status.HTTP_200_OK: ActorSerializer() }
    ),
)
class ActorViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action in ['list','retrieve']:
            return [AllowAny()]
        return super().get_permissions()

   
@extend_schema_view(
    list = extend_schema(
        summary="Genres list",
        tags=["Genre"],
        responses={
            status.HTTP_200_OK: GenreSerializer(many=True)},
    ),
    retrieve = extend_schema(
        summary="Genre retrieve",
        tags=["Genre"],
        responses={
            status.HTTP_200_OK: GenreSerializer()},
    ),
    create = extend_schema(
        summary="Genres create",
        tags=["Genre"],
        responses={
            status.HTTP_201_CREATED: GenreSerializer}
    ),
    destroy = extend_schema(
        summary="Genres delete",
        tags=["Genre"],
        responses= {status.HTTP_204_NO_CONTENT: None}
    ),
    partial_update = extend_schema(
        summary="Genres patch",
        tags=["Genre"],
        responses={
            status.HTTP_200_OK:GenreSerializer() }
    ),
    update = extend_schema(
        summary="Genre update",
        tags=["Genre"],
        responses={
            status.HTTP_200_OK: GenreSerializer() }
    ),
)
class GenreViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action in ['list','retrieve']:
            return [AllowAny()]
        return super().get_permissions()

