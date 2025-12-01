from rest_framework import serializers
from .models import MovieCache

class MovieCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieCache
        fields = "__all__"
