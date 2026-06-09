import os
import time
import requests
import random
from openai import OpenAI
from datetime import datetime, timedelta, timezone

print("=== ФАЙЛ ЗАПУЩЕН ===", flush=True)

# ====== ENV ======
GREEN_API_ID = os.getenv("GREEN_API_ID")
GREEN_API_TOKEN = os.getenv("GREEN_API_TOKEN")
CHAT_ID = os.getenv("GROUP_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

BASE_URL = f"https://api.green-api.com/waInstance{GREEN_API_ID}/sendMessage/{GREEN_API_TOKEN}"

client = OpenAI(
    api_key=OPENAI_API_KEY
)

# ====== ЧАСОВОЙ ПОЯС АЛМАТЫ ======
ALMATY_TZ = timezone(timedelta(hours=5))

# ====== СОСТОЯНИЕ ======
last_sent_date = None
scheduled_date = None
scheduled_datetime = None


# ====== GPT КОНТЕНТ ======
def get_gpt_content():
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": """
Придумай:

1. Один интересный факт дня.
2. Одно бесполезное, но забавное знание дня.

Ответ строго в формате:

🧠 Интересный факт:
...

🤯 Бесполезное знание:
...

На русском языке.
Не более двух предложений на каждый пункт.
Без приветствий и лишнего текста.
"""
                }
            ],
            temperature=1
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Ошибка GPT: {e}", flush=True)

        return (
            "🧠 Интересный факт:\n"
            "Осьминог имеет три сердца.\n\n"
            "🤯 Бесполезное знание:\n"
            "Вомбаты производят кубические какашки."
        )


# ====== ПОГОДА ======
def get_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": 43.2389,
            "longitude": 76.8897,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_probability_max",
                "precipitation_sum"
            ],
            "current_weather": True,
            "timezone": "Asia/Almaty"
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        current_temp = data["current_weather"]["temperature"]
        wind = data["current_weather"]["windspeed"]

        temp_max = data["daily"]["temperature_2m_max"][0]
        temp_min = data["daily"]["temperature_2m_min"][0]

        rain_probability = data["daily"]["precipitation_probability_max"][0]
        rain_amount = data["daily"]["precipitation_sum"][0]

        return (
            f"🌤 Алматы\n"
            f"Сейчас: {current_temp}°C\n"
            f"📈 Днём до: {temp_max}°C\n"
            f"📉 Ночью: {temp_min}°C\n"
            f"🌧 Вероятность осадков: {rain_probability}%\n"
            f"☔ Осадки: {rain_amount} мм\n"
            f"💨 Ветер: {wind} м/с"
        )

    except Exception as e:
        print(f"Ошибка получения погоды: {e}", flush=True)
        return "🌤 Погода временно недоступна"


# ====== ТЕКСТ СООБЩЕНИЯ ======
def build_message():
    gpt_content = get_gpt_content()
    weather = get_weather()

    greetings = [
        "☀️ *Доброе утро, банда!*",
        "😄 *Просыпаемся, легенды!*",
        "🌿 *Спокойное утро начинается...*"
    ]

    header = random.choice(greetings)

    return (
        f"{header}\n\n"
        f"{gpt_content}\n\n"
        f"{weather}\n\n"
        f"Хорошего дня ☕"
    )


# ====== ОТПРАВКА ======
def send_whatsapp_message():
    payload = {
        "chatId": CHAT_ID,
        "message": build_message()
    }

    try:
        print("📤 Отправка сообщения...", flush=True)

        response = requests.post(
            BASE_URL,
            json=payload,
            timeout=15
        )

        if response.status_code == 200:
            print("✅ Сообщение отправлено!", flush=True)
            print(response.json(), flush=True)
        else:
            print(
                f"❌ Ошибка {response.status_code}: {response.text}",
                flush=True
            )

    except Exception as e:
        print(f"❌ Ошибка сети: {e}", flush=True)


# ====== СЛУЧАЙНОЕ ВРЕМЯ ======
def generate_daily_time():
    hour = random.choice([8, 9, 9, 10])
    minute = random.randint(0, 59)
    return hour, minute


print("🚀 BOT STARTED", flush=True)

# ТЕСТ GPT ПРИ СТАРТЕ
print(get_gpt_content(), flush=True)

while True:
    now = datetime.now(ALMATY_TZ)
    today = now.date()

    if now.minute in (0, 30) and now.second < 20:
        print(
            f"💓 BOT ALIVE | {now.strftime('%Y-%m-%d %H:%M:%S')}",
            flush=True
        )

    # Планируем отправку один раз в день
    if scheduled_date != today:
        hour, minute = generate_daily_time()

        candidate = datetime(
            now.year,
            now.month,
            now.day,
            hour,
            minute,
            tzinfo=ALMATY_TZ
        )

        if candidate <= now:
            candidate += timedelta(days=1)

        scheduled_datetime = candidate
        scheduled_date = today

        print(
            f"⏰ Следующая отправка: "
            f"{scheduled_datetime.strftime('%Y-%m-%d %H:%M')}",
            flush=True
        )

    # Проверяем пора ли отправлять
    if (
        scheduled_datetime is not None
        and now >= scheduled_datetime
        and last_sent_date != now.date()
    ):
        send_whatsapp_message()

        last_sent_date = now.date()
        scheduled_date = None
        scheduled_datetime = None

        print(
            f"✅ Сообщение отправлено в "
            f"{now.strftime('%H:%M:%S')}",
            flush=True
        )

        time.sleep(65)

    time.sleep(20)
