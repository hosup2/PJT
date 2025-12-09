import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Movie, Genre
from movies.serializers import MovieResponseSerializer
from django.db.models import Q
from rest_framework.permissions import AllowAny


class TMDBImportView(APIView):
    def get(self, request):

        TMDB_KEY = settings.TMDB_API_KEY

        if not TMDB_KEY:
            return Response(
                {"error": "TMDB_API_KEY is missing in environment variables"},
                status=500
            )

        url = (
            f"https://api.themoviedb.org/3/movie/upcoming"
            f"?api_key={TMDB_KEY}&language=ko-KR"
        )

        response = requests.get(url)
        data = response.json()

        # TMDB 요청 실패 시 안전 처리
        if "results" not in data:
            return Response(
                {
                    "error": "Invalid TMDB API response",
                    "tmdb_response": data
                }, 
                status=500
            )

        imported_count = 0

        for item in data["results"]:

            # 장르 처리
            genre_ids = item.get("genre_ids", [])
            movie_genres = []

            for gid in genre_ids:
                genre_obj, created = Genre.objects.get_or_create(id=gid, defaults={"name": f"Genre {gid}"})
                movie_genres.append(genre_obj)

            # 영화 저장
            movie, created = Movie.objects.get_or_create(
                tmdb_id=item["id"],
                defaults={
                    "title": item.get("title"),
                    "overview": item.get("overview", ""),
                    "poster_path": item.get("poster_path"),
                    "release_date": item.get("release_date"),
                }
            )

            # 장르 연결 (ManyToMany)
            if created:
                movie.genres.set(movie_genres)
                imported_count += 1

        return Response({"message": "Import completed", "imported_movies": imported_count})



class MovieListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        qs = Movie.objects.all().order_by("-release_date")[:20]
        serializer = MovieResponseSerializer(qs, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieResponseSerializer(movie)
        return Response(serializer.data)

class MovieSearchView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        query = request.GET.get("q", "")

        if not query:
            return Response([], status=200)

        qs = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(original_title__icontains=query)
        ).distinct()

        serializer = MovieResponseSerializer(qs, many=True)
        return Response(serializer.data)