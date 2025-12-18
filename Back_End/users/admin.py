from django.contrib import admin
from .models import FavoriteMovie, WatchedMovie, UserPreference

admin.site.register(FavoriteMovie)
admin.site.register(WatchedMovie)
admin.site.register(UserPreference)
