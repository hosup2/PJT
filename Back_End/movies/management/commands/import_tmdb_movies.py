from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import time
from datetime import date

from movies.models import Movie, Genre


TMDB_BASE = "https://api.themoviedb.org/3"


class Command(BaseCommand):
    help = "Import movies from TMDB discover API (shallow data only)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🎬 TMDB import started"))

        total_saved = 0
        page = 189
        total_pages = 189  # 초기값

        while page <= total_pages:
            self.stdout.write(f"📄 Discover page {page}")

            data = self.fetch_discover(page)
            if not data or "results" not in data:
                break

            total_pages = data.get("total_pages", 1)

            for item in data["results"]:
                saved = self.save_movie_from_discover(item)
                if saved:
                    total_saved += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"✔ Saved: {item.get('title')}")
                    )

                time.sleep(0.05)

            page += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Import finished. Total saved: {total_saved}"
        ))

    def fetch_discover(self, page):
        params = {
            "api_key": settings.TMDB_API_KEY,
            "language": "ko-KR",
            "page": page,
            "sort_by": "popularity.desc",
            "include_adult": False,
        }
        r = requests.get(f"{TMDB_BASE}/discover/movie", params=params)
        if r.status_code != 200:
            self.stderr.write(f"❌ Discover failed: {r.status_code}")
            return None
        return r.json()

    def save_movie_from_discover(self, item):
        # 중복 방지
        if Movie.objects.filter(tmdb_id=item["id"]).exists():
            return False

        # 🔞 성인 영화 필터
        if item.get("adult"):
            return False

        # 🇰🇷 국내 제목 없음
        if not item.get("title"):
            return False

        # 📝 줄거리 없음
        if not item.get("overview"):
            return False

        # 🖼️ 이미지 부족
        if not item.get("poster_path") or not item.get("backdrop_path"):
            return False

        # 🗑️ 저품질 필터
        if (item.get("vote_average") or 0) < 5.5:
            return False

        if (item.get("vote_count") or 0) < 50:
            return False

        # ⏳ 이미 개봉한 영화 제외 (선택)
        # if item.get("release_date"):
        #     if date.fromisoformat(item["release_date"]) < date.today():
        #         return False

        # ✅ 저장
        movie = Movie.objects.create(
            tmdb_id=item["id"],
            title=item.get("title"),
            original_title=item.get("original_title"),
            overview=item.get("overview"),
            release_date=item.get("release_date") or None,
            tmdb_rating=item.get("vote_average"),
            poster_path=item.get("poster_path"),
            backdrops=item.get("backdrop_path"),
        )

        for gid in item.get("genre_ids", []):
            genre, _ = Genre.objects.get_or_create(id=gid)
            movie.genres.add(genre)

        return True

