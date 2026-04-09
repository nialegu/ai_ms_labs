"""
Скрипт выполняет фильтрацию только по классу "самолёт"
и выделяет найденные объекты зелёной рамкой.

Установка:
    pip install opencv-python numpy

Запуск (веб-камера):
    python main_airplane.py

Запуск (видео):
    python main_airplane.py --video airplane_video.mp4

Для выхода нажмите клавишу 'q'.
"""

import os
import sys
import shutil
import tempfile
import numpy as np
import argparse
import time
import cv2


# Парсинг аргументов
parser = argparse.ArgumentParser(description="Детектирование самолётов (вариант 17)")
parser.add_argument("-v", "--video", type=str, default=None,
                    help="путь к видео (если не указан — используется камера)")
parser.add_argument("-c", "--confidence", type=float, default=0.3,
                    help="порог уверенности (по умолчанию 0.3)")
args = vars(parser.parse_args())

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_safe_path(path):
    # Проверка пути на ASCII и копирование во временную папку при необходимости
    try:
        path.encode("ascii")
        return path
    except UnicodeEncodeError:
        pass

    cache_dir = os.path.join(tempfile.gettempdir(), "lab2_cache")
    os.makedirs(cache_dir, exist_ok=True)

    new_path = os.path.join(cache_dir, os.path.basename(path))

    if not os.path.isfile(new_path) or os.path.getsize(new_path) != os.path.getsize(path):
        shutil.copy2(path, new_path)

    return new_path


# Параметры целевого класса
TARGET_CLASS_ID = 5            
TARGET_LABEL = "airplane"
BOX_COLOR = (0, 255, 0)      


# Пути к модели
MODEL_DIR = os.path.join(BASE_DIR, "ssd_mobilenet_v2_coco_2018_03_29")
MODEL_WEIGHTS = os.path.join(MODEL_DIR, "frozen_inference_graph.pb")
MODEL_CONFIG = os.path.join(BASE_DIR, "ssd_mobilenet_v2_coco_2018_03_29.pbtxt")

# Проверка наличия файлов модели
for file_path in [MODEL_WEIGHTS, MODEL_CONFIG]:
    if not os.path.isfile(file_path):
        print(f"[ERROR] Файл не найден: {file_path}")
        print("Скачайте модель с помощью: python download_model.py")
        sys.exit(1)


# Инициализация модели
print("[INFO] Загрузка модели SSD MobileNet V2...")
net = cv2.dnn.readNetFromTensorflow(get_safe_path(MODEL_WEIGHTS),
                                    get_safe_path(MODEL_CONFIG))
print("[INFO] Модель успешно загружена")
print(f"[INFO] Детектируемый класс: {TARGET_LABEL} (id={TARGET_CLASS_ID})")


# Инициализация видеопотока
if args["video"]:
    input_video = args["video"]

    if not os.path.isfile(input_video):
        input_video = os.path.join(BASE_DIR, input_video)

    if not os.path.isfile(input_video):
        print(f"[ERROR] Видео не найдено: {args['video']}")
        sys.exit(1)

    print(f"[INFO] Используется видеофайл: {input_video}")
    cap = cv2.VideoCapture(get_safe_path(os.path.abspath(input_video)))
else:
    print("[INFO] Запуск веб-камеры...")
    cap = cv2.VideoCapture(0)
    time.sleep(2.0)


if not cap.isOpened():
    print("[ERROR] Не удалось открыть источник видео")
    sys.exit(1)


# Основной цикл обработки
total_frames = 0
frames_with_airplane = 0
start_time = time.time()

while True:
    grabbed, frame = cap.read()
    if not grabbed:
        break

    (height, width) = frame.shape[:2]
    total_frames += 1

    # Подготовка изображения для нейросети
    blob = cv2.dnn.blobFromImage(frame, size=(300, 300), swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward()

    airplane_detected = False

    for i in range(detections.shape[2]):
        conf = detections[0, 0, i, 2]

        if conf > args["confidence"]:
            class_id = int(detections[0, 0, i, 1])

            # Обрабатываем только самолёты
            if class_id == TARGET_CLASS_ID:
                airplane_detected = True

                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                (x1, y1, x2, y2) = box.astype("int")

                label = f"{TARGET_LABEL}: {conf * 100:.1f}%"

                cv2.rectangle(frame, (x1, y1), (x2, y2), BOX_COLOR, 2)

                text_y = y1 - 15 if y1 - 15 > 15 else y1 + 15
                cv2.putText(frame, label, (x1, text_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, BOX_COLOR, 2)

    if airplane_detected:
        frames_with_airplane += 1

    # Расчёт FPS
    elapsed_time = time.time() - start_time
    fps = total_frames / elapsed_time if elapsed_time > 0 else 0

    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.putText(frame,
                f"Airplane: {frames_with_airplane}/{total_frames} frames",
                (10, height - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1)

    cv2.imshow("Airplane Detection (Variant 17)", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Завершение работы
elapsed_time = time.time() - start_time
fps = total_frames / elapsed_time if elapsed_time > 0 else 0

print(f"\n[INFO] Всего кадров: {total_frames}")
print(f"[INFO] Кадров с самолётом: {frames_with_airplane}")
print(f"[INFO] Время работы: {elapsed_time:.1f}с, FPS: {fps:.1f}")

cap.release()
cv2.destroyAllWindows()