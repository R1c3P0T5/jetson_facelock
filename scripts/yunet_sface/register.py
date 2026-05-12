from __future__ import annotations

import argparse
import sys
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
from scripts.yunet_sface.recognizer import FaceRecognizer, cosine
from scripts.yunet_sface.store import EmbeddingStore


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STORE = ROOT / "scripts/yunet_sface/store.pkl"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Register one face embedding with YuNet + SFace.")
    parser.add_argument("--name", required=True, help="User key to store, later replaceable by UUID.")
    parser.add_argument("--camera", type=int, default=0, help="Camera index.")
    parser.add_argument("--store", type=Path, default=DEFAULT_STORE, help="Embedding store path.")
    parser.add_argument("--detector-model", type=Path, default=DEFAULT_DETECTOR_MODEL)
    parser.add_argument("--recognizer-model", type=Path, default=DEFAULT_RECOGNIZER_MODEL)
    return parser.parse_args()


def largest_face(faces: np.ndarray) -> np.ndarray:
    areas = faces[:, 2] * faces[:, 3]
    return faces[int(np.argmax(areas))]


def draw_face(frame: np.ndarray, face: np.ndarray, label: str, color: tuple[int, int, int]) -> None:
    x, y, w, h = face[:4].astype(int)
    score = float(face[-1])
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    cv2.putText(
        frame,
        f"{label} {score:.2f}",
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

    existing = store.all()
    if args.name in existing:
        print(f"{args.name!r} 已存在；按 c 儲存時會覆蓋。")

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print(f"Could not open camera {args.camera}", file=sys.stderr)
        return 1

    status = "press c to capture, q to quit"
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Could not read frame from camera", file=sys.stderr)
                return 1

            faces = detector.detect(frame)
            selected = None
            if faces is not None and len(faces) > 0:
                selected = largest_face(faces)
                for face in faces:
                    draw_face(frame, face, "face", (0, 255, 255))
                draw_face(frame, selected, "capture target", (0, 255, 0))

            cv2.putText(
                frame,
                status,
                (12, 28),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.imshow("YuNet + SFace register", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("c"):
                if selected is None:
                    status = "no face detected"
                    print(status)
                    continue
                embedding = recognizer.embed(frame, selected)
                old_blob = store.all().get(args.name)
                if old_blob is not None:
                    old_embedding = recognizer.from_bytes(old_blob)
                    similarity = cosine(embedding, old_embedding)
                    print(f"覆蓋 {args.name!r}；與舊 embedding 的 cosine: {similarity:.4f}")
                else:
                    print(f"saving new embedding for {args.name!r}")
                store.upsert(args.name, recognizer.to_bytes(embedding))
                status = f"saved {args.name}"
                print(status)
    finally:
        cap.release()
        cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
