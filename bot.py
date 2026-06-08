import requests
import random

# ====== НАСТРОЙКИ GREEN API ======
ID_INSTANCE = "7107646143"
API_TOKEN = "7b6363cae6d644afafaddef92bdb3f0512915c22d5cf425dba"

CHAT_ID = "77023958782-1590737066@g.us"

BASE_URL = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"


def get_fact_of_the_day():
    try:
        # нормального публичного API тут нет, оставим fallback
        return random.choice([
            "Медведи-гризли могут бегать так же быстро, как лошади.",
            "Земля — единственная планета, не названная в честь бога.",
            "Улитка может спать до 3 лет при плохих условиях.",
            "В космосе металл может свариваться без нагрева."
        ])
    except Exception:
        return "Каждый день — это новая возможность."


def send_whatsapp_message():
    fact = get_fact_of_the_day()

    message_text = (
        "☀️ *Доброе утро, банда!*\n\n"
        f"🤖 Рубрика *«Факт дня»*:\n"
        f"_{fact}_\n\n"
        "Прекрасного вам дня ☕"
    )

    payload = {
        "chatId": CHAT_ID,
        "message": message_text
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        print("📤 Отправка сообщения...")

        response = requests.post(
            BASE_URL,
            json=payload,
            headers=headers,
            timeout=15
        )

        if response.status_code == 200:
            print("✅ Успешно отправлено!")
            print(response.json())
        else:
            print("❌ Ошибка Green API:")
            print(response.status_code)
            print(response.text)

    except Exception as e:
        print(f"❌ Ошибка сети: {e}")


if __name__ == "__main__":
    print("🚀 Запуск бота...")
    send_whatsapp_message()
