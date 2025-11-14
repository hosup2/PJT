from django.urls import path
from movies import views

urlpatterns = [
    path('movies/',views.movie_list),
    path('movies/<int:movies_pk>/',views.movie_detail),
    path('actors/',views.actors_list),
    path('actors/<int:actors_pk>/',views.actors_detail),
    path('reviews/',views.reviews_list),
    path('reviews/<int:movies_pk>/create/',views.reviews_create),  
    path('reviews/<int:reviews_pk>/',views.reviews_detail),
]
