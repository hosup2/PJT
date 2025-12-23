from django.contrib import admin
from .models import Post, Comment, ChatRoom, ChatMessage

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('movie', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('movie__title',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'message', 'created_at')
    list_filter = ('room', 'created_at')
    search_fields = ('message', 'user__username')
