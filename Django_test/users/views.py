from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserPreference
from .serializers import UserPreferenceSerializer

class UserPreferenceView(APIView):
    def post(self, request):
        prefs, created = UserPreference.objects.get_or_create(
            user=request.user
        )
        serializer = UserPreferenceSerializer(prefs, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
