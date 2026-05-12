from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DETECTOR_MODEL = ROOT / "scripts/models/face_detection_yunet_2023mar.onnx"
DEFAULT_RECOGNIZER_MODEL = ROOT / "scripts/models/face_recognition_sface_2021dec.onnx"
DOWNLOAD_COMMAND = "bash scripts/download-face-models.sh"


def missing_model_paths(paths: Iterable[Path]) -> list[Path]:
    return [path for path in paths if not path.is_file()]


def model_setup_hint(missing_paths: Iterable[Path]) -> str:
    missing = "\n".join(f"  - {path}" for path in missing_paths)
    return (
        "Missing face model file(s):\n"
        f"{missing}\n\n"
        f"Run `{DOWNLOAD_COMMAND}` from the repository root, or pass custom paths with "
        "`--detector-model` and `--recognizer-model`."
    )
