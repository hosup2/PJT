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

        # ⭐️⭐️ 핵심 추가 부분 ⭐️⭐️
        # 첫 번째 user 메시지면 세션 제목으로 설정
        if session.title == "새 대화":
            session.title = message[:30]  # 너무 길면 잘라줌
            session.save(update_fields=["title"])

        # 3️⃣ 챗봇 로직 실행 (대화 or 추천)
        result = run_chatbot(request.user, message, session)

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
