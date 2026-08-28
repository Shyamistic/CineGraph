"""Embedding provider with an honest fallback.

Real semantic vectors come from ``gemini-embedding-001`` on Vertex. When that is
unreachable we fall back to a deterministic hashed vector so semantic search
still returns *something* offline — but the source is always reported, because a
hashed vector does not carry real semantics and results should not be presented
as if it does.
"""

from __future__ import annotations

import hashlib
import math

from app.config import settings
from app.services import vertex

Vector = list[float]


def hashed_embedding(text: str, dims: int | None = None) -> Vector:
    """Deterministic pseudo-embedding. Lexical overlap only, no semantics."""
    dims = dims or settings.embedding_dims
    vec = [0.0] * dims
    tokens = [t.lower() for t in text.replace("\n", " ").split() if t]
    if not tokens:
        return vec
    for i, token in enumerate(tokens):
        digest = hashlib.sha256(f"{token}:{i}".encode()).digest()
        for j in range(min(32, dims)):
            vec[(i * 13 + j) % dims] += (digest[j] - 128) / 128.0
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def embed_text(text: str) -> tuple[Vector, str]:
    """Return ``(vector, source)`` where source is ``"vertex"`` or ``"hash"``."""
    if settings.vertex_enabled:
        vector = vertex.embed(text)
        if vector:
            return _fit(vector), "vertex"
    return hashed_embedding(text), "hash"


def _fit(vector: Vector) -> Vector:
    """Pad or truncate so every stored vector matches the table dimensionality."""
    dims = settings.embedding_dims
    if len(vector) == dims:
        return vector
    if len(vector) > dims:
        return vector[:dims]
    return vector + [0.0] * (dims - len(vector))
