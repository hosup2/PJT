from django.urls import path
from movies import views

urlpatterns = [
    path('actors/',views.actors_list),
    path('actors/<int:actors_pk>/',views.actors_detail),
    path('movies/',views.movie_list),
    path('movies/<int:movies_pk>/',views.movie_detail),
    path('reviews/',views.review_list),
    path('reviews/<int:movies_pk>/create/',views.reviews_create),  
    path('reviews/<int:reviews_pk>/',views.review_detail),
    path('movies/search/', views.movie_search),
]
