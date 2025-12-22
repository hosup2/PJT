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

        for page in range(1, 501):
            self.stdout.write(f"📄 Discover page {page}")

            data = self.fetch_discover(page)
            if not data or "results" not in data:
                break

            for item in data["results"]:
                saved = self.save_movie_from_discover(item)
                if saved:
                    total_saved += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"✔ Saved: {item.get('title')}")
                    )

                time.sleep(0.05)

            if page >= data.get("total_pages", 1):
                break

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
        if Movie.objects.filter(tmdb_id=item["id"]).exists():
            return False

        if item.get("release_date"):
            if date.fromisoformat(item["release_date"]) < date.today():
                return False

        movie = Movie.objects.create(
            tmdb_id=item["id"],
            title=item.get("title"),
            original_title=item.get("original_title"),
            overview=item.get("overview", ""),
            release_date=item.get("release_date") or None,
            tmdb_rating=item.get("vote_average"),
            poster_path=item.get("poster_path"),
            backdrops=item.get("backdrop_path"),
            is_detail_fetched=False,
        )

        for gid in item.get("genre_ids", []):
            genre, _ = Genre.objects.get_or_create(id=gid)
            movie.genres.add(genre)

        return True
