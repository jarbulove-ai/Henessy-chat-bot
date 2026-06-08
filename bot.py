import os
import time
import requests
import random
from datetime import datetime, timedelta, timezone

# ====== ENV ======
GREEN_API_ID = os.getenv("GREEN_API_ID")
GREEN_API_TOKEN = os.getenv("GREEN_API_TOKEN")
CHAT_ID = os.getenv("GROUP_CHAT_ID")

BASE_URL = f"https://api.green-api.com/waInstance{GREEN_API_ID}/sendMessage/{GREEN_API_TOKEN}"

# ====== ЧАСОВОЙ ПОЯС АЛМАТЫ ======
ALMATY_TZ = timezone(timedelta(hours=5))

# ====== НАСТРОЙКИ ======
last_sent_date = None
target_time = None


# ====== ФАКТЫ ======
def get_fact_of_the_day():
    return random.choice([
        "Осьминог имеет три сердца.",
        "Кошки не чувствуют сладкий вкус.",
        "В космосе нет звука.",
        "Мозг использует около 20% энергии тела.",
        "Сердце человека бьётся ~100 000 раз в день."
    ])


# ====== ПОГОДА ======
def get_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 43.2389,
            "longitude": 76.8897,
            "current_weather": True
        }

        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        temp = data["current_weather"]["temperature"]
        wind = data["current_weather"]["windspeed"]

        return f"🌤 Алматы: {temp}°C, ветер {wind} м/с"
    except:
        return "🌤 Погода недоступна"


# ====== СТИЛИ СООБЩЕНИЯ ======
def build_message():
    fact = get_fact_of_the_day()
    weather = get_weather()

    styles = [
        "☀️ *Доброе утро, банда!*",
        "😄 *Просыпаемся, легенды!*",
        "🌿 *Спокойное утро начинается...*"
    ]

    header = random.choice(styles)

    return (
        f"{header}\n\n"
        f"🤖 *Факт дня:*\n_{fact}_\n\n"
        f"{weather}\n\n"
        "Хорошего дня ☕"
    )


# ====== ОТПРАВКА ======
def send_whatsapp_message():
    payload = {
        "chatId": CHAT_ID,
        "message": build_message()
    }

    try:
        print("📤 Отправка сообщения...")

        response = requests.post(BASE_URL, json=payload, timeout=15)

        if response.status_code == 200:
            print("✅ Отправлено!")
        else:
            print("❌ Ошибка:", response.text)

    except Exception as e:
        print("❌ Ошибка сети:", e)


# ====== СЛУЧАЙНОЕ ВРЕМЯ ======
def generate_daily_time():
    # между 08:00 и 10:00
    hour = random.choice([8, 9, 9, 10])
    minute = random.randint(0, 59)
    return hour, minute


# ====== ЦИКЛ ======
if __name__ == "__main__":
    print("🚀 Bot Level 2 (Almaty TZ) запущен")

    while True:
        now = datetime.now(ALMATY_TZ)
        today = now.date()

        global target_time

        # новое время каждый день
        if last_sent_date != today:
            target_time = generate_daily_time()
            print(f"⏰ Сегодня отправка в: {target_time[0]:02d}:{target_time[1]:02d}")

        # проверка времени
        if target_time:
            if now.hour == target_time[0] and now.minute == target_time[1]:
                if last_sent_date != today:
                    send_whatsapp_message()
                    last_sent_date = today

                    print("✅ Сообщение отправлено, жду завтра...")
                    time.sleep(65)

        time.sleep(20)
