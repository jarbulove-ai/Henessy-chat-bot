import os
import time
import requests
import random

# --- ВСТАВЛЯЕМ ВАШИ ДАННЫЕ НАПРЯМУЮ В КАВЫЧКАХ ---
ID_INSTANCE = "7107646143"
API_TOKEN_INSTANCE = "7b6363cae6d644afafaddef92bdb3f0512915c22d5cf425dba"
CHAT_ID = "77023958782-1590737066@g.us"
# ------------------------------------------------

# Время отправки (4:00 UTC — это 09:00 утра по времени Алматы)
SEND_HOUR = 4
SEND_MINUTE = 0

def get_fact_of_the_day():
    """Получение случайного факта дня"""
    try:
        response = requests.get("https://russiandict.ru", timeout=5)
        if response.status_code == 200:
            return response.json().get("fact", "Каждое утро приносит новые возможности!")
    except Exception:
        pass
    
    # Резервные факты, если у Франкфурта нет связи с сайтом фактов
    local_facts = [
        "Медведи-гризли могут бегать так же быстро, как и обычные лошади!",
        "Земля — единственная планета, не названная в честь бога.",
        "Улитка может спать три года подряд, если условия неблагоприятны.",
        "Зрачки у коз квадратные, что помогает им лучше видеть хищников."
    ]
    return random.choice(local_facts)

def send_whatsapp_message():
    """Отправка сообщения в группу через прямой IP/домен Green API"""
    # Мы используем прямой глобальный адрес шлюза
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
    headers = {
        'Content-Type': 'application/json',
        'Host': '://green-api.com'
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            print(f"Успешно отправлено! Ответ сервера: {response.json()}")
        else:
            print(f"Ошибка сервера Green API: Код {response.status_code}, Текст: {response.text}")
    except Exception as e:
        print(f"Попытка через запасной сервер из-за сбоя сети Render: {e}")
        # Если основной адрес заблокирован, пробуем напрямую через ваш хост-сервер 7107
        try:
            alt_url = f"https://greenapi.com{ID_INSTANCE}/sendMessage/{API_TOKEN_INSTANCE}"
            response = requests.post(alt_url, json=payload, headers={'Content-Type': 'application/json'}, timeout=15)
            print(f"Успешно отправлено через резервный шлюз! Ответ: {response.json()}")
        except Exception as alt_e:
            print(f"Критическая ошибка сети хостинга: {alt_e}")

if __name__ == "__main__":
    print("Тестовый запуск бота...")
    send_whatsapp_message()

    # Основной цикл закомментирован для проверки:
    # while True:
    #     current_time = time.gmtime() 
    #     
    #     if current_time.tm_hour == SEND_HOUR and current_time.tm_min == SEND_MINUTE:
    #         send_whatsapp_message()
    #         time.sleep(65)
    #     
    #     time.sleep(30)
