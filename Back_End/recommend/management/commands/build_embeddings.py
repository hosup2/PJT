from django.core.management.base import BaseCommand
import pickle
from pathlib import Path

from recommend.services.semantic import preload_movie_embeddings, _cache


class Command(BaseCommand):
    help = "Build and save movie embeddings"

    def handle(self, *args, **options):
        self.stdout.write("🔄 Building movie embeddings...")
        count = preload_movie_embeddings(force=True)

        path = Path("recommend/services/movie_embeddings.pkl")
        with open(path, "wb") as f:
            pickle.dump(_cache, f)

        self.stdout.write(self.style.SUCCESS(
            f"✅ Saved {count} embeddings to {path}"
        ))
