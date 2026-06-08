import requests

CHAT_ID = "77023958782-1590737066@g.us"

def send_whatsapp_message():
    url = "https://7107.api.greenapi.com/waInstance7107646143/sendMessage/7b6363cae6d644afafaddef92bdb3f0512915c22d5cf425dba"

    payload = {
        "chatId": CHAT_ID,
        "message": "Тестовое сообщение от бота"
    }

    response = requests.post(url, json=payload)

    print("Код:", response.status_code)
    print("Ответ:", response.text)
