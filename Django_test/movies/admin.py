from django.contrib import admin
from .models import Movie, FeaturedMovie, Genre


@admin.register(FeaturedMovie)

class FeaturedMovieAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "priority", "created_at")
    list_editable = ("priority",)     # ⭐ 리스트에서 바로 순서 수정
    ordering = ("priority",)
    autocomplete_fields = ("movie",)  # 영화 검색으로 선택 가능

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "release_date", "tmdb_rating")
    search_fields = ("title", "original_title")
    list_filter = ("release_date",)
