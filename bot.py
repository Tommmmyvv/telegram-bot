import os
from flask import Flask, request
import telebot
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    # Форматируем сообщение из SendPulse
    if 'message' in data:
        message = f"""
📩 <b>Новое сообщение в чате SendPulse</b>

От: {data['message'].get('sender', 'Неизвестно')}
Сообщение: {data['message'].get('text', 'Нет текста')}
Время: {data['message'].get('created_at', 'Не указано')}
"""
    else:
        message = f"📌 Новое уведомление от SendPulse:\n{str(data)}"

    # Отправляем в Telegram
    bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode='HTML')
    return 'OK'

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f"""
✨ Бот готов к работе!
Ваш chat_id: {message.chat.id}

Настройте вебхук в SendPulse на URL:
https://ваш_домен/webhook
""")

if __name__ == '__main__':
    # Запускаем Flask сервер
    app.run(host='0.0.0.0', port=5000)
