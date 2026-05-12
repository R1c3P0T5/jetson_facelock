from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import cv2
import numpy as np

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from scripts.yunet_sface.detector import FaceDetector
from scripts.yunet_sface.model_files import (
    DEFAULT_DETECTOR_MODEL,
    DEFAULT_RECOGNIZER_MODEL,
    missing_model_paths,
    model_setup_hint,
)
from scripts.yunet_sface.recognizer import COSINE_THRESHOLD, FaceRecognizer, cosine
from scripts.yunet_sface.store import EmbeddingStore


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STORE = ROOT / "scripts/yunet_sface/store.pkl"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recognize faces with YuNet + SFace.")
    parser.add_argument("--camera", type=int, default=0, help="Camera index.")
    parser.add_argument("--store", type=Path, default=DEFAULT_STORE, help="Embedding store path.")
    parser.add_argument("--threshold", type=float, default=COSINE_THRESHOLD)
    parser.add_argument(
        "--no-live-panel",
        action="store_true",
        help="Disable the live embedding heatmap and comparison panel.",
    )
    parser.add_argument("--detector-model", type=Path, default=DEFAULT_DETECTOR_MODEL)
    parser.add_argument("--recognizer-model", type=Path, default=DEFAULT_RECOGNIZER_MODEL)
    return parser.parse_args()


def load_embeddings(store: EmbeddingStore, recognizer: FaceRecognizer) -> dict[str, np.ndarray]:
    return {key: recognizer.from_bytes(blob) for key, blob in store.all().items()}


def best_match(
    embedding: np.ndarray, candidates: dict[str, np.ndarray]
) -> tuple[str | None, float]:
    best_name = None
    best_score = float("-inf")
    for name, stored_embedding in candidates.items():
        score = cosine(embedding, stored_embedding)
        if score > best_score:
            best_name = name
            best_score = score
    return best_name, best_score


def all_scores(embedding: np.ndarray, candidates: dict[str, np.ndarray]) -> list[tuple[str, float]]:
    scores = [(name, cosine(embedding, stored)) for name, stored in candidates.items()]
    return sorted(scores, key=lambda item: item[1], reverse=True)


def largest_face_index(faces: np.ndarray) -> int:
    areas = faces[:, 2] * faces[:, 3]
    return int(np.argmax(areas))


def embedding_heatmap(embedding: np.ndarray, cell_size: int = 24) -> np.ndarray:
    grid = embedding.reshape(8, 16)
    min_value = float(np.min(grid))
    max_value = float(np.max(grid))
    if max_value == min_value:
        normalized = np.zeros_like(grid, dtype=np.uint8)
    else:
        normalized = ((grid - min_value) / (max_value - min_value) * 255).astype(np.uint8)

    heatmap = cv2.applyColorMap(normalized, cv2.COLORMAP_VIRIDIS)
    return cv2.resize(
        heatmap,
        (16 * cell_size, 8 * cell_size),
        interpolation=cv2.INTER_NEAREST,
    )


def score_color(score: float, threshold: float) -> tuple[int, int, int]:
    if score >= 0.5:
        return (80, 190, 80)
    if score >= threshold:
        return (70, 190, 220)
    return (90, 90, 220)


