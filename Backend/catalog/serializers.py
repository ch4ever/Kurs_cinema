from rest_framework import serializers
from .models import Franchise, Movie, Review, Genre, Actor
from .services import *

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name', 'surname']
    

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class FranchiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchise
        fields = ['id', 'name']


class MovieSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True)
    genres = GenreSerializer(many=True)
    franchise = FranchiseSerializer(allow_null=True)
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date','franchise', 'actors', 'genres']

class MovieCreateSerializer(serializers.ModelSerializer):
    actor_ids = serializers.ListField(child=serializers.IntegerField(), required=False,write_only=True)
    genre_ids = serializers.ListField(child=serializers.IntegerField(), required=False,write_only=True)
    franchise_id = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'poster', 'actor_ids', 'genre_ids', 'franchise_id']

    def create(self, validated_data):
        actor_ids = validated_data.pop('actor_ids', [])
        genre_ids = validated_data.pop('genre_ids', [])
        franchise_id = validated_data.pop('franchise_id', None)
        return create_movie(
            actor_ids=actor_ids,
            genre_ids=genre_ids,
            franchise=franchise_id,
            **validated_data,
        )