from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from movies.models import Movie, MovieRating
from .models import UserPreference, FavoriteMovie, WatchedMovie, UserFollow
from .serializers import (
    UserPreferenceSerializer,
    FavoriteMovieSerializer,
    WatchedMovieSerializer,
    MeSerializer,
    SignupSerializer,
    PublicUserProfileSerializer,
)
from movies.serializers import (
    MovieResponseSerializer,
    )

User = get_user_model()

# 회원가입
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # 1. 요청 데이터 로깅 (디버깅 목적)
        print("Received signup request with data:", request.data)

        # 2. username 중복 확인
        username = request.data.get('username')
        if username and User.objects.filter(username=username).exists():
            return Response({"username": ["이미 사용 중인 아이디입니다."]}, status=status.HTTP_400_BAD_REQUEST)

        # 3. 기존 serializer 로직 실행
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(MeSerializer(user).data, status=201)

        # 유효성 검사 실패 시 에러 출력
        print("❌ signup errors:", serializer.errors)
        return Response(serializer.errors, status=400)


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

class UserProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = PublicUserProfileSerializer(user, context={'request': request})
        return Response(serializer.data)

class UserReviewListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        reviews = MovieRating.objects.filter(user=user).select_related("movie")

        data = [
            {
                "movie": review.movie.title,
                "movie_id": review.movie.id,
                "rating": review.rating,
                "comment": review.comment,
            }
            for review in reviews
        ]

        return Response(data)


class FollowToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, id=user_id)

        # 자기 자신 팔로우 방지
        if target == request.user:
            return Response({"error": "You cannot follow yourself."}, status=400)

        follow, created = UserFollow.objects.get_or_create(
            follower=request.user,
            following=target
        )

        if not created:
            follow.delete()
            return Response({"followed": False})

        return Response({"followed": True})

class FollowerListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        followers = user.followers.select_related("follower")

        data = []
        for f in followers:
            follower_user = f.follower
            is_following = False
            if request.user.is_authenticated:
                is_following = UserFollow.objects.filter(
                    follower=request.user,
                    following=follower_user
                ).exists()
            
            # getattr로 안전하게 가져오기
            profile_image = getattr(follower_user, 'profile_image', None)
            profile_image_url = None
            if profile_image and hasattr(profile_image, 'url'):
                profile_image_url = profile_image.url
            
            data.append({
                "id": follower_user.id,
                "username": follower_user.username,
                "email": follower_user.email,
                "profile_image": profile_image_url,
                "is_following": is_following
            })

        return Response(data)


class FollowingListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        following = user.following.select_related("following")

        data = []
        for f in following:
            following_user = f.following
            is_following = False
            if request.user.is_authenticated:
                is_following = UserFollow.objects.filter(
                    follower=request.user,
                    following=following_user
                ).exists()
            
            # getattr로 안전하게 가져오기
            profile_image = getattr(following_user, 'profile_image', None)
            profile_image_url = None
            if profile_image and hasattr(profile_image, 'url'):
                profile_image_url = profile_image.url
            
            data.append({
                "id": following_user.id,
                "username": following_user.username,
                "email": following_user.email,
                "profile_image": profile_image_url,
                "is_following": is_following
            })

        return Response(data)