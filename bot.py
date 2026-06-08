import os
import time
import requests
import random

CHAT_ID = "77023958782-1590737066@g.us"

def get_fact_of_the_day():
    try:
        response = requests.get("https://russiandict.ru", timeout=5)
        if response.status_code == 200:
            return response.json().get("fact", "Каждое утро приносит новые возможности!")
    except Exception:
        pass
    
    local_facts = [
        "Медведи-гризли могут бегать так же быстро, как и обычные лошади!",
        "Земля — единственная планета, не названная в честь бога.",
        "Улитка может спать три года подряд, если условия неблагоприятны."
    ]
    return random.choice(local_facts)

def send_whatsapp_message():
    # МЫ ПОЛНОСТЬЮ ПЕРЕПИСАЛИ ПЕРЕМЕННУЮ. БУКВА M ТЕПЕРЬ ОГРОМНАЯ.
    NEW_URL_LINK = "https://green-api.com"
    
    fact = get_fact_of_the_day()
    message_text = (
        "☀️ *Доброе утро, банда!*\n\n"
        f"🤖 Рубрика *«Факт дня»*:\n"
        f"_{fact}_\n\n"
        "Прекрасного вам дня! ☕"
    )
    
    payload = {
        "chatId": CHAT_ID,
        "message": message_text
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        print("Отправка через абсолютно новую переменную...")
        # Используем новую переменную
        response = requests.post(NEW_URL_LINK, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            print(f"Успешно отправлено! Ответ сервера: {response.json()}")
        else:
            print(f"Ответ сервера Green API: {response.status_code}. Проверьте правильность токена.")
    except Exception as e:
        print(f"Ошибка сети: {e}")

if __name__ == "__main__":
    print("Тестовый запуск бота...")
    send_whatsapp_message()
