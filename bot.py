import os
from flask import Flask, request, jsonify
import telebot
from dotenv import load_dotenv
from datetime import datetime
import json

# Сначала загружаем переменные окружения
load_dotenv()

# Создаем приложение Flask и бота
app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Определяем маршруты
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

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    try:
        if request.method == 'GET':
            return jsonify({
                'status': 'webhook is working',
                'method': 'GET'
            })
            
        data = request.json
        print("Received webhook data:", json.dumps(data, indent=2))
        
        if isinstance(data, list) and len(data) > 0:
            event = data[0]
            contact = event.get('contact', {})
            variables = contact.get('variables', {})
            event_type = event.get('title')
            username = contact.get('username') or contact.get('telegram_id', 'Не указано')
            name = contact.get('name', 'Не указано')
            
            # Формируем сообщение в зависимости от типа события
            if event_type == 'run_custom_flow':
                selected_option = variables.get('$selected_option', 'Не указано')
                message = f"""
🔔 <b>Новая заявка!</b>

👤 Имя: {name}
📱 Telegram: {username}
🎯 Выбрал: {selected_option}
⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            elif event_type == 'incoming_message':
                last_message = contact.get('last_message', 'Нет сообщения')
                if last_message != '/start':  # Игнорируем команду /start
                    message = f"""
✍️ <b>Пользователь ввел:</b>

👤 Имя: {name}
📱 Telegram: {username}
💬 Сообщение: {last_message}
⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                else:
                    return jsonify({'status': 'skipped start command'})
            else:
                return jsonify({'status': 'skipped other event'})
            
            # Отправляем сообщение в Telegram
            print(f"Sending message: {message}")
            bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode='HTML')
            print("Message sent successfully")
            
        return jsonify({'status': 'success', 'message': 'Webhook processed'})
    except Exception as e:
        print(f"Error in webhook: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
