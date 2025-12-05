from rest_framework.views import APIView
from rest_framework.response import Response
from .logic import recommend_movies_for_user
from movies.serializers import MovieSerializer

class UserRecommendView(APIView):
    def get(self, request):
        movies = recommend_movies_for_user(request.user)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
