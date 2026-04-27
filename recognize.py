#!/usr/bin/env python3
"""
即時人臉辨識
偵測: DNN SSD（側臉 OK）
辨識: OpenFace embedding → SVM 分類器
"""
import os
import cv2
import time
import pickle
import numpy as np
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(SCRIPT_DIR, "models")
DNN_PROTO = os.path.join(MODEL_DIR, "deploy.prototxt")
DNN_MODEL = os.path.join(MODEL_DIR, "res10_300x300_ssd_iter_140000.caffemodel")
EMBED_MODEL = os.path.join(MODEL_DIR, "openface_nn4.small2.v1.t7")


def open_camera(camera_arg):
    if isinstance(camera_arg, str):
        if camera_arg.isdigit():
            return cv2.VideoCapture(int(camera_arg))
        if camera_arg.startswith("/dev/video"):
            idx = camera_arg.replace("/dev/video", "")
            if idx.isdigit():
                return cv2.VideoCapture(int(idx))
    return cv2.VideoCapture(camera_arg)


class FaceRecognizer:
    def __init__(self, proto, model, embed_model, model_path, threshold=0.5):
        self.detector = cv2.dnn.readNetFromCaffe(proto, model)
        self.embedder = cv2.dnn.readNetFromTorch(embed_model)
        self.threshold = threshold

        with open(model_path, "rb") as f:
            data = pickle.load(f)

        self.svm = data["svm"]
        self.id_to_name = data["id_to_name"]
        self.names = list(data["id_to_name"].values())

        print(f"已載入模型，{len(self.names)} 個人: {', '.join(self.names)}")

    def detect_faces(self, frame, min_conf=0.5):
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                     (104.0, 177.0, 123.0), False, False)
        self.detector.setInput(blob)
        dets = self.detector.forward()

        faces = []
        for i in range(dets.shape[2]):
            c = float(dets[0, 0, i, 2])
            if c < min_conf:
                continue
            x1 = max(0, int(dets[0, 0, i, 3] * w))
            y1 = max(0, int(dets[0, 0, i, 4] * h))
            x2 = min(w, int(dets[0, 0, i, 5] * w))
            y2 = min(h, int(dets[0, 0, i, 6] * h))
            if x2 > x1 and y2 > y1:
                faces.append((x1, y1, x2, y2, c))
        return faces

    def get_embedding(self, face_img):
        blob = cv2.dnn.blobFromImage(face_img, 1.0 / 255, (96, 96),
                                     (0, 0, 0), True, False)
        self.embedder.setInput(blob)
        return self.embedder.forward().flatten()

    def recognize(self, face_img):
        emb = self.get_embedding(face_img)
        emb = emb.reshape(1, -1).astype(np.float64)

        proba = self.svm.predict_proba(emb)[0]
        max_idx = np.argmax(proba)
        confidence = float(proba[max_idx])
        predicted_id = self.svm.classes_[max_idx]
        name = self.id_to_name.get(int(predicted_id), "Unknown")

        if confidence < self.threshold:
            name = "Unknown"

        return name, confidence


def main():
    parser = argparse.ArgumentParser(description="即時人臉辨識（SVM）")
    parser.add_argument("--camera", default="/dev/video0")
    parser.add_argument("--model",
                        default=os.path.join(SCRIPT_DIR, "model.pkl"))
    parser.add_argument("--threshold", type=float, default=0.5,
                        help="信心門檻（0~1，越高越嚴格，建議 0.4~0.7）")
    parser.add_argument("--detect-conf", type=float, default=0.5)
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    args = parser.parse_args()

    for path, desc in [(DNN_PROTO, "偵測模型"),
                        (DNN_MODEL, "偵測模型"),
                        (EMBED_MODEL, "OpenFace 模型"),
                        (args.model, "SVM 模型")]:
        if not os.path.exists(path):
            print(f"找不到: {path} ({desc})")
            if path == args.model:
                print("請先跑 python3 train_SVM.py --augment")
            return

    recognizer = FaceRecognizer(
        DNN_PROTO, DNN_MODEL, EMBED_MODEL,
        args.model, args.threshold
    )

    cap = open_camera(args.camera)
    if not cap.isOpened():
        print("無法開啟攝影機")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    print(f"threshold: {args.threshold}")
    print("按 q 離開")

    prev_time = time.time()
    fps = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        now = time.time()
        dt = now - prev_time
        if dt > 0:
            fps = 0.8 * fps + 0.2 * (1.0 / dt)
        prev_time = now

        display = frame.copy()
        faces = recognizer.detect_faces(frame, args.detect_conf)

        for (x1, y1, x2, y2, det_conf) in faces:
            face_img = frame[y1:y2, x1:x2]
            if face_img.shape[0] < 20 or face_img.shape[1] < 20:
                continue

            name, confidence = recognizer.recognize(face_img)

            if name != "Unknown":
                color = (0, 255, 0)
                text = f"{name} ({confidence:.0%})"
            else:
                color = (0, 0, 255)
                text = f"Unknown ({confidence:.0%})"

            cv2.rectangle(display, (x1, y1), (x2, y2), color, 2)
            ts = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            ty = max(25, y1 - 8)
            cv2.rectangle(display, (x1, ty - ts[1] - 6),
                          (x1 + ts[0] + 4, ty + 4), color, -1)
            cv2.putText(display, text, (x1 + 2, ty),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.putText(display, f"FPS: {fps:.1f}", (args.width - 140, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

        if not faces:
            cv2.putText(display, "no face", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)

        cv2.imshow("Face Recognition", display)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
