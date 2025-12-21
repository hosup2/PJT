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

from .models import Actor, Director
from .serializers import MovieDetailSerializer
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
        # ⭐ context에 request 전달 (is_liked 계산을 위해)
        serializer = MovieResponseSerializer(qs, many=True, context={'request': request})
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

        serializer = MovieResponseSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)


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
        
        # 받은 데이터 검증
        rating_value = request.data.get("rating")
        comment_value = request.data.get("comment", "")
        
        # rating이 없으면 에러 반환 (별점은 필수)
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

    def delete(self, request, movie_id):
        rating_id = request.data.get('rating_id')
        
        if not rating_id:
            return Response(
                {"error": "rating_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        rating = get_object_or_404(
            MovieRating, 
            id=rating_id,
            movie_id=movie_id,
            user=request.user
        )
        rating.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ⭐ 새로운 뷰: 개별 리뷰 수정
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
        
        rating.rating = request.data.get('rating', rating.rating)
        rating.comment = request.data.get('comment', rating.comment)
        rating.save()
        
        serializer = MovieRatingSerializer(rating)
        return Response(serializer.data)


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
    """
    GET /api/v1/movies/<movie_id>/
    - DB에 director/actors가 있으면 DB에서 반환
    - 없으면 TMDB credits 호출해서 저장 후 반환
    """

    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)

        # ✅ 이미 DB에 있으면 DB 데이터로 바로 반환
        if movie.director is not None and movie.actors.exists():
            serializer = MovieDetailSerializer(movie)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # ❌ 없으면 TMDB에서 가져와서 DB에 저장
        try:
            credits = fetch_movie_credits(movie.tmdb_id, language="ko-KR")
        except Exception as e:
            # TMDB 실패 시에도 영화 기본정보는 반환하고 싶으면 이렇게 처리 가능
            serializer = MovieDetailSerializer(movie)
            return Response(
                {
                    "movie": serializer.data,
                    "credits_error": str(e),
                },
                status=status.HTTP_200_OK,
            )

        crew = credits.get("crew", [])
        cast = credits.get("cast", [])

        # 감독 찾기 (job == "Director")
        director_item = next((c for c in crew if c.get("job") == "Director"), None)

        if director_item:
            director, _ = Director.objects.get_or_create(
                tmdb_id=director_item["id"],
                defaults={
                    "name": director_item.get("name", ""),
                    "profile_path": director_item.get("profile_path"),
                },
            )
            movie.director = director

        # 출연진 상위 5명만 저장 (원하면 숫자 조절)
        actor_objs = []
        for item in cast[:5]:
            actor, _ = Actor.objects.get_or_create(
                tmdb_id=item["id"],
                defaults={
                    "name": item.get("name", ""),
                    "profile_path": item.get("profile_path"),
                },
            )
            actor_objs.append(actor)

        movie.save()
        if actor_objs:
            movie.actors.set(actor_objs)

        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)


# # 영화 디테일 요청
# class MovieDetailView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, movie_id):
#         movie = get_object_or_404(Movie, id=movie_id)

#         # 🔑 디테일 정보가 충분한지 판단
#         need_tmdb_fetch = (
#             movie.runtime is None or
#             movie.overview == "" or
#             movie.genres.count() == 0
#         )

#         if need_tmdb_fetch:
#             tmdb_data = fetch_tmdb_movie_detail(movie.tmdb_id)

#             # DB 업데이트 (필요한 필드만)
#             movie.runtime = tmdb_data.get("runtime")
#             movie.overview = tmdb_data.get("overview") or movie.overview
#             movie.save()

#             # 장르 동기화
#             genres = []
#             for g in tmdb_data.get("genres", []):
#                 genre, _ = Genre.objects.get_or_create(
#                     id=g["id"],
#                     defaults={"name": g["name"]}
#                 )
#                 genres.append(genre)
#             movie.genres.set(genres)

#         # ⭐ context에 request 전달 (is_liked 계산을 위해)
#         serializer = MovieResponseSerializer(movie, context={'request': request})
#         return Response(serializer.data)