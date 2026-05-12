import numpy as np
import pytest

from src.core.config import get_settings


def _models_present() -> bool:
    try:
        settings = get_settings()
        return (
            settings.FACE_DETECTOR_MODEL.exists()
            and settings.FACE_RECOGNIZER_MODEL.exists()
        )
    except Exception:
        return False


skip_no_models = pytest.mark.skipif(
    not _models_present(),
    reason="ONNX model files not found",
)


@skip_no_models
def test_face_engine_instantiates_with_valid_model_paths() -> None:
    from src.faces.engine import FaceEngine

    settings = get_settings()
    engine = FaceEngine(settings.FACE_DETECTOR_MODEL, settings.FACE_RECOGNIZER_MODEL)

    assert engine is not None


@skip_no_models
def test_detect_and_embed_blank_image_returns_none() -> None:
    from src.faces.engine import FaceEngine

    settings = get_settings()
    engine = FaceEngine(settings.FACE_DETECTOR_MODEL, settings.FACE_RECOGNIZER_MODEL)
    blank = np.zeros((320, 240, 3), dtype=np.uint8)

    result = engine.detect_and_embed(blank)

    assert result is None
