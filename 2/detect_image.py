"""
Лабораторная работа №2, Часть 1
Обнаружение объектов на изображении с использованием SSD MobileNet V2 COCO.

Используется OpenCV DNN для работы с моделью TensorFlow.
"""

import os
import sys
import tempfile
import shutil
import argparse
import numpy as np
import cv2

# Парсинг аргументов
parser = argparse.ArgumentParser(description="Обнаружение объектов на изображении")
parser.add_argument("-i", "--image", type=str, help="Путь к изображению")
parser.add_argument("-o", "--output", type=str, help="Сохранить результат в файл")
parser.add_argument("-t", "--threshold", type=float, default=0.3,
                    help="Минимальный порог уверенности (по умолчанию 0.3)")
args = parser.parse_args()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def copy_to_temp(path):
    try:
        path.encode("ascii")
        return path
    except UnicodeEncodeError:
        temp_dir = os.path.join(tempfile.gettempdir(), "cache")
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, os.path.basename(path))
        if not os.path.exists(temp_path) or os.path.getsize(temp_path) != os.path.getsize(path):
            shutil.copy2(path, temp_path)
        return temp_path


# Классы COCO
COCO_LABELS = {
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
    89: 'hair drier', 90: 'toothbrush'
}

np.random.seed(42)
CLASS_COLORS = {k: [int(c) for c in color] for k, color in zip(
    COCO_LABELS.keys(), np.random.uniform(0, 255, (len(COCO_LABELS), 3)))}


# Пути к модели
MODEL_DIR = os.path.join(SCRIPT_DIR, "ssd_mobilenet_v2_coco_2018_03_29")
PB_PATH = os.path.join(MODEL_DIR, "frozen_inference_graph.pb")
PBTXT_PATH = os.path.join(SCRIPT_DIR, "ssd_mobilenet_v2_coco_2018_03_29.pbtxt")

for f in [PB_PATH, PBTXT_PATH]:
    if not os.path.exists(f):
        print(f"[ERROR] Файл не найден: {f}")
        print("Скачайте модель через download_model.py")
        sys.exit(1)

# Загрузка модели
print("[INFO] Загружаем модель SSD MobileNet V2 COCO...")
net = cv2.dnn.readNetFromTensorflow(copy_to_temp(PB_PATH), copy_to_temp(PBTXT_PATH))
print("[INFO] Модель успешно загружена.")

# Загрузка изображения
if args.image:
    img_file = args.image
    if not os.path.isfile(img_file):
        img_file = os.path.join(SCRIPT_DIR, args.image)
    if not os.path.isfile(img_file):
        print(f"[ERROR] Изображение не найдено: {args.image}")
        sys.exit(1)
    print(f"[INFO] Загружаем изображение: {img_file}")
    frame = cv2.imread(copy_to_temp(os.path.abspath(img_file)))
else:
    # Берём кадр из видео
    video_file = os.path.join(SCRIPT_DIR, "airplane_video.mp4")
    if not os.path.isfile(video_file):
        print("[ERROR] Укажите --image или положите airplane_video.mp4 рядом")
        sys.exit(1)
    cap = cv2.VideoCapture(copy_to_temp(video_file))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames // 2)
    ret, frame = cap.read()
    cap.release()
    print(f"[INFO] Использован кадр видео (frame {total_frames // 2})")

if frame is None:
    print("[ERROR] Не удалось прочитать изображение.")
    sys.exit(1)

# Обработка и распознавание
height, width = frame.shape[:2]
blob = cv2.dnn.blobFromImage(frame, size=(300, 300), swapRB=True, crop=False)
net.setInput(blob)
detections = net.forward()

print(f"\n=== Обнаруженные объекты (порог: {args.threshold*100:.0f}%) ===")
detected_count = 0
for i in range(detections.shape[2]):
    conf = detections[0, 0, i, 2]
    if conf > args.threshold:
        class_id = int(detections[0, 0, i, 1])
        label = COCO_LABELS.get(class_id, f"class_{class_id}")
        detected_count += 1

        box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
        startX, startY, endX, endY = box.astype(int)

        color = CLASS_COLORS.get(class_id, (0, 255, 0))
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        y_text = startY - 15 if startY - 15 > 15 else startY + 15
        cv2.putText(frame, f"{label}: {conf*100:.1f}%", (startX, y_text),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        print(f"  {detected_count}. {label}: {conf*100:.1f}% [{startX},{startY} - {endX},{endY}]")

if detected_count == 0:
    print("  Объекты не обнаружены.")
else:
    print(f"\nВсего обнаружено: {detected_count}")

# Сохранение и отображение результата
if args.output:
    cv2.imwrite(args.output, frame)
    print(f"[INFO] Результат сохранён: {args.output}")

cv2.imshow("Detected Objects", frame)
print("\nНажмите любую клавишу для закрытия окна...")
cv2.waitKey(0)
cv2.destroyAllWindows()