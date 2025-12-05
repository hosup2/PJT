from django.urls import path
from .views import TMDBImportView

urlpatterns = [
    path('import/', TMDBImportView.as_view()),
]
