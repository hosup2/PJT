# recommend/services/semantic.py

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Optional
import threading

import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
from pathlib import Path

from movies.models import Movie


MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

_lock = threading.Lock()
_model: Optional[SentenceTransformer] = None
_cache: Optional[list[tuple[int, np.ndarray]]] = None  # [(movie_id, vec)]
_loaded_count: int = 0


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def build_movie_text(movie: Movie) -> str:
    # ✅ 텍스트는 합쳐야 “분위기/감정” 같은 뉘앙스가 잘 잡힘
    genres = ", ".join(movie.genres.values_list("name", flat=True))
    year = movie.release_date.year if movie.release_date else ""
    overview = movie.overview or ""

    return (
        f"제목: {movie.title}\n"
        f"장르: {genres}\n"
        f"개봉: {year}\n"
        f"줄거리: {overview}\n"
    )
def load_cached_embeddings():
    global _cache, _loaded_count
    path = Path(__file__).parent / "movie_embeddings.pkl"

    if not path.exists():
        return False

    with open(path, "rb") as f:
        _cache = pickle.load(f)
        _loaded_count = len(_cache)

    return True

def preload_movie_embeddings(force: bool = False) -> int:
    """
    서버 시작 시 1회 호출 추천.
    force=True면 캐시 재생성
    """
    global _cache, _loaded_count

    if not force and load_cached_embeddings():
        return _loaded_count
    
    with _lock:
        if _cache is not None and not force:
            return _loaded_count

        model = _get_model()
        movies = list(Movie.objects.all().prefetch_related("genres"))

        texts = [build_movie_text(m) for m in movies]

        # normalize_embeddings=True -> 코사인 유사도 계산을 dot으로 바로 가능
        vecs = model.encode(texts, normalize_embeddings=True, batch_size=64, show_progress_bar=True)

        _cache = [(m.id, v.astype(np.float32)) for m, v in zip(movies, vecs)]
        _loaded_count = len(_cache)
        return _loaded_count


def semantic_topk(query: str, top_k: int = 30, candidate_ids: Optional[list[int]] = None) -> list[int]:
    """
    query와 의미적으로 가까운 영화 id top_k 반환
    candidate_ids가 있으면 그 범위 안에서만 검색(속도/정확도 향상)
    """
    if not query:
        return []

    # 캐시 없으면 즉시 생성(안전장치)
    if _cache is None:
        preload_movie_embeddings()

    model = _get_model()
    q = model.encode([query], normalize_embeddings=True)[0].astype(np.float32)

    # 후보 제한이 있으면 해당 id만 필터
    if candidate_ids:
        candidate_set = set(candidate_ids)
        pool = [(mid, vec) for (mid, vec) in _cache if mid in candidate_set]
    else:
        pool = _cache

    if not pool:
        return []

    # dot == cosine similarity (normalize_embeddings=True)
    scores = [(float(np.dot(q, vec)), mid) for (mid, vec) in pool]
    scores.sort(reverse=True, key=lambda x: x[0])

    return [mid for _, mid in scores[:top_k]]
