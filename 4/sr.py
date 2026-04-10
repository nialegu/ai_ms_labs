#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import sys
import os
import webbrowser

import speech_recognition as sr
from gtts import gTTS
import pygame


# Инициализация аудиомодуля pygame один раз
pygame.mixer.init()


# функция синтеза речи
def speak(text, lang="ru"):
    print(f"[Ассистент]: {text}")

    filename = "voice_answer.mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove(filename)


# захват голосовой команды
def listen_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as mic:
        print("\n[Ожидание команды...]")
        recognizer.adjust_for_ambient_noise(mic, duration=1)
        audio = recognizer.listen(mic)

    try:
        text = recognizer.recognize_google(audio, language="ru-RU").lower()
        print(f"[Распознано]: {text}")
        return text

    except sr.UnknownValueError:
        speak("Я не расслышала команду, попробуйте ещё раз.")
        return ""

    except sr.RequestError:
        speak("Ошибка подключения к сервису распознавания речи.")
        return ""


# преобразование времени в текст
def get_time_text():
    now = datetime.datetime.now()
    h, m = now.hour, now.minute

    hours_map = {
        0: "часов", 1: "час", 2: "часа", 3: "часа", 4: "часа",
        5: "часов", 6: "часов", 7: "часов", 8: "часов", 9: "часов",
        10: "часов", 11: "часов", 12: "часов", 13: "часов", 14: "часов",
        15: "часов", 16: "часов", 17: "часов", 18: "часов", 19: "часов",
        20: "часов", 21: "час", 22: "часа", 23: "часа"
    }

    result = f"{h} {hours_map[h]}"

    if m == 0:
        result += " ровно"
    else:
        if m in [1, 21, 31, 41, 51]:
            form = "минута"
        elif m in [2, 3, 4, 22, 23, 24, 32, 33, 34, 42, 43, 44, 52, 53, 54]:
            form = "минуты"
        else:
            form = "минут"

        result += f" {m} {form}"

    return result


# преобразование даты
def get_date_text():
    months = [
        "", "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ]

    today = datetime.datetime.now()
    return f"{today.day} {months[today.month]} {today.year} года"


# --- заглушка погоды ---
def weather_info():
    return "Погода пока не подключена. Лучше посмотреть в окно или открыть прогноз."


# обработка команд
def handle_command(text):
    if not text:
        return

    # выход
    if any(word in text for word in ["стоп", "выход", "stop"]):
        speak("Завершаю работу. Хорошего дня!")
        sys.exit()

    # время
    elif any(word in text for word in ["время", "который час", "сколько времени"]):
        speak(f"Сейчас {get_time_text()}")

    # дата
    elif any(word in text for word in ["дата", "число", "какой сегодня день"]):
        speak(f"Сегодня {get_date_text()}")

    # почта
    elif "почта" in text:
        speak("Открываю почтовый сервис.")
        webbrowser.open("https://mail.ru")

    # youtube
    elif "ютуб" in text or "youtube" in text:
        speak("Запускаю YouTube.")
        webbrowser.open("https://youtube.com")

    # имя ассистента
    elif any(word in text for word in ["кто ты", "как тебя зовут", "твое имя"]):
        speak("Я голосовой помощник Мария, созданный на Python.")

    # погода
    elif "погода" in text:
        speak(weather_info())

    # анекдот
    elif "анекдот" in text or "шутк" in text:
        speak("Почему программисты путают Хэллоуин и Рождество? Потому что Oct 31 == Dec 25!")

    # неизвестная команда
    else:
        speak(f"Я не поняла команду: {text}. Повторите, пожалуйста.")


# основной цикл
if __name__ == "__main__":
    speak("Здравствуйте! Я голосовой ассистент Мария. Я вас слушаю.")

    while True:
        command_text = listen_command()
        handle_command(command_text)

        if command_text:
            speak("Есть ли ещё задачи для выполнения?")