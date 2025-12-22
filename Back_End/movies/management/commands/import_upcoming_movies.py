import time
import requests
import re
from datetime import date
from django.core.management.base import BaseCommand
from django.conf import settings
from movies.models import Movie, Genre

TMDB_BASE = "https://api.themoviedb.org/3"

def has_korean(text: str) -> bool:
    return bool(re.search(r"[가-힣]", text))

class Command(BaseCommand):
    help = "Import filtered upcoming movies (<= 2026) from TMDB"

    MIN_VOTE_AVERAGE = 5.5
    MIN_VOTE_COUNT = 50

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🎬 Import filtered upcoming movies started"))

        total_saved = 0
        skipped = 0

        for page in range(501, 1000):
            self.stdout.write(f"📄 Discover page {page}")

            data = self.fetch_discover(page)
            if not data or "results" not in data:
                break

            for item in data["results"]:
                tmdb_id = item["id"]

                if Movie.objects.filter(tmdb_id=tmdb_id).exists():
                    continue

                if not self.is_valid_movie(item):
                    skipped += 1
                    continue

                saved = self.save_movie(item)
                if saved:
                    total_saved += 1
                    self.stdout.write(self.style.SUCCESS(
                        f"  ✔ Saved: {item.get('title')}"
                    ))

                time.sleep(0.05)

            if page >= data.get("total_pages", 1):
                break

        self.stdout.write(self.style.SUCCESS(
            f"✅ Finished | saved={total_saved}, skipped={skipped}"
        ))

    # --------------------
    # TMDB API
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

    # --------------------
    # FILTER LOGIC
    # --------------------
    
    def is_valid_movie(self, item):
        title = item.get("title")
        release_date = item.get("release_date")
        poster = item.get("poster_path")
        vote_avg = item.get("vote_average", 0)
        vote_cnt = item.get("vote_count", 0)

        # 제목 없음
        if not title:
            return False

        # 포스터 없음
        if not poster:
            return False
        
        if not has_korean(title):
            return False
        
        # # 개봉일 없음 or 이미 개봉
        # if not release_date:
        #     return False
        # if date.fromisoformat(release_date) < date.today():
        #     return False

        # 저품질 필터
        if vote_avg < self.MIN_VOTE_AVERAGE:
            return False
        if vote_cnt < self.MIN_VOTE_COUNT:
            return False

        return True

    # --------------------
    # SAVE LOGIC
    # --------------------

    def save_movie(self, item):
        movie = Movie.objects.create(
            tmdb_id=item["id"],
            title=item.get("title"),
            original_title=item.get("original_title"),
            overview=item.get("overview", ""),
            release_date=item.get("release_date"),
            tmdb_rating=item.get("vote_average"),
            poster_path=item.get("poster_path"),
            backdrops=item.get("backdrop_path"),
        )

        for gid in item.get("genre_ids", []):
            genre, _ = Genre.objects.get_or_create(id=gid)
            movie.genres.add(genre)

        return True