def live_panel(
    embedding: np.ndarray | None,
    scores: list[tuple[str, float]],
    threshold: float,
    width: int = 460,
) -> np.ndarray:
    panel = np.full((640, width, 3), 245, dtype=np.uint8)
    cv2.putText(
        panel,
        "Live embedding heatmap",
        (18, 34),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.74,
        (25, 25, 25),
        2,
        cv2.LINE_AA,
    )

    if embedding is None:
        cv2.putText(
            panel,
            "No face detected",
            (18, 95),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (80, 80, 80),
            2,
            cv2.LINE_AA,
        )
        return panel

    heatmap = embedding_heatmap(embedding)
    y0 = 56
    x0 = 18
    panel[y0 : y0 + heatmap.shape[0], x0 : x0 + heatmap.shape[1]] = heatmap

    y = y0 + heatmap.shape[0] + 46
    cv2.putText(
        panel,
        "Cosine compare",
        (18, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.74,
        (25, 25, 25),
        2,
        cv2.LINE_AA,
    )
    y += 34

    if not scores:
        cv2.putText(
            panel,
            "No stored embeddings",
            (18, y + 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (80, 80, 80),
            2,
            cv2.LINE_AA,
        )
        return panel

    bar_x = 140
    bar_w = width - bar_x - 28
    for name, score in scores[:8]:
        color = score_color(score, threshold)
        bar_len = int(max(0.0, min(score, 1.0)) * bar_w)
        cv2.putText(
            panel,
            name[:13],
            (18, y + 23),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.58,
            (35, 35, 35),
            2,
            cv2.LINE_AA,
        )
        cv2.rectangle(panel, (bar_x, y), (bar_x + bar_w, y + 28), (220, 220, 220), -1)
        cv2.rectangle(panel, (bar_x, y), (bar_x + bar_len, y + 28), color, -1)
        cv2.putText(
            panel,
            f"{score:.3f}",
            (bar_x + 8, y + 21),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.56,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        y += 42

    cv2.putText(
        panel,
        f"threshold {threshold:.3f}",
        (18, panel.shape[0] - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.56,
        (65, 65, 65),
        1,
        cv2.LINE_AA,
    )
    return panel


def draw_result(
    frame: np.ndarray,
    face: np.ndarray,
    label: str,
    score: float,
    color: tuple[int, int, int],
) -> None:
    x, y, w, h = face[:4].astype(int)
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    cv2.putText(
        frame,
        f"{label} {score:.3f}",
        (x, max(20, y - 8)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2,
        cv2.LINE_AA,
    )


def main() -> int:
    args = parse_args()
    missing_models = missing_model_paths([args.detector_model, args.recognizer_model])
    if missing_models:
        print(model_setup_hint(missing_models), file=sys.stderr)
        return 1

    detector = FaceDetector(args.detector_model)
    recognizer = FaceRecognizer(args.recognizer_model)
    store = EmbeddingStore(args.store)
    embeddings = load_embeddings(store, recognizer)

    if not embeddings:
        print(f"No embeddings found in {args.store}. 請先跑 register.py。")

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print(f"Could not open camera {args.camera}", file=sys.stderr)
        return 1

    last_time = time.perf_counter()
    fps = 0.0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Could not read frame from camera", file=sys.stderr)
                return 1

            now = time.perf_counter()
            elapsed = now - last_time
            last_time = now
            if elapsed > 0:
                fps = 0.9 * fps + 0.1 * (1.0 / elapsed) if fps else 1.0 / elapsed

            faces = detector.detect(frame)
            panel_embedding = None
            panel_scores: list[tuple[str, float]] = []
            if faces is not None and len(faces) > 0:
                target_index = largest_face_index(faces)
                for index, face in enumerate(faces):
                    embedding = recognizer.embed(frame, face)
                    name, score = best_match(embedding, embeddings)
                    if name is not None and score >= args.threshold:
                        draw_result(frame, face, name, score, (0, 255, 0))
                    else:
                        unknown_score = score if name is not None else 0.0
                        draw_result(frame, face, "Unknown", unknown_score, (0, 0, 255))
                    if index == target_index:
                        panel_embedding = embedding
                        panel_scores = all_scores(embedding, embeddings)

            cv2.putText(
                frame,
                f"FPS {fps:.1f}",
                (12, 28),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            if not embeddings:
                cv2.putText(
                    frame,
                    "請先跑 register.py",
                    (12, 58),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

            cv2.imshow("YuNet + SFace recognize", frame)
            if not args.no_live_panel:
                cv2.imshow(
                    "YuNet + SFace live compare",
                    live_panel(panel_embedding, panel_scores, args.threshold),
                )
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
