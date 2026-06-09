import json
import base64
import os
import time
import requests
import random
from datetime import datetime, timedelta, timezone

print("=== ФАЙЛ ЗАПУЩЕН ===", flush=True)

# ====== ENV ======
GREEN_API_ID = os.getenv("GREEN_API_ID")
GREEN_API_TOKEN = os.getenv("GREEN_API_TOKEN")
CHAT_ID = os.getenv("GROUP_CHAT_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

GITHUB_OWNER = "jarbulove-ai"
GITHUB_REPO = "Henessy-chat-bot"

BASE_URL = f"https://api.green-api.com/waInstance{GREEN_API_ID}/sendMessage/{GREEN_API_TOKEN}"

# ====== функции GitHub ======
def load_state():
    try:
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/state.json"

        headers = {
            "Authorization": f"token {GITHUB_TOKEN}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("⚠️ Не удалось загрузить state.json")
            return {
                "used_facts": [],
                "used_useless_facts": [],
                "used_jokes": [],
                "used_questions": []
            }, None

        data = response.json()

        content = base64.b64decode(
            data["content"]
        ).decode("utf-8")

        return json.loads(content), data["sha"]

    except Exception as e:
        print(f"Ошибка загрузки state.json: {e}")

        return {
            "used_facts": [],
            "used_useless_facts": [],
            "used_jokes": [],
            "used_questions": []
        }, None


def save_state(state, sha):
    try:
        if sha is None:
            return

        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/state.json"

        headers = {
            "Authorization": f"token {GITHUB_TOKEN}"
        }

        content = base64.b64encode(
            json.dumps(
                state,
                ensure_ascii=False,
                indent=2
            ).encode("utf-8")
        ).decode()

        payload = {
            "message": "Update bot memory",
            "content": content,
            "sha": sha
        }

        response = requests.put(
            url,
            headers=headers,
            json=payload
        )

        print(
            f"💾 State saved: {response.status_code}",
            flush=True
        )

    except Exception as e:
        print(f"Ошибка сохранения state.json: {e}")

# ====== ЧАСОВОЙ ПОЯС АЛМАТЫ ======
ALMATY_TZ = timezone(timedelta(hours=5))

# ====== СОСТОЯНИЕ ======
last_sent_date = None
scheduled_date = None
scheduled_datetime = None


# ====== ФАКТЫ ======
def load_items(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [
                line.strip()
                for line in f
                if line.strip()
            ]
    except Exception as e:
        print(f"Ошибка чтения {filename}: {e}", flush=True)
        return []


def get_unique_item(source_file, state_key):
    items = load_items(source_file)

    if not items:
        return "Данные временно недоступны."

    state, sha = load_state()

    used = set(
        state.get(state_key, [])
    )

    available = [
        item
        for item in items
        if item not in used
    ]

    if not available:
        print(
            f"♻️ Все записи из {source_file} использованы. Новый круг.",
            flush=True
        )

        state[state_key] = []

        save_state(state, sha)

        available = items

    selected = random.choice(available)

    state[state_key].append(selected)

    save_state(state, sha)

    return selected


def get_fact_of_the_day():
    return get_unique_item(
        "facts.txt",
        "used_facts"
    )


def get_useless_fact():
    return get_unique_item(
        "useless_facts.txt",
        "used_useless_facts"
    )


def get_joke_of_the_day():
    return get_unique_item(
        "jokes.txt",
        "used_jokes"
    )


def get_question_of_the_day():
    return get_unique_item(
        "questions.txt",
        "used_questions"
    )


def get_friday_index():
    today = datetime.now(ALMATY_TZ)

    days_until_friday = (4 - today.weekday()) % 7

    if days_until_friday == 0:
        return "🍺 Индекс пятницы: СЕГОДНЯ ПЯТНИЦА!"
    elif days_until_friday == 1:
        return "🍺 До пятницы остался 1 день."
    else:
        return f"🍺 До пятницы осталось {days_until_friday} дн."


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
    fact = get_fact_of_the_day()
    useless_fact = get_useless_fact()
    weather = get_weather()
    joke = get_joke_of_the_day()
    question = get_question_of_the_day()
    friday_index = get_friday_index()
    
    greetings = [
        "☀️ *Доброе утро, банда!*",
        "😄 *Просыпаемся, легенды!*",
        "🌿 *Спокойное утро начинается...*"
    ]

    header = random.choice(greetings)

    return (
        f"{header}\n\n"
        f"🧠 *Интересный факт дня:*\n"
        f"{fact}\n\n"
        f"🤯 *Бесполезное знание дня:*\n"
        f"{useless_fact}\n\n"
        f"😂 *Шутка дня:*\n"
        f"{joke}\n\n"
        f"🤔 *Вопрос дня:*\n"
        f"{question}\n\n"
        f"{weather}\n\n"
        f"{friday_index}\n\n"
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

#send_whatsapp_message()

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
