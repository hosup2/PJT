from rest_framework.views import APIView
from rest_framework.response import Response
from movies.serializers import MovieSerializer
from .logic import recommend_movies_for_user

# 임시 테스트용
from django.contrib.auth import get_user_model
User = get_user_model()

def get_test_user():
    return User.objects.first()


class RecommendMovieView(APIView):
    def get(self, request):
        user = request.user if request.user.is_authenticated else get_test_user()

        movies = recommend_movies_for_user(user)
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)
