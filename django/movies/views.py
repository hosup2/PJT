from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Actor,Movie,Review
from .serializers import ActorSerializer, MovieSerializer, ReviewSerializer
from .serializers import ActorListserializer, MovieListSerializer


# Create your views here.


@api_view(['GET'])
def actors_list(request):
    if request.method == "GET":
        actors = Actor.objects.all()
        serializer = ActorListserializer(actors, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def actors_detail(request, actors_pk):
    actor = Actor.objects.get(pk=actors_pk)
    if request.method == "GET":
        serializer = ActorSerializer(actor)
        return Response(serializer.data)
    
@api_view(['GET'])
def movie_list(request):
    if request.method == "GET":
        movies = Movie.objects.all()
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def movie_detail(request, movies_pk):
    movie = Movie.objects.get(pk=movies_pk)
    if request.method == "GET":
        serializer = MovieSerializer(movie)
        return Response(serializer.data)



