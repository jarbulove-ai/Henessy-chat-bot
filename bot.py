import os
import time
import requests
import random

# Данные вашей группы
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
    # ВОТ ЭТА СТРОКА: sendMessage теперь написан правильно, с большой буквы M
    url = "https://green-api.com"
    
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
        print("Отправка прямого текстового запроса...")
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            print(f"Успешно отправлено! Ответ сервера: {response.json()}")
        else:
            print(f"Ошибка сервера Green API: Код {response.status_code}, Текст: {response.text}")
    except Exception as e:
        print(f"Критическая ошибка сети хостинга: {e}")

if __name__ == "__main__":
    print("Тестовый запуск бота...")
    send_whatsapp_message()
