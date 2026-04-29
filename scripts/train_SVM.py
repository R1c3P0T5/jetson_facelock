#!/usr/bin/env python3
"""
訓練流程:
1. 讀取 dataset/ 裡的人臉圖片
2. 用 OpenFace 算出 128 維 embedding
3. 訓練 SVM 分類器
4. 輸出 model.pkl
"""
import os
import cv2
import pickle
import numpy as np
import argparse
from sklearn.svm import SVC

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(SCRIPT_DIR, "models")
DNN_PROTO = os.path.join(MODEL_DIR, "deploy.prototxt")
DNN_MODEL = os.path.join(MODEL_DIR, "res10_300x300_ssd_iter_140000.caffemodel")
EMBED_MODEL = os.path.join(MODEL_DIR, "openface_nn4.small2.v1.t7")


def get_embedding(embedder, face_img):
    blob = cv2.dnn.blobFromImage(face_img, 1.0 / 255, (96, 96),
                                 (0, 0, 0), True, False)
    embedder.setInput(blob)
    return embedder.forward().flatten()


def detect_and_crop(detector, frame, min_conf=0.3):
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                 (104.0, 177.0, 123.0), False, False)
    detector.setInput(blob)
    dets = detector.forward()

    best = None
    best_area = 0
    for i in range(dets.shape[2]):
        c = float(dets[0, 0, i, 2])
        if c < min_conf:
            continue
        x1 = max(0, int(dets[0, 0, i, 3] * w))
        y1 = max(0, int(dets[0, 0, i, 4] * h))
        x2 = min(w, int(dets[0, 0, i, 5] * w))
        y2 = min(h, int(dets[0, 0, i, 6] * h))
        area = (x2 - x1) * (y2 - y1)
        if area > best_area:
            best_area = area
            best = (x1, y1, x2, y2)

    if best is None:
        return None
    x1, y1, x2, y2 = best
    return frame[y1:y2, x1:x2]


def augment(img):
    results = [img]
    results.append(cv2.flip(img, 1))
    results.append(cv2.convertScaleAbs(img, alpha=1.15, beta=15))
    results.append(cv2.convertScaleAbs(img, alpha=0.85, beta=-15))
    results.append(cv2.GaussianBlur(img, (3, 3), 0))
    return results


def main():
    parser = argparse.ArgumentParser(description="訓練 SVM 人臉辨識模型")
    parser.add_argument("--dataset", default=os.path.join(SCRIPT_DIR, "dataset"))
    parser.add_argument("--output", default=os.path.join(SCRIPT_DIR, "model.pkl"))
    parser.add_argument("--augment", action="store_true", help="資料增強（建議開）")
    args = parser.parse_args()

    for path, desc in [(DNN_PROTO, "偵測模型 prototxt"),
                        (DNN_MODEL, "偵測模型 caffemodel"),
                        (EMBED_MODEL, "OpenFace embedding 模型")]:
        if not os.path.exists(path):
            print(f"找不到 {desc}: {path}")
            return

    detector = cv2.dnn.readNetFromCaffe(DNN_PROTO, DNN_MODEL)
    embedder = cv2.dnn.readNetFromTorch(EMBED_MODEL)

    all_embeddings = []
    all_names = []

    if not os.path.isdir(args.dataset):
        print(f"dataset 不存在: {args.dataset}")
        return

    persons = sorted([d for d in os.listdir(args.dataset)
                      if os.path.isdir(os.path.join(args.dataset, d))])
    if not persons:
        print("dataset 裡沒有資料")
        return

    # 建立 name <-> id 對照表
    name_to_id = {}
    id_to_name = {}
    for i, name in enumerate(persons):
        name_to_id[name] = i
        id_to_name[i] = name

    print("=== 讀取資料集 ===")
    for person_name in persons:
        person_dir = os.path.join(args.dataset, person_name)
        count = 0

        files = sorted([f for f in os.listdir(person_dir)
                        if f.lower().endswith((".jpg", ".jpeg", ".png"))])

        for file in files:
            path = os.path.join(person_dir, file)
            img = cv2.imread(path)
            if img is None:
                continue

            face = detect_and_crop(detector, img)
            if face is None:
                face = img

            if face.shape[0] < 20 or face.shape[1] < 20:
                continue

            images = augment(face) if args.augment else [face]
            for aug_img in images:
                emb = get_embedding(embedder, aug_img)
                all_embeddings.append(emb)
                all_names.append(person_name)
                count += 1

        print(f"  {person_name}: {count} 筆")

    if len(all_embeddings) < 2:
        print("資料太少，無法訓練")
        return

    X = np.array(all_embeddings, dtype=np.float64)
    y = np.array([name_to_id[n] for n in all_names], dtype=np.int64)

    print(f"\n=== 訓練 SVM ===")
    print(f"  共 {len(X)} 筆，{len(persons)} 個人")

    svm = SVC(
        kernel="rbf",
        C=10.0,
        gamma="auto",
        probability=True,
        random_state=42
    )
    svm.fit(X, y)

    train_acc = svm.score(X, y)
    print(f"  訓練準確率: {train_acc:.1%}")

    model_data = {
        "svm": svm,
        "name_to_id": name_to_id,
        "id_to_name": id_to_name,
    }

    with open(args.output, "wb") as f:
        pickle.dump(model_data, f)

    print(f"\n=== 完成 ===")
    print(f"  模型: {args.output}")
    print(f"  人員: {', '.join(persons)}")
    print(f"  下一步: python3 recognize_face.py")


if __name__ == "__main__":
    main()
