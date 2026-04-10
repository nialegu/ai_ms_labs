import os
import sys
import argparse
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image_dataset_from_directory

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ============================================================
# CONFIG
# ============================================================

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "Images"   # Stanford Dogs

TMP = Path(os.environ.get("TEMP", "/tmp"))
OUT_DIR = TMP / "dogs_lab_output"
LOGS_DIR = TMP / "dogs_lab_logs"

IMG_SIZE = 224
BATCH = 32

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)


# ============================================================
# DATA
# ============================================================

def load_data(augment):
    if not DATA_DIR.exists():
        print("# *Ошибка: папка data/Images не найдена (Stanford Dogs Dataset)*")
        sys.exit(1)

    print("# *Загрузка датасета собак (Stanford Dogs)*")

    train_ds = image_dataset_from_directory(
        DATA_DIR,
        validation_split=0.2,
        subset="training",
        seed=42,
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH,
    )

    val_test = image_dataset_from_directory(
        DATA_DIR,
        validation_split=0.2,
        subset="validation",
        seed=42,
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH,
    )

    class_names = train_ds.class_names
    num_classes = len(class_names)

    print(f"# *Найдено пород собак: {num_classes}*")

    val_batches = tf.data.experimental.cardinality(val_test).numpy() // 2
    val_ds = val_test.take(val_batches)
    test_ds = val_test.skip(val_batches)

    # labels
    labels_path = OUT_DIR / "dog_labels.txt"
    with open(labels_path, "w", encoding="utf-8") as f:
        f.write("\n".join(class_names))

    print("# *Сохранены метки классов собак*")

    # ========================================================
    # augmentation
    # ========================================================

    aug_layers = []

    if augment["flip"]:
        print("# *Аугментация: horizontal flip*")
        aug_layers.append(layers.RandomFlip("horizontal"))

    if augment["zoom"]:
        print(f"# *Аугментация: zoom {augment['zoom']}*")
        aug_layers.append(layers.RandomZoom(augment["zoom"]))

    if augment["brightness"]:
        print(f"# *Аугментация: brightness {augment['brightness']}*")
        aug_layers.append(layers.RandomBrightness(augment["brightness"]))

    aug_model = keras.Sequential(aug_layers) if aug_layers else None
    norm = layers.Rescaling(1./127.5, offset=-1)

    def preprocess(x, y, training=False):
        if training and aug_model:
            x = aug_model(x, training=True)
        return norm(x), y

    AUTOTUNE = tf.data.AUTOTUNE

    train_ds = train_ds.map(lambda x, y: preprocess(x, y, True)).prefetch(AUTOTUNE)
    val_ds = val_ds.map(preprocess).prefetch(AUTOTUNE)
    test_ds = test_ds.map(preprocess).prefetch(AUTOTUNE)

    return train_ds, val_ds, test_ds, class_names, num_classes


# ============================================================
# MODEL
# ============================================================

def build_model(num_classes, lr):
    print("# *Создание модели MobileNetV2 (transfer learning)*")

    base = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights="imagenet"
    )

    base.trainable = False

    model = keras.Sequential([
        base,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation="softmax")
    ])

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=lr),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


# ============================================================
# TRAIN
# ============================================================

def train(model, train_ds, val_ds, epochs):
    print(f"# *Обучение модели: {epochs} эпох*")

    tb = keras.callbacks.TensorBoard(log_dir=str(LOGS_DIR))
    es = keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=[tb, es]
    )

    return history


# ============================================================
# EVAL
# ============================================================

def evaluate(model, test_ds):
    print("# *Оценка модели на тестовой выборке*")

    loss, acc = model.evaluate(test_ds)

    print(f"# *Test accuracy: {acc * 100:.2f}%*")
    print(f"# *Test loss: {loss:.4f}*")

    return acc


# ============================================================
# PLOTS
# ============================================================

def plot(history):
    print("# *Сохранение графиков обучения*")

    fig, ax = plt.subplots(1, 2, figsize=(12, 4))

    ax[0].plot(history.history["accuracy"])
    ax[0].plot(history.history["val_accuracy"])
    ax[0].set_title("Accuracy")

    ax[1].plot(history.history["loss"])
    ax[1].plot(history.history["val_loss"])
    ax[1].set_title("Loss")

    plt.savefig(OUT_DIR / "training_dogs.png")
    plt.close()


# ============================================================
# EXPORT
# ============================================================

def export(model):
    print("# *Экспорт модели в TFLite*")

    saved = OUT_DIR / "saved_model"
    model.export(str(saved))

    converter = tf.lite.TFLiteConverter.from_saved_model(str(saved))
    tflite = converter.convert()

    tflite_path = OUT_DIR / "dogs_model.tflite"
    with open(tflite_path, "wb") as f:
        f.write(tflite)

    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    quant = converter.convert()

    quant_path = OUT_DIR / "dogs_model_quant.tflite"
    with open(quant_path, "wb") as f:
        f.write(quant)

    print("# *TFLite модели сохранены*")
    print(f"# *{tflite_path.name}*")
    print(f"# *{quant_path.name}*")


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--lr", type=float, default=0.001)

    parser.add_argument("--flip", action="store_true")
    parser.add_argument("--zoom", type=float, default=0.0)
    parser.add_argument("--brightness", type=float, default=0.0)

    args = parser.parse_args()

    augment = {
        "flip": args.flip,
        "zoom": args.zoom,
        "brightness": args.brightness
    }

    print("# *Запуск лабораторной работы: классификация собак*")

    train_ds, val_ds, test_ds, class_names, num_classes = load_data(augment)

    model = build_model(num_classes, args.lr)

    history = train(model, train_ds, val_ds, args.epochs)

    evaluate(model, test_ds)

    plot(history)

    export(model)

    print("# *Готово*")


if __name__ == "__main__":
    main()