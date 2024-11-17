import os
from flask import Flask, request, jsonify
import telebot
from dotenv import load_dotenv
from datetime import datetime
import json

# Загрузка переменных окружения
load_dotenv()

# Глобальные переменные
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Создание приложения Flask
app = Flask(__name__)

# Создание бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Маршруты
@app.route('/')
def home():
    try:
        if not TELEGRAM_BOT_TOKEN:
            return 'Error: TELEGRAM_BOT_TOKEN not set'
        if not TELEGRAM_CHAT_ID:
            return 'Error: TELEGRAM_CHAT_ID not set'
            
        bot.send_message(TELEGRAM_CHAT_ID, "✅ Бот успешно запущен!")
        return 'Bot is running and telegram message sent successfully!'
    except Exception as e:
        return f'Error: {str(e)}'

@app.route('/test')
def test():
    return jsonify({
        'status': 'ok',
        'telegram_token': bool(TELEGRAM_BOT_TOKEN),
        'chat_id': bool(TELEGRAM_CHAT_ID)
    })

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    try:
        if request.method == 'GET':
            return jsonify({
                'status': 'webhook is working',
                'method': 'GET'
            })
            
        print("\n=== REQUEST INFO ===")
        print("Headers:", dict(request.headers))
        print("Method:", request.method)
        print("Content-Type:", request.content_type)
        
        data = request.json
        print("\n=== WEBHOOK DATA ===")
        print("Raw data:", json.dumps(data, indent=2))
        
        if isinstance(data, list) and len(data) > 0:
            event = data[0]
            contact = event.get('contact', {})
            variables = contact.get('variables', {})
            event_type = event.get('title')
            
            print("\n=== EVENT INFO ===")
            print("Event type:", event_type)
            print("Contact:", json.dumps(contact, indent=2))
            print("Variables:", json.dumps(variables, indent=2))
            
            # Получаем данные пользователя
            username = contact.get('username') or contact.get('telegram_id', 'Не указано')
            name = contact.get('name', 'Не указано')
            last_message = contact.get('last_message', 'Нет сообщения')
            
            print("\n=== USER INFO ===")
            print(f"Username: {username}")
            print(f"Name: {name}")
            print(f"Last message: {last_message}")
            
            # Всегда отправляем сообщение для отладки
            message = f"""
📝 <b>Новое событие в боте</b>

Тип события: {event_type}
👤 Имя: {name}
📱 Telegram: {username}
💬 Сообщение: {last_message}
🔄 Переменные: {json.dumps(variables, ensure_ascii=False)}
⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                
            print("\n=== SENDING MESSAGE ===")
            print("Chat ID:", TELEGRAM_CHAT_ID)
            print("Message:", message)
            
            try:
                bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode='HTML')
                print("Message sent successfully")
            except Exception as e:
                print(f"Error sending message: {str(e)}")
                
        return jsonify({'status': 'success', 'message': 'Webhook processed'})
    except Exception as e:
        print(f"\n=== ERROR ===")
        print(f"Error in webhook: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
