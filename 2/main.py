"""
Используется SSD MobileNet V2 COCO (90 классов) + OpenCV DNN.

Установка:
    pip install opencv-python numpy

Запуск с веб-камерой:
    python main.py

Запуск с видеофайлом:
    python main.py --video airplane_video.mp4

Для выхода нажмите 'q'.
"""
import os
import sys
import shutil
import tempfile
import numpy as np
import argparse
import time
import cv2


# ===== Аргументы =====
ap = argparse.ArgumentParser(description="Распознавание объектов в видеопотоке")
ap.add_argument("-v", "--video", type=str, default=None,
                help="путь к видеофайлу (без аргумента — веб-камера)")
ap.add_argument("-c", "--confidence", type=float, default=0.3,
                help="минимальный порог уверенности (по умолчанию 0.3)")
args = vars(ap.parse_args())

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def safe_path(filepath):
    try:
        filepath.encode("ascii")
        return filepath
    except UnicodeEncodeError:
        pass
    tmpdir = os.path.join(tempfile.gettempdir(), "lab2_cache")
    os.makedirs(tmpdir, exist_ok=True)
    dst = os.path.join(tmpdir, os.path.basename(filepath))
    if not os.path.isfile(dst) or os.path.getsize(dst) != os.path.getsize(filepath):
        shutil.copy2(filepath, dst)
    return dst


# ===== 90 классов COCO =====
COCO_CLASSES = {
    0: 'background', 1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle',
    5: 'airplane', 6: 'bus', 7: 'train', 8: 'truck', 9: 'boat',
    10: 'traffic light', 11: 'fire hydrant', 13: 'stop sign',
    14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat', 18: 'dog',
    19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
    24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella',
    31: 'handbag', 32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis',
    36: 'snowboard', 37: 'sports ball', 38: 'kite', 39: 'baseball bat',
    40: 'baseball glove', 41: 'skateboard', 42: 'surfboard',
    43: 'tennis racket', 44: 'bottle', 46: 'wine glass', 47: 'cup',
    48: 'fork', 49: 'knife', 50: 'spoon', 51: 'bowl', 52: 'banana',
    53: 'apple', 54: 'sandwich', 55: 'orange', 56: 'broccoli',
    57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut', 61: 'cake',
    62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
    67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
    75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave',
    79: 'oven', 80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book',
    85: 'clock', 86: 'vase', 87: 'scissors', 88: 'teddy bear',
    89: 'hair drier', 90: 'toothbrush',
}

np.random.seed(42)
COLORS = {k: [int(c) for c in color]
           for k, color in zip(COCO_CLASSES.keys(),
                               np.random.uniform(0, 255, size=(len(COCO_CLASSES), 3)))}

# ===== Пути к модели =====
MODEL_PB = os.path.join(SCRIPT_DIR, "ssd_mobilenet_v2_coco_2018_03_29",
                        "frozen_inference_graph.pb")
MODEL_PBTXT = os.path.join(SCRIPT_DIR, "ssd_mobilenet_v2_coco_2018_03_29.pbtxt")

for fpath in [MODEL_PB, MODEL_PBTXT]:
    if not os.path.isfile(fpath):
        print(f"[ОШИБКА] Не найден: {fpath}")
        print("Скачайте модель: python download_model.py")
        sys.exit(1)

# ===== Загрузка модели =====
print("[INFO] Загрузка модели SSD MobileNet V2 COCO...")
net = cv2.dnn.readNetFromTensorflow(safe_path(MODEL_PB), safe_path(MODEL_PBTXT))
print("[INFO] Модель загружена.")

# ===== Открытие видео =====
if args["video"]:
    video_path = args["video"]
    if not os.path.isfile(video_path):
        video_path = os.path.join(SCRIPT_DIR, args["video"])
    if not os.path.isfile(video_path):
        print(f"[ОШИБКА] Видеофайл не найден: {args['video']}")
        sys.exit(1)
    print(f"[INFO] Видеофайл: {video_path}")
    cap = cv2.VideoCapture(safe_path(os.path.abspath(video_path)))
else:
    print("[INFO] Веб-камера...")
    cap = cv2.VideoCapture(0)
    time.sleep(2.0)

if not cap.isOpened():
    print("[ОШИБКА] Не удалось открыть видеоисточник.")
    sys.exit(1)

# ===== Основной цикл =====
frame_count = 0
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    (h, w) = frame.shape[:2]
    frame_count += 1

    blob = cv2.dnn.blobFromImage(frame, size=(300, 300), swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > args["confidence"]:
            cls_id = int(detections[0, 0, i, 1])
            name = COCO_CLASSES.get(cls_id, f"class_{cls_id}")

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            label = f"{name}: {confidence*100:.1f}%"
            color = COLORS.get(cls_id, (0, 255, 0))
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    elapsed = time.time() - start_time
    fps_val = frame_count / elapsed if elapsed > 0 else 0
    cv2.putText(frame, f"FPS: {fps_val:.1f}", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Object Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

elapsed = time.time() - start_time
fps_val = frame_count / elapsed if elapsed > 0 else 0
print(f"\n[INFO] Кадров: {frame_count}, время: {elapsed:.1f}с, FPS: {fps_val:.1f}")

cap.release()
cv2.destroyAllWindows()