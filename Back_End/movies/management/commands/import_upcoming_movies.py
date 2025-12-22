# movies/management/commands/import_upcoming_2026_movies.py

import time
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from movies.models import Movie, Genre


TMDB_BASE = "https://api.themoviedb.org/3"


class Command(BaseCommand):
    help = "Import upcoming movies (release date <= 2026) from TMDB"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🎬 Import upcoming movies (<= 2026) started"))

        total_saved = 0

        # 2025~2026 범위 (미래 개봉작은 미리 등록되는 경우가 많음)
        for page in range(67, 501):
            self.stdout.write(f"📄 Discover page {page}")

            data = self.fetch_discover(page)
            if not data or "results" not in data:
                break

            for item in data["results"]:
                tmdb_id = item["id"]

                if Movie.objects.filter(tmdb_id=tmdb_id).exists():
                    continue

                saved = self.save_movie(item)
                if saved:
                    total_saved += 1
                    self.stdout.write(self.style.SUCCESS(
                        f"  ✔ Saved: {item.get('title')}"
                    ))

                time.sleep(0.05)  # discover만 쓰니 더 빠르게 가능


            if page >= data.get("total_pages", 1):
                break

        self.stdout.write(self.style.SUCCESS(
            f"✅ Import finished. Total saved: {total_saved}"
        ))

    # --------------------
    # TMDB API FUNCTIONS
    # --------------------

    def fetch_discover(self, page):
        params = {
            "api_key": settings.TMDB_API_KEY,
            "language": "ko-KR",
            "page": page,
            "sort_by": "popularity.desc",
            "primary_release_date.gte": "2025-01-01",
            "primary_release_date.lte": "2027-12-31",
            "include_adult": False,
        }
        r = requests.get(f"{TMDB_BASE}/discover/movie", params=params)
        if r.status_code != 200:
            self.stderr.write(f"❌ Discover failed: {r.status_code}")
            return None
        return r.json()

    def fetch_movie_detail(self, tmdb_id):
        params = {
            "api_key": settings.TMDB_API_KEY,
            "language": "ko-KR",
        }
        r = requests.get(f"{TMDB_BASE}/movie/{tmdb_id}", params=params)
        if r.status_code != 200:
            return None
        return r.json()

    # --------------------
    # SAVE LOGIC
    # --------------------

    def save_movie(self, item):
        # discover 결과에는 이미 개봉된 영화도 섞일 수 있음
        if item.get("release_date"):
            from datetime import date
            if date.fromisoformat(item["release_date"]) < date.today():
                return False

        # overview 없는 건 저장 안 할 수도 있음 (선택)
        # 추천만 목적이면 없어도 OK
        # if not item.get("overview"):
        #     return False

        movie = Movie.objects.create(
            tmdb_id=item["id"],
            title=item.get("title"),
            original_title=item.get("original_title"),
            overview=item.get("overview", ""),  # 비워도 됨
            release_date=item.get("release_date") or None,
            tmdb_rating=item.get("vote_average"),
            poster_path=item.get("poster_path"),
            backdrops=item.get("backdrop_path"),
        )

        for g in item.get("genre_ids", []):
            genre, _ = Genre.objects.get_or_create(id=g)
            movie.genres.add(genre)

        return True

