from django.apps import AppConfig

class RecommendConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recommend"

    def ready(self):
        # 서버 시작 시 임베딩 캐시 생성
        try:
            # from .services.semantic import preload_movie_embeddings
            # preload_movie_embeddings()
            pass
        except Exception as e:
            # 로컬 개발 중에는 실패해도 서버는 떠야 하니까 print만
            print("[Recommend] preload_movie_embeddings failed:", e)
