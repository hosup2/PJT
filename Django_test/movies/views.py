import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import Movie, Genre, FeaturedMovie
from .serializers import MovieResponseSerializer, FeaturedMovieSerializer


# TMDB 날짜 안전 파서
def safe_date(value):
    return value if value else None


# TMDB 장르 처리 함수
def get_or_create_genres(genre_ids):
    genres = []
    for gid in genre_ids:
        g, _ = Genre.objects.get_or_create(id=gid, defaults={"name": f"Genre {gid}"})
        genres.append(g)
    return genres


class TMDBImportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        TMDB_KEY = settings.TMDB_API_KEY

        if not TMDB_KEY:
            return Response({"error": "TMDB_API_KEY missing"}, status=500)

        url = (
            f"https://api.themoviedb.org/3/movie/upcoming"
            f"?api_key={TMDB_KEY}&language=ko-KR"
        )

        res = requests.get(url)
        data = res.json()

        if "results" not in data:
            return Response({"error": "Invalid TMDB response", "response": data}, status=500)

        imported = 0

        for item in data["results"]:
            genre_list = get_or_create_genres(item.get("genre_ids", []))

            movie, created = Movie.objects.get_or_create(
                tmdb_id=item["id"],
                defaults={
                    "title": item.get("title") or "",
                    "original_title": item.get("original_title"),
                    "overview": item.get("overview") or "",
                    "poster_path": item.get("poster_path"),
                    "backdrops": item.get("backdrop_path"),
                    "release_date": safe_date(item.get("release_date")),
                }
            )

            if created:
                movie.genres.set(genre_list)
                imported += 1

        return Response({"message": "Upcoming import finished", "imported": imported})


# 영화 목록
class MovieListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Movie.objects.all().order_by("-release_date")[:20]
        serializer = MovieResponseSerializer(qs, many=True)
        return Response(serializer.data)


# 영화 상세
class MovieDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieResponseSerializer(movie)
        return Response(serializer.data)


# 영화 검색
class MovieSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        q = request.GET.get("q", "")

        if not q:
            return Response([], status=200)

        qs = Movie.objects.filter(
            Q(title__icontains=q) | Q(original_title__icontains=q)
        ).distinct()

        serializer = MovieResponseSerializer(qs, many=True)
        return Response(serializer.data)


# Featured Movie 조회
class FeaturedMovieView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = FeaturedMovie.objects.select_related("movie").order_by("priority")[:10]
        serializer = FeaturedMovieSerializer(qs, many=True)
        return Response(serializer.data)


class TMDBPopularImportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        TMDB_KEY = settings.TMDB_API_KEY
        BASE_URL = "https://api.themoviedb.org/3/movie/top_rated"

        imported = 0
        featured_created = 0
        pages = 10  # Popular 200

        for page in range(1, pages + 1):
            url = f"{BASE_URL}?api_key={TMDB_KEY}&language=ko-KR&page={page}"
            res = requests.get(url)

            try:
                data = res.json()
            except:
                continue

            results = data.get("results", [])
            if not results:
                continue

            # popular 1페이지일 때만 → FeaturedMovie 등록
            is_feature_page = (page == 1)

            for idx, item in enumerate(results):
                tmdb_id = item.get("id")

                # 장르 매핑
                genre_list = get_or_create_genres(item.get("genre_ids", []))

                # Movie 저장
                movie, created = Movie.objects.get_or_create(
                    tmdb_id=tmdb_id,
                    defaults={
                        "title": item.get("title") or "",
                        "original_title": item.get("original_title"),
                        "overview": item.get("overview") or "",
                        "poster_path": item.get("poster_path"),
                        "backdrops": item.get("backdrop_path"),
                        "release_date": safe_date(item.get("release_date")),
                        "tmdb_rating": item.get("vote_average"),
                    }
                )

                if created:
                    movie.genres.set(genre_list)
                    imported += 1

                # 1페이지 결과만 FeaturedMovie 처리
                if is_feature_page:
                    featured, f_created = FeaturedMovie.objects.get_or_create(
                        movie=movie,
                        defaults={"priority": idx + 1}
                    )

                    # 기존 FeaturedMovie가 있으면 priority 업데이트
                    if not f_created:
                        featured.priority = idx + 1
                        featured.save()

                    if f_created:
                        featured_created += 1

        return Response({
            "message": "Popular movies imported & featured updated",
            "imported_movies": imported,
            "featured_created": featured_created,
            "featured_updated": 20 - featured_created,
            "pages_loaded": pages,
        })

