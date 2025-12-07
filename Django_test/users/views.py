from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from movies.models import Movie
from .models import UserPreference, FavoriteMovie, WatchedMovie
from .serializers import UserPreferenceSerializer


User = get_user_model()

class UserPreferenceView(APIView):
    def get(self, request):
        prefs = UserPreference.objects.filter(user=request.user).first()
        if not prefs:
            return Response({"favorite_genres": []})
        serializer = UserPreferenceSerializer(prefs)
        return Response(serializer.data)

    def post(self, request):
        prefs, _ = UserPreference.objects.get_or_create(user=request.user)
        serializer = UserPreferenceSerializer(
            prefs, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class FavoriteMovieView(APIView):
    def post(self, request):
        movie_id = request.data.get("movie_id")
        movie = get_object_or_404(Movie, id=movie_id)

        FavoriteMovie.objects.get_or_create(
            user=request.user,
            movie=movie
        )

        return Response(
            {"message": "Favorite added"},
            status=status.HTTP_201_CREATED
        )

class FavoriteMovieDetailView(APIView):
    def delete(self, request, movie_id):
        favorite = FavoriteMovie.objects.filter(
            user=request.user,
            movie_id=movie_id
        )
        favorite.delete()

        return Response({"message": "Favorite removed"})

class WatchedMovieView(APIView):
    def post(self, request):
        movie_id = request.data.get("movie_id")
        movie = get_object_or_404(Movie, id=movie_id)

        WatchedMovie.objects.get_or_create(
            user=request.user,
            movie=movie
        )

        return Response(
            {"message": "Watched movie recorded"},
            status=status.HTTP_201_CREATED
        )

# 내 정보 조회
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        })

# 내 정보 수정
class MeUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        user.email = request.data.get("email", user.email)
        user.save()
        return Response({"message": "Profile updated"})

# 삭제
class MeDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.delete()
        return Response({"message": "User deleted"})

# 회원가입
class SignupView(APIView):
    permission_classes = []  # ✅ 인증 불필요

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Signup successful"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=400)
