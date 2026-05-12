from pathlib import Path

import cv2
import numpy as np


class FaceDetector:
    def __init__(
        self,
        model_path: str | Path,
        input_size: tuple[int, int] = (320, 320),
        score_threshold: float = 0.9,
        nms_threshold: float = 0.3,
        top_k: int = 50,
    ):
        self._model = cv2.FaceDetectorYN.create(
            model=str(model_path),
            config="",
            input_size=input_size,
            score_threshold=score_threshold,
            nms_threshold=nms_threshold,
            top_k=top_k,
        )

    def detect(self, frame_bgr: np.ndarray) -> np.ndarray | None:
        """Return an (N, 15) face array, or None when no face is detected.

        Each row is:
        [x, y, w, h, lx0, ly0, ... lx4, ly4, score]

        The row format can be passed directly to FaceRecognizerSF.alignCrop().
        """
        h, w = frame_bgr.shape[:2]
        self._model.setInputSize((w, h))
        _, faces = self._model.detect(frame_bgr)
        return faces
