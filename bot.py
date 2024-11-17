import os
from flask import Flask, request, jsonify
import telebot
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

@app.route('/')
def home():
    try:
        # Проверяем наличие переменных окружения
        if not os.getenv('TELEGRAM_BOT_TOKEN'):
            return 'Error: TELEGRAM_BOT_TOKEN not set'
        if not os.getenv('TELEGRAM_CHAT_ID'):
            return 'Error: TELEGRAM_CHAT_ID not set'
            
        # Пробуем отправить тестовое сообщение
        bot.send_message(TELEGRAM_CHAT_ID, "✅ Бот успешно запущен!")
        return 'Bot is running and telegram message sent successfully!'
    except Exception as e:
        return f'Error: {str(e)}'

@app.route('/test')
def test():
    return jsonify({
        'status': 'ok',
        'telegram_token': bool(os.getenv('TELEGRAM_BOT_TOKEN')),
        'chat_id': bool(os.getenv('TELEGRAM_CHAT_ID')),
        'token_value': os.getenv('TELEGRAM_BOT_TOKEN')[:10] + '...' if os.getenv('TELEGRAM_BOT_TOKEN') else None,
        'chat_id_value': os.getenv('TELEGRAM_CHAT_ID')
    })

# Добавим обработчик ошибок
@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({
        'error': str(error),
        'status': 'error'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
