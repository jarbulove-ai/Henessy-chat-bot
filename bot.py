import time
import requests
import random
from datetime import datetime, timedelta, timezone

print("=== ФАЙЛ ЗАПУЩЕН ===", flush=True)

# ====== НАСТРОЙКИ ======
GREEN_API_ID = "7107646143"
GREEN_API_TOKEN = "7b6363cae6d644afafaddef92bdb3f0512915c22d5cf425dba"
CHAT_ID = "77023958782-1590737066@g.us"

BASE_URL = f"https://api.green-api.com/waInstance{GREEN_API_ID}/sendMessage/{GREEN_API_TOKEN}"

# ====== ЧАСОВОЙ ПОЯС АЛМАТЫ ======
ALMATY_TZ = timezone(timedelta(hours=5))

# ====== СОСТОЯНИЕ ======
last_sent_date = None
scheduled_date = None
scheduled_datetime = None


# ====== ФАКТ ДНЯ ======
def get_fact_of_the_day():
    facts = [
        "Осьминог имеет три сердца.",
        "Кошки не чувствуют сладкий вкус.",
        "В космосе нет звука.",
        "Мозг использует около 20% энергии тела.",
        "Сердце человека бьётся около 100 000 раз в день.",
        "У жирафов такое же количество шейных позвонков, как у человека.",
        "Мёд может храниться десятилетиями и не портиться."
    ]
    return random.choice(facts)


# ====== ПОГОДА ======
def get_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": 43.2389,
            "longitude": 76.8897,
            "current_weather": True
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        temp = data["current_weather"]["temperature"]
        wind = data["current_weather"]["windspeed"]

        return f"🌤 Алматы: {temp}°C, ветер {wind} м/с"

    except Exception as e:
        print(f"Ошибка получения погоды: {e}", flush=True)
        return "🌤 Погода временно недоступна"


# ====== ТЕКСТ СООБЩЕНИЯ ======
def build_message():
    fact = get_fact_of_the_day()
    weather = get_weather()

    greetings = [
        "☀️ *Доброе утро, банда!*",
        "😄 *Просыпаемся, легенды!*",
        "🌿 *Спокойное утро начинается...*"
    ]

    header = random.choice(greetings)

    return (
        f"{header}\n\n"
        f"🤖 *Факт дня:*\n"
        f"_{fact}_\n\n"
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

        # Если время уже прошло — переносим на завтра
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

        # Защита от двойной отправки
        time.sleep(65)

    time.sleep(20)
