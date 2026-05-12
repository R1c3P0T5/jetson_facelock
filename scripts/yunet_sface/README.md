# YuNet + SFace Scripts

Prototype scripts for local face registration and recognition with OpenCV YuNet
for face detection and SFace for 128-dimensional face embeddings.

## Quick Start

```bash
bash scripts/download-face-models.sh
python3 scripts/yunet_sface/register.py --name alice --camera 0
python3 scripts/yunet_sface/recognize.py --camera 0
```

`register.py` saves one embedding to `scripts/yunet_sface/store.pkl`.
`recognize.py` compares live camera embeddings against that local store.

## Files

| File | Purpose |
| ---- | ------- |
| `register.py` | Capture and save one face embedding. |
| `recognize.py` | Compare live faces against saved embeddings. |
| `detector.py` | YuNet detector wrapper. |
| `recognizer.py` | SFace embedding and cosine helpers. |
| `store.py` | Local pickle-backed embedding store. |
| `model_files.py` | Model path defaults and missing-file hints. |
| `../download-face-models.sh` | Download and verify ONNX models. |

## Notes

- ONNX models live in `scripts/models/` and are ignored by Git.
- `store.pkl` contains local face data and is ignored by Git.
- Use `--threshold` to tune recognition strictness; higher is stricter.
- If `cv2.FaceDetectorYN` or `cv2.FaceRecognizerSF` is missing, check the
  installed OpenCV version.

## References

- https://docs.opencv.org/4.x/d0/dd4/tutorial_dnn_face.html
- https://github.com/ShiqiYu/libfacedetection
- https://github.com/zhongyy/SFace
- https://github.com/ShiqiYu/libfacedetection.train
