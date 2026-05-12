from pathlib import Path

import cv2
import numpy as np


EMBEDDING_DIM = 128
EMBEDDING_BYTES = EMBEDDING_DIM * np.dtype(np.float32).itemsize
COSINE_THRESHOLD = 0.363


class FaceRecognizer:
    def __init__(self, model_path: str | Path):
        self._model = cv2.FaceRecognizerSF.create(str(model_path), "")

    def embed(self, frame_bgr: np.ndarray, face_row: np.ndarray) -> np.ndarray:
        """Return a (1, 128) float32 embedding for one detector face row."""
        aligned = self._model.alignCrop(frame_bgr, face_row)
        feat = self._model.feature(aligned)
        return feat.astype(np.float32)

    @staticmethod
    def to_bytes(embedding: np.ndarray) -> bytes:
        embedding = np.asarray(embedding, dtype=np.float32)
        if embedding.shape != (1, EMBEDDING_DIM):
            raise ValueError(
                f"embedding must have shape (1, {EMBEDDING_DIM}), got {embedding.shape}"
            )
        return embedding.tobytes()

    @staticmethod
    def from_bytes(blob: bytes) -> np.ndarray:
        if len(blob) != EMBEDDING_BYTES:
            raise ValueError(f"embedding blob must be {EMBEDDING_BYTES} bytes, got {len(blob)}")
        return np.frombuffer(blob, dtype=np.float32).reshape(1, EMBEDDING_DIM)

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        return float(self._model.match(a, b, cv2.FaceRecognizerSF_FR_COSINE))


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    a_flat = a.flatten()
    b_flat = b.flatten()
    denom = np.linalg.norm(a_flat) * np.linalg.norm(b_flat)
    if denom == 0:
        return 0.0
    return float(np.dot(a_flat, b_flat) / denom)

