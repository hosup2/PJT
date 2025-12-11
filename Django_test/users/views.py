from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from movies.models import Movie
from .models import UserPreference, FavoriteMovie, WatchedMovie
from .serializers import (
    UserPreferenceSerializer,
    FavoriteMovieSerializer,
    WatchedMovieSerializer,
    MeSerializer,
    SignupSerializer,
)
from movies.serializers import MovieResponseSerializer

User = get_user_model()

# 회원가입
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(MeSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 내 정보
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(MeSerializer(request.user).data)

# 내 정보 수정
class MeUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = MeSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(MeSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 회원 삭제
class MeDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 
class UserPreferenceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pref, _ = UserPreference.objects.get_or_create(user=request.user)
        serializer = UserPreferenceSerializer(pref)
        return Response(serializer.data)

    def put(self, request):
        pref, _ = UserPreference.objects.get_or_create(user=request.user)
        serializer = UserPreferenceSerializer(pref, data=request.data)
        if serializer.is_valid():
            pref = serializer.save()
            return Response(UserPreferenceSerializer(pref).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavoriteMovieView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = FavoriteMovie.objects.filter(user=request.user)\
                                         .select_related("movie")
        movies = [fav.movie for fav in favorites]
        serializer = MovieResponseSerializer(movies, many=True)
        return Response(serializer.data)


class FavoriteMovieDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        FavoriteMovie.objects.get_or_create(user=request.user, movie=movie)
        return Response({"detail": "added"}, status=status.HTTP_201_CREATED)

    def delete(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        FavoriteMovie.objects.filter(user=request.user, movie=movie).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchedMovieView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        watched = WatchedMovie.objects.filter(user=request.user)\
                                      .select_related("movie")
        movies = [w.movie for w in watched]
        serializer = MovieResponseSerializer(movies, many=True)
        return Response(serializer.data)
