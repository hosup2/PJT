from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from movies.models import Movie, Genre
from users.models import UserPreference, WatchedMovie


User = get_user_model()


class Command(BaseCommand):
    help = "Seed example data for recommendation system"

    def handle(self, *args, **options):
        self.stdout.write("🌱 Seeding example data...")

        # 1️⃣ Genre 생성
        genres = {
            "Action": Genre.objects.get_or_create(name="Action")[0],
            "SF": Genre.objects.get_or_create(name="SF")[0],
            "Drama": Genre.objects.get_or_create(name="Drama")[0],
            "Thriller": Genre.objects.get_or_create(name="Thriller")[0],
        }

        # 2️⃣ Movie 생성
        movies_data = [
            ("Interstellar", ["SF", "Drama"]),
            ("Inception", ["SF", "Action", "Thriller"]),
            ("The Matrix", ["SF", "Action"]),
            ("Mad Max: Fury Road", ["Action"]),
            ("Tenet", ["SF", "Action"]),
            ("The Dark Knight", ["Action", "Drama"]),
            ("Arrival", ["SF", "Drama"]),
            ("John Wick", ["Action", "Thriller"]),
        ]

        movie_objs = []
        for idx, (title, genre_names) in enumerate(movies_data, start=1):
            movie, created = Movie.objects.get_or_create(
                tmdb_id=1000 + idx,
                defaults={
                    "title": title,
                    "overview": f"{title} overview example.",
                    "poster_path": "",
                }
            )
            movie.genres.set([genres[g] for g in genre_names])
            movie_objs.append(movie)

        # 3️⃣ User 생성
        user, _ = User.objects.get_or_create(
            username="testuser",
            defaults={"email": "testuser@example.com"}
        )
        if not user.password:
            user.set_password("test1234")
            user.save()

        # 4️⃣ UserPreference (Action, SF 선호)
        pref, _ = UserPreference.objects.get_or_create(user=user)
        pref.favorite_genres.set([genres["Action"], genres["SF"]])

        # 5️⃣ WatchedMovie (Interstellar, Inception 시청 처리)
        WatchedMovie.objects.get_or_create(user=user, movie=movie_objs[0])
        WatchedMovie.objects.get_or_create(user=user, movie=movie_objs[1])

        self.stdout.write(self.style.SUCCESS("✅ Seed data inserted successfully!"))
        self.stdout.write("👉 testuser / test1234 로 테스트 가능")
