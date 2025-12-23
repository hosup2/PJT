import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status

from .models import Movie, Genre, FeaturedMovie, MovieRating, HeroMovie
from .serializers import MovieResponseSerializer, FeaturedMovieSerializer
from .serializers import MovieRatingSerializer, HeroMovieSerializer

from .models import Actor, Director, Cast, CuratedLifeMovie
from .serializers import MovieDetailSerializer, LifeMovieSerializer
from .tmdb import fetch_movie_credits

# TMDB 날짜 안전 파서
def safe_date(value):
    return value if value else None

# TMDB 장르 처리 함수
def get_or_create_genres(genre_ids):
    return Genre.objects.filter(id__in=genre_ids)

class TMDBGenreSyncView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        url = "https://api.themoviedb.org/3/genre/movie/list"
        params = {
            "api_key": settings.TMDB_API_KEY,
            "language": "ko-KR",
        }

        res = requests.get(url, params=params)
        data = res.json()

        genres = data.get("genres", [])
        created, updated = 0, 0

        for g in genres:
            genre, is_created = Genre.objects.update_or_create(
                id=g["id"],
                defaults={"name": g["name"]}
            )
            if is_created:
                created += 1
            else:
                updated += 1

        return Response({
            "total": len(genres),
            "created": created,
            "updated": updated,
        })

class TMDBImportView(APIView):
    permission_classes = [IsAdminUser]

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
        search_query = request.query_params.get("search")
        if search_query:
            qs = Movie.objects.filter(title__icontains=search_query).order_by("-release_date")[:20]
        else:
            qs = Movie.objects.all().order_by("-release_date")[:41]
        
        # ⭐ context에 request 전달 (is_liked 계산을 위해)
        serializer = MovieResponseSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

class MovieSearchView(APIView):
    """
    우리 DB에 저장된 영화 검색
    """
    def get(self, request):
        query = request.query_params.get("q", "").strip()

        if not query:
            return Response([])

        qs = (
            Movie.objects
            .filter(title__icontains=query)
            .order_by("-tmdb_rating")[:10]
        )

        data = [
            {
                "id": movie.id,
                "title": movie.title,
                "poster_path": movie.poster_path,
                "release_date": movie.release_date,
            }
            for movie in qs
        ]

        return Response(data)



# Featured Movie 조회
class FeaturedMovieView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = FeaturedMovie.objects.select_related("movie").order_by("priority")[:20]
        serializer = FeaturedMovieSerializer(qs, many=True, context={'request': request})
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

class TMDBPopularPageImportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, page):
        TMDB_KEY = settings.TMDB_API_KEY
        BASE_URL = "https://api.themoviedb.org/3/movie/popular"

        if page < 1 or page > 500:
            return Response(
                {"error": "page must be between 1 and 500"},
                status=400
            )

        url = f"{BASE_URL}?api_key={TMDB_KEY}&language=ko-KR&page={page}"
        res = requests.get(url)
        data = res.json()

        movies = data.get("results", [])
        imported = 0
        skipped = 0

        for item in movies:
            movie, created = Movie.objects.get_or_create(
                tmdb_id=item["id"],
                defaults={
                    "title": item.get("title"),
                    "original_title": item.get("original_title"),
                    "overview": item.get("overview") or "",
                    "poster_path": item.get("poster_path"),
                    "backdrops": item.get("backdrop_path"),
                    "release_date": item.get("release_date") or None,
                    "tmdb_rating": item.get("vote_average"),
                }
            )

            if created:
                imported += 1
            else:
                skipped += 1

        return Response({
            "requested_page": page,
            "movies_in_page": len(movies),
            "imported": imported,
            "skipped": skipped,
            "message": f"Popular page {page} imported successfully"
        })


class MovieRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        
        rating_value = request.data.get("rating")
        comment_value = request.data.get("comment", "")
        
        if rating_value is None:
            return Response(
                {"error": "Rating is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        rating_obj, created = MovieRating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={
                'rating': rating_value,
                'comment': comment_value,
            }
        )

        serializer = MovieRatingSerializer(rating_obj)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)


class MovieRatingDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, movie_id, rating_id):
        """특정 리뷰 수정"""
        rating = get_object_or_404(
            MovieRating,
            id=rating_id,
            movie_id=movie_id,
            user=request.user
        )
        
        rating_value = request.data.get('rating')
        comment_value = request.data.get('comment')
        
        # 별점이 제공되면 업데이트
        if rating_value is not None:
            rating.rating = rating_value
        
        # 댓글이 제공되면 업데이트
        if comment_value is not None:
            rating.comment = comment_value
            
        rating.save()
        
        serializer = MovieRatingSerializer(rating)
        return Response(serializer.data)
    
    def delete(self, request, movie_id, rating_id):
        """특정 리뷰 삭제"""
        rating = get_object_or_404(
            MovieRating,
            id=rating_id,
            movie_id=movie_id,
            user=request.user
        )
        rating.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MovieRatingListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        ratings = MovieRating.objects.filter(movie=movie).select_related("user")

        serializer = MovieRatingSerializer(ratings, many=True)
        return Response(serializer.data)
    

class HeroMovieListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        heroes = HeroMovie.objects.filter(is_active=True).order_by("priority")[:5]
        serializer = HeroMovieSerializer(heroes, many=True, context={'request': request})
        return Response(serializer.data)

def fetch_tmdb_movie_detail(tmdb_id):
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
        params = {
            "api_key": settings.TMDB_API_KEY,
            "language": "ko-KR",
        }
        res = requests.get(url, params=params)
        return res.json()

class MovieDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)

        # ⭐ cast 정보 없으면 TMDB에서 가져오기
        if not movie.casts.exists():
            try:
                credits = fetch_movie_credits(movie.tmdb_id, language="ko-KR")

                # 감독
                crew = credits.get("crew", [])
                director_item = next(
                    (c for c in crew if c.get("job") == "Director"),
                    None
                )

                if director_item:
                    director, _ = Director.objects.get_or_create(
                        tmdb_id=director_item["id"],
                        defaults={
                            "name": director_item.get("name", ""),
                            "profile_path": director_item.get("profile_path"),
                        },
                    )
                    movie.director = director
                    movie.save(update_fields=["director"])
                    
                casts = credits.get("cast", [])

                # 출연진 + 배역
                for item in casts[:10]:
                    actor, _ = Actor.objects.get_or_create(
                        tmdb_id=item["id"],
                        defaults={
                            "name": item.get("name", ""),
                            "profile_path": item.get("profile_path"),
                        }
                    )

                    Cast.objects.get_or_create(
                        movie=movie,
                        actor=actor,
                        defaults={
                            "character": item.get("character", ""),
                            "order": item.get("order", 0),
                        }
                    )


            except Exception as e:
                print("TMDB credits fetch failed:", e)

        # ⭐ serializer에서 casts 내려줌
        movie = Movie.objects.prefetch_related(
            "casts__actor",
            "genres",
            "ratings__user",
        ).get(id=movie_id)

        serializer = MovieResponseSerializer(
            movie,
            context={"request": request}
        )
        return Response(serializer.data)

# movies/views.py
class LifeMovieCurationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = CuratedLifeMovie.objects.select_related(
            "user", "movie"
        )[:3]   # 인증회원 2명만

        serializer = LifeMovieSerializer(qs, many=True)
        return Response(serializer.data)
