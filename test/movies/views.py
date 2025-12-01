from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import get_upcoming_movies

@api_view(['GET'])
def upcoming_movies(request):
    page = request.GET.get("page", 1)
    data = get_upcoming_movies(page)
    return Response(data)
