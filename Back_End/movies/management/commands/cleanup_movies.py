from django.core.management.base import BaseCommand
from django.db.models import Q
from movies.models import Movie

class Command(BaseCommand):
    help = "Delete movies without overview or poster or backdrop"

    def handle(self, *args, **options):
        qs = Movie.objects.filter(
            Q(overview__isnull=True) | Q(overview="") |
            Q(poster_path__isnull=True) | Q(poster_path="") |
            Q(backdrops__isnull=True) | Q(backdrops="")
        )

        count = qs.count()
        self.stdout.write(f"🧹 Movies to delete: {count}")

        if count == 0:
            return

        deleted, _ = qs.delete()
        self.stdout.write(self.style.SUCCESS(f"✅ Deleted {deleted} movies"))
