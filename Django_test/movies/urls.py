from django.urls import path
from .views import TMDBImportView, MovieDetailView, MovieListView, MovieSearchView
from .views import FeaturedMovieView, TMDBPopularImportView, MovieRatingListView, MovieRatingView
from .views import TMDBPopularPageImportView, TMDBMovieDetailView

urlpatterns = [
    path("import/", TMDBImportView.as_view()),          # 관리자
    path("", MovieListView.as_view()),                  # 영화 목록
    path("<int:movie_id>/", MovieDetailView.as_view()), # 영화 상세
    path("search/", MovieSearchView.as_view()),         # 영화 검색
    path("featured/", FeaturedMovieView.as_view(), name="featured-movies"), # 대표 영화
    path("popular/", TMDBPopularImportView.as_view()),
    path("<int:movie_id>/rating/", MovieRatingView.as_view()),
    path("<int:movie_id>/ratings/", MovieRatingListView.as_view()),
    path("popular/import/<int:page>/", TMDBPopularPageImportView.as_view()),
    path("<int:movie_id>/tmdb-detail/", TMDBMovieDetailView.as_view()),

]