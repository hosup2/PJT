from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth import get_user_model
User = get_user_model()

from .services.logic import run_chatbot

from .models import ChatSession, ChatMessage
from .serializers import ChatRequestSerializer, ChatSessionSerializer
from .services.logic import update_session_summary

from recommend.models import MovieFeedback
from movies.models import Movie

class ChatRecommendView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):

        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.validated_data["message"]
        session_id = serializer.validated_data.get("session_id")

        # 1️⃣ 세션 가져오거나 생성
        if session_id:
            session = ChatSession.objects.filter(
                id=session_id,
                user=request.user
            ).first()
            if not session:
                return Response(
                    {"detail": "Invalid session_id"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            session = ChatSession.objects.create(
                user=request.user,
                title="새 대화"
            )

        # 2️⃣ 사용자 메시지 저장
        ChatMessage.objects.create(
            session=session,
            role="user",
            content=message
        )

        # user message 저장 직후
        if session.title in ["", "새 대화", "MIA CHAT"]:
            session.title = message.strip()[:30]
            session.save(update_fields=["title"])

        # run_chatbot
        result = run_chatbot(message, session)

        # assistant 저장
        ChatMessage.objects.create(session=session, role="assistant", content=result["answer"])

        # summary 갱신
        update_session_summary(session)

        # 4️⃣ AI 메시지 저장

        # AI 응답 저장 후
        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=result["answer"]
        )

        update_session_summary(session)


        return Response({
            "session_id": session.id,
            "answer": result["answer"],
            "movies": result["movies"],
        }, status=status.HTTP_200_OK)


class ChatSessionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        session = ChatSession.objects.filter(
            id=session_id,
            user=request.user
        ).first()

        if not session:
            return Response(status=404)

        serializer = ChatSessionSerializer(session)
        return Response(serializer.data)
    
    def delete(self, request, session_id):
        ChatSession.objects.filter(
            id=session_id,
            user=request.user
        ).delete()
        return Response(status=204)

class ChatSessionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = ChatSession.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data)

class MovieFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        movie_id = request.data.get("movie_id")
        feedback = request.data.get("feedback")  # "like" or "dislike"

        if feedback not in ["like", "dislike"]:
            return Response({"error": "Invalid feedback"}, status=400)

        movie = Movie.objects.filter(id=movie_id).first()
        if not movie:
            return Response({"error": "Movie not found"}, status=404)

        obj, _ = MovieFeedback.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={"feedback": feedback},
        )

        return Response({"status": "ok", "feedback": obj.feedback})
