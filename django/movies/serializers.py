from rest_framework import serializers
from .models import Actor,Movie,Review


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id','name']

class MovieSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(many= True)

    class Meta:
        model = Movie
        fields = ['id','title','overview','release_date','poster_path','actors']


class ReviewSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()

    class Meta:
        movie = Review
        fields = ['id','movie','title','content']
