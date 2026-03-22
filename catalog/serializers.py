from rest_framework import serializers
from .models import Franchise, Movie, Review, Rating, Genre, Actor
from .services import create_movie

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
    franchise = FranchiseSerializer()
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date','franchise', 'actors', 'genres']

class MovieCreateSerializer(serializers.ModelSerializer):
    actor_ids = serializers.ListField(child=serializers.IntegerField(), required=False,write_only=True)
    genre_ids = serializers.ListField(child=serializers.IntegerField(), required=False,write_only=True)
    class Meta:
        model = Movie
        fields = [ 'title', 'description', 'release_date', 'actor_ids', 'genre_ids']

    def create(self, validated_data):
        return create_movie(**validated_data)