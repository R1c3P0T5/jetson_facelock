#!/usr/bin/env python3
"""
錄影 → 自動抽取人臉樣本
偵測: OpenCV DNN SSD（側臉 OK）
"""
import os
import cv2
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(SCRIPT_DIR, "models")
DNN_PROTO = os.path.join(MODEL_DIR, "deploy.prototxt")
DNN_MODEL = os.path.join(MODEL_DIR, "res10_300x300_ssd_iter_140000.caffemodel")


def open_camera(camera_arg):
    if isinstance(camera_arg, str):
        if camera_arg.isdigit():
            return cv2.VideoCapture(int(camera_arg))
        if camera_arg.startswith("/dev/video"):
            idx = camera_arg.replace("/dev/video", "")
            if idx.isdigit():
                return cv2.VideoCapture(int(idx))
    return cv2.VideoCapture(camera_arg)


class FaceDetector:
    def __init__(self, proto, model, conf=0.5):
        self.net = cv2.dnn.readNetFromCaffe(proto, model)
        self.conf = conf

    def detect(self, frame):
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                     (104.0, 177.0, 123.0), False, False)
        self.net.setInput(blob)
        dets = self.net.forward()
        faces = []
        for i in range(dets.shape[2]):
            c = float(dets[0, 0, i, 2])
            if c < self.conf:
                continue
            x1 = max(0, int(dets[0, 0, i, 3] * w))
            y1 = max(0, int(dets[0, 0, i, 4] * h))
            x2 = min(w, int(dets[0, 0, i, 5] * w))
            y2 = min(h, int(dets[0, 0, i, 6] * h))
            if x2 > x1 and y2 > y1:
                faces.append((x1, y1, x2 - x1, y2 - y1, c))
        return faces


def largest_face(faces):
    if not faces:
        return None
    return max(faces, key=lambda f: f[2] * f[3])


def extract_faces(frames, detector, person_dir, name, start_idx, count, interval):
    saved = 0
    idx = start_idx

    for i, frame in enumerate(frames):
        if saved >= count:
            break
        if i % interval != 0:
            continue

        faces = detector.detect(frame)
        face = largest_face(faces)
        if face is None:
            continue

        x, y, w, h, _ = face
        pad_x = int(w * 0.15)
        pad_y = int(h * 0.15)
        fh, fw = frame.shape[:2]
        x1 = max(0, x - pad_x)
        y1 = max(0, y - pad_y)
        x2 = min(fw, x + w + pad_x)
        y2 = min(fh, y + h + pad_y)

        face_img = frame[y1:y2, x1:x2]
        if face_img.size == 0:
            continue

        face_img = cv2.resize(face_img, (256, 256))
        filename = os.path.join(person_dir, f"{name}_{idx:04d}.jpg")
        cv2.imwrite(filename, face_img, [cv2.IMWRITE_JPEG_QUALITY, 95])
        saved += 1
        idx += 1
        print(f"  已存: {filename}")

    return saved


def main():
    parser = argparse.ArgumentParser(description="錄影 → 自動抽取人臉樣本")
    parser.add_argument("--name", required=True, help="人名")
    parser.add_argument("--camera", default="/dev/video0")
    parser.add_argument("--save-dir", default=os.path.join(SCRIPT_DIR, "dataset"))
    parser.add_argument("--count", type=int, default=50, help="最多抽幾張（建議 30~80）")
    parser.add_argument("--interval", type=int, default=2, help="每隔幾幀抽一張")
    parser.add_argument("--confidence", type=float, default=0.5, help="偵測信心門檻")
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    args = parser.parse_args()

    if not os.path.exists(DNN_PROTO) or not os.path.exists(DNN_MODEL):
        print("找不到 DNN 模型，請確認 models/ 資料夾:")
        print(f"  {DNN_PROTO}")
        print(f"  {DNN_MODEL}")
        return

    detector = FaceDetector(DNN_PROTO, DNN_MODEL, args.confidence)
    print("偵測器: DNN SSD（側臉 OK）")

    person_dir = os.path.join(args.save_dir, args.name)
    os.makedirs(person_dir, exist_ok=True)

    existing = [f for f in os.listdir(person_dir)
                if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    next_index = len(existing) + 1

    cap = open_camera(args.camera)
    if not cap.isOpened():
        print("無法開啟攝影機")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    recording = False
    recorded_frames = []

    print("=== 操作說明 ===")
    print("  r = 開始/停止錄影")
    print("  q = 離開")
    print(f"  目標: {args.count} 張，每 {args.interval} 幀抽 1 張")
    print("================")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        display = frame.copy()
        faces = detector.detect(frame)
        face = largest_face(faces)

        if face is not None:
            x, y, w, h, conf = face
            cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(display, f"{conf:.0%}", (x, y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        if recording:
            recorded_frames.append(frame.copy())
            cv2.circle(display, (30, 30), 12, (0, 0, 255), -1)
            cv2.putText(display, f"REC  {len(recorded_frames)} frames", (50, 38),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(display, "press r to stop", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        else:
            cv2.putText(display, f"name: {args.name}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(display, f"saved: {next_index - 1}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(display, "press r to record", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("Register Face", display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        elif key == ord("r"):
            if not recording:
                recording = True
                recorded_frames = []
                print(">>> 開始錄影，慢慢轉頭（正面→左→右→上→下），按 r 停止")
            else:
                recording = False
                print(f">>> 停止錄影，共 {len(recorded_frames)} 幀")

                saved = extract_faces(
                    recorded_frames, detector,
                    person_dir, args.name,
                    next_index, args.count, args.interval
                )
                next_index += saved
                print(f">>> 存了 {saved} 張，目前共 {next_index - 1} 張")
                recorded_frames = []

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
