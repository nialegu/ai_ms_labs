"""Скачивание модели SSD MobileNet V2 COCO из TensorFlow Model Zoo

Запуск:
    python download_model.py

Скачивает архив, извлекает frozen_inference_graph.pb и конфиг для OpenCV
"""
import os
import sys
import urllib.request
import tarfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(SCRIPT_DIR, "ssd_mobilenet_v2_coco_2018_03_29")
MODEL_PB = os.path.join(MODEL_DIR, "frozen_inference_graph.pb")
MODEL_PBTXT = os.path.join(SCRIPT_DIR, "ssd_mobilenet_v2_coco_2018_03_29.pbtxt")

TF_ZOO_URL = "http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz"
PBTXT_URL = "https://raw.githubusercontent.com/opencv/opencv_extra/4.x/testdata/dnn/ssd_mobilenet_v2_coco_2018_03_29.pbtxt"


def main():
    # Скачиваем frozen graph из TF Model Zoo
    if os.path.isfile(MODEL_PB) and os.path.getsize(MODEL_PB) > 50_000_000:
        print(f"[OK] Модель уже скачана: {MODEL_PB}")
    else:
        archive = os.path.join(SCRIPT_DIR, "ssd_mobilenet_v2_coco.tar.gz")
        print(f"[INFO] Скачиваю модель из TF Model Zoo (~187 МБ)...")
        print(f"  URL: {TF_ZOO_URL}")
        urllib.request.urlretrieve(TF_ZOO_URL, archive)
        print(f"  Скачано: {os.path.getsize(archive) / 1024 / 1024:.0f} МБ")

        print("[INFO] Извлекаю архив...")
        with tarfile.open(archive, "r:gz") as tar:
            tar.extractall(SCRIPT_DIR)

        os.remove(archive)
        print(f"[OK] Модель: {MODEL_PB}")

    # Скачиваем pbtxt-конфиг для OpenCV DNN
    if os.path.isfile(MODEL_PBTXT) and os.path.getsize(MODEL_PBTXT) > 1000:
        print(f"[OK] Конфиг уже скачан: {MODEL_PBTXT}")
    else:
        print(f"[INFO] Скачиваю конфиг OpenCV...")
        urllib.request.urlretrieve(PBTXT_URL, MODEL_PBTXT)
        print(f"[OK] Конфиг: {MODEL_PBTXT}")

    print("\n[ГОТОВО] Всё скачано. Можно запускать:")
    print("  python detect_image.py")
    print("  python main.py --video airplane_video.mp4")
    print("  python main_airplane.py --video airplane_video.mp4")


if __name__ == "__main__":
    main()