from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from .models import Post, Comment
from .serializers import (
    PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer,
    CommentSerializer
)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    작성자만 수정/삭제 가능, 읽기는 모두 가능
    """
    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 쓰기 권한은 작성자에게만 허용
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """게시글 ViewSet"""
    queryset = Post.objects.select_related('author').prefetch_related('comments__author').all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer
    
    def get_permissions(self):
        """
        - list, retrieve: 모두 가능
        - create (Post), comments (create Comment), delete_comment: 인증 필요
        - update, partial_update, destroy (Post): 인증 + 작성자만
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action in ['create', 'comments', 'delete_comment']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        """게시글 작성자 자동 설정"""
        serializer.save(author=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        """게시글 조회시 조회수 증가"""
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'],
            permission_classes=[permissions.IsAuthenticated],
            authentication_classes=[JWTAuthentication])
    def comments(self, request, pk=None):
        """댓글 작성"""
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'],
            permission_classes=[permissions.IsAuthenticated],
            authentication_classes=[JWTAuthentication],
            url_path='comments/(?P<comment_id>[^/.]+)')
    def delete_comment(self, request, pk=None, comment_id=None):
        """댓글 삭제"""
        try:
            comment = Comment.objects.get(id=comment_id, post_id=pk)
            if comment.author != request.user:
                return Response(
                    {'error': '본인의 댓글만 삭제할 수 있습니다.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response(
                {'error': '댓글을 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )


from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer

class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.filter(is_active=True)
    serializer_class = ChatRoomSerializer

    def create(self, request, *args, **kwargs):
        movie_id = request.data.get('movie_id')
        if not movie_id:
            return Response({'error': 'movie_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 있으면 가져오고, 없으면 생성
            room, created = ChatRoom.objects.get_or_create(movie_id=movie_id)
            serializer = self.get_serializer(room)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def active_rooms(self, request):
        """영화별 활성 채팅방 목록"""
        rooms = self.queryset.select_related('movie').all()
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """특정 채팅방의 메시지 내역"""
        room = self.get_object()
        messages = room.messages.select_related('user').all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

