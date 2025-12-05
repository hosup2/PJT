from movies.models import Movie
from users.models import UserPreference, WatchedMovie

def recommend_movies_for_user(user):

    prefs = UserPreference.objects.get(user=user)
    favorite_genres = prefs.favorite_genres.all()

    qs = Movie.objects.filter(genres__in=favorite_genres).distinct()

    watched = WatchedMovie.objects.filter(user=user).values_list("movie_id", flat=True)
    qs = qs.exclude(id__in=watched)

    return qs[:20]
