from rest_framework import serializers
from .models import Actor,Movie,Review


class ActorSerializer(serializers.ModelSerializer):

    class MovieDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('title',)

    movies = MovieDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ('id', 'name', 'movies')

class ActorListserializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id','name']


class MovieSerializer(serializers.ModelSerializer):

    class ActorDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Actor
            fields = ('name',)

    class ReviewSetSerializer(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = ('title', 'content',)

    actors = ActorDetailSerializer(many= True, read_only=True)
    review_set = ReviewSetSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 
            'actors',
            'review_set',
            'title',
            'overview',
            'release_date',
            'poster_path',
            ]


class ReviewSerializer(serializers.ModelSerializer):

    class MovieDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ['title',]

    movie = MovieDetailSerializer(read_only = True)

    class Meta:
        model = Review
        fields = ['id','movie','title','content',]


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title','overview',]


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['title','content',]


