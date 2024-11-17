import os
from flask import Flask, request, jsonify
import telebot
from dotenv import load_dotenv
from datetime import datetime
import json

# Сначала загружаем переменные окружения
load_dotenv()

# Затем создаем приложение Flask и бота
app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Теперь определяем все маршруты
@app.route('/')
def home():
    try:
        if not os.getenv('TELEGRAM_BOT_TOKEN'):
            return 'Error: TELEGRAM_BOT_TOKEN not set'
        if not os.getenv('TELEGRAM_CHAT_ID'):
            return 'Error: TELEGRAM_CHAT_ID not set'
            
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

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        print("Parsed JSON data:", json.dumps(data, indent=2))
        
        if isinstance(data, list) and len(data) > 0:
            event = data[0]
            contact = event.get('contact', {})
            variables = contact.get('variables', {})
            event_type = event.get('title')
            last_message = contact.get('last_message', 'Нет сообщения')
            
            if event_type == 'run_custom_flow':
                username = contact.get('username', 'Не указано')
                name = variables.get('$name', 'Не указано')
                selected_option = variables.get('$selected_option', 'Не указано')
                current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                message = f"""
🔔 <b>Новая заявка!</b>

👤 Имя: {name}
📱 Telegram: @{username}
🎯 Выбрал: {selected_option}
⏰ Время: {current_datetime}
"""
                
                print(f"Preparing to send message: {message}")
                bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode='HTML')
                print("Message sent successfully")
            
        return jsonify({'status': 'success', 'message': 'Webhook processed'})
    except Exception as e:
        print(f"Error in webhook: {str(e)}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({
        'error': str(error),
        'status': 'error'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
