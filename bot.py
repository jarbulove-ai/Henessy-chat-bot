import os
import time
import requests

# 1. Настройки авторизации Green API
# В облаке мы будем брать эти данные из переменных окружения (безопасный способ)
ID_INSTANCE = os.getenv("7107646143")#, "ВАШ_ID_ЕСЛИ_ТЕСТИРУЕТЕ_ЛОКАЛЬНО"
API_TOKEN_INSTANCE = os.getenv("7b6363cae6d644afafaddef92bdb3f0512915c22d5cf425dba")#, "ВАШ_ТОКЕН_ЕСЛИ_ТЕСТИРУЕТЕ_ЛОКАЛЬНО")
CHAT_ID = os.getenv("77023958782-1590737066@g.us")#, "ID_ВАШЕЙ_ГРУППЫ@g.us")

# Время отправки (по часовому поясу сервера, обычно это UTC)
SEND_HOUR = 5  # Например, 5:00 UTC — это 8:00 по Москве / 10:00 по Алматы
SEND_MINUTE = 0

def get_fact_of_the_day():
    """Получение случайного факта дня"""
    try:
        response = requests.get("https://russiandict.ru", timeout=5)
        if response.status_code == 200:
            return response.json().get("fact", "Каждое утро приносит новые возможности!")
    except Exception as e:
        print(f"Ошибка получения факта: {e}")
    return "Земля — единственная планета, не названная в честь бога."

def send_whatsapp_message():
    """Отправка сообщения в группу через Green API"""
    url = f"https://green-api.com{ID_INSTANCE}/sendMessage/{API_TOKEN_INSTANCE}"
    
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
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"Успешно отправлено! Ответ сервера: {response.json()}")
        else:
            print(f"Ошибка сервера Green API: Код {response.status_code}, Текст: {response.text}")
    except Exception as e:
        print(f"Не удалось отправить запрос: {e}")

if __name__ == "__main__":
    print("Бот успешно запущен в облаке и вошел в бесконечный цикл ожидания...")
    
 """while True:
        # Получаем текущее время сервера
        current_time = time.gmtime() 
        
        if current_time.tm_hour == SEND_HOUR and current_time.tm_min == SEND_MINUTE:
            send_whatsapp_message()
            # Засыпаем на 65 секунд, чтобы исключить повторную отправку в эту же минуту
            time.sleep(65)
        
        # Проверяем время каждые 30 секунд
        time.sleep(30)"""
if __name__ == "__main__":
    print("Тестовый запуск бота...")
    send_whatsapp_message()

