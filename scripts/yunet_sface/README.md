# YuNet + SFace Scripts

These scripts are the current face-recognition prototype path. They use OpenCV's
YuNet detector to locate faces and SFace to create 128-dimensional embeddings for
registration and recognition.

## Local Model Files

Download the OpenCV ONNX model files before running the scripts:

```bash
bash scripts/download-face-models.sh
```

The script places these files under `scripts/models/`:

```text
scripts/models/face_detection_yunet_2023mar.onnx
scripts/models/face_recognition_sface_2021dec.onnx
```

The model files are local runtime artifacts and are ignored by Git. Keep the
downloaded model versions aligned with the filenames above, or pass custom paths
with `--detector-model` and `--recognizer-model`.

## Register a Face

```bash
python scripts/yunet_sface/register.py --name alice --camera 0
```

Press `c` to capture the largest detected face and save its embedding. Press `q`
to quit. The default store is `scripts/yunet_sface/store.pkl`; it contains local
face data and is intentionally ignored by Git.

## Recognize Faces

```bash
python scripts/yunet_sface/recognize.py --camera 0
```

The recognition script compares live embeddings against the local store with a
cosine threshold. Use `--threshold` to tune strictness and `--no-live-panel` to
disable the embedding heatmap/comparison window.

## References

- OpenCV YuNet and SFace DNN tutorial: https://docs.opencv.org/4.x/d0/dd4/tutorial_dnn_face.html
- libfacedetection: https://github.com/ShiqiYu/libfacedetection
- SFace: https://github.com/zhongyy/SFace
- libfacedetection training code: https://github.com/ShiqiYu/libfacedetection.train
