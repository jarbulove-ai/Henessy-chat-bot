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
target_time = None


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
            "latitude": 43.2389,  # Алматы
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
        f"🤖 *Факт дня:*\n_{fact}_\n\n"
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


# ====== СЛУЧАЙНОЕ ВРЕМЯ НА ДЕНЬ ======
def generate_daily_time():
    hour = random.choice([8, 9, 9, 10])
    minute = random.randint(0, 59)
    return hour, minute


print("🚀 BOT STARTED", flush=True)

while True:
    now = datetime.now(ALMATY_TZ)
    today = now.date()

    print(f"💓 BOT LOOP TICK | {now.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)

    # Генерируем время только один раз в день
    if scheduled_date != today:
        target_time = generate_daily_time()
        scheduled_date = today

        print(
            f"⏰ Сегодня отправка в: "
            f"{target_time[0]:02d}:{target_time[1]:02d}",
            flush=True
        )

    # Проверяем время отправки
    if (
        target_time
        and now.hour == target_time[0]
        and now.minute == target_time[1]
        and last_sent_date != today
    ):
        send_whatsapp_message()
        last_sent_date = today

        print("✅ Сообщение отправлено. Жду завтра.", flush=True)

        # чтобы не отправить дважды за одну минуту
        time.sleep(65)

    time.sleep(20)
