from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Actor,Movie,Review
from .serializers import ActorSerializer, MovieSerializer, ReviewSerializer
from .serializers import ActorListserializer, MovieListSerializer, ReviewListSerializer


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
    
@api_view(['GET'])
def review_list(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)
    
@api_view(['GET','PUT','DELETE'])
def review_detail(request,reviews_pk):
    review = Review.objects.get(pk=reviews_pk)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        review.delete()
        data = {
            'message' : f' review {reviews_pk} is deleted. '
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def reviews_create(request,movies_pk):

    movie = Movie.objects.get(pk=movies_pk)
    if request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
    else:
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
    
