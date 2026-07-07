from rest_framework import serializers
from .models import Franchise, Movie, Review, Genre, Actor,MovieBooking
from .services import *

class ActorSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Actor
        fields = ['id', 'name', 'surname', 'description']
        read_only_fields = ['id']

    def create(self, validated_data):
        actor = create_actor(**validated_data)
        return actor
        

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id','name']
        read_only_fields = ['id']

    def create(self,validated_data):
        genre = create_genre(**validated_data)
        return genre


class FranchiseSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Franchise
        fields = ['id', 'name','description']
        read_only_fields = ['id']

    def create(self, validated_data):
        franchise = create_franchise(**validated_data)
        return franchise



class MovieSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True)
    genres = GenreSerializer(many=True)
    franchise = FranchiseSerializer(allow_null=True)
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date','franchise', 'actors', 'genres','poster']


class MovieCreateSerializer(serializers.ModelSerializer):
    actors = serializers.PrimaryKeyRelatedField(
        queryset=Actor.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )

    genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )

    franchise = serializers.PrimaryKeyRelatedField(
        queryset=Franchise.objects.all(),
        required=False,
        allow_null=True,
    )
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'poster', 'actors', 'genres', 'franchise']

    def create(self, validated_data):
        actors = validated_data.pop('actors', [])
        genres = validated_data.pop('genres', [])
        franchise = validated_data.pop('franchise', None)
        return create_movie(
            actors=actors,
            genres=genres,
            franchise=franchise,
            **validated_data,
        )

    def update(self, instance, validated_data):
        actors = validated_data.pop('actors', None)
        genres = validated_data.pop('genres', None)
        franchise = validated_data.pop('franchise', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if franchise is not None:
            instance.franchise = franchise

        instance.save()

        if actors is not None:
            instance.actors.set(actors)

        if genres is not None:
            instance.genres.set(genres)

        return instance


#TODO make for this another app
class MovieBookingSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True) 
    
    class Meta:
        model = MovieBooking
        fields = ['id', 'movie', 'seats', 'created_at'] 
        read_only_fields = ['id', 'created_at']