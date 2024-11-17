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
PORT = int(os.environ.get('PORT', 10000))

# Создание приложения Flask
app = Flask(__name__)

# Создание бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@app.route('/')
@app.route('/index')
def home():
    return jsonify({
        'status': 'ok',
        'message': 'Bot is running'
    })

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    try:
        print("\n=== NEW WEBHOOK REQUEST ===")
        print("Method:", request.method)
        print("Headers:", dict(request.headers))
        
        if request.method == 'GET':
            return jsonify({
                'status': 'webhook is working',
                'method': 'GET'
            })
            
        data = request.json
        print("\n=== WEBHOOK DATA ===")
        print("Raw data:", json.dumps(data, indent=2))
        
        if isinstance(data, list) and len(data) > 0:
            event = data[0]
            contact = event.get('contact', {})
            event_type = event.get('title')
            variables = contact.get('variables', {})
            last_message = contact.get('last_message', '')
            
            print("\n=== DETAILED EVENT INFO ===")
            print(f"Event type: {event_type}")
            print(f"Variables: {json.dumps(variables, indent=2)}")
            print(f"Last message: {last_message}")
            print(f"Contact info: {json.dumps(contact, indent=2)}")
            
            # Получаем данные пользователя
            username = contact.get('username', 'Не указано')
            name = contact.get('name', 'Не указано')
            
            # Проверяем выбор пользователя
            if last_message in ['Модель', 'Чатер']:
                message = f"""
👤 <b>{name}</b> (@{username})
✅ Выбрал: <b>{last_message}</b>
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                
                print("\n=== SENDING MESSAGE ===")
                print(f"Chat ID: {TELEGRAM_CHAT_ID}")
                print(f"Message: {message}")
                
                try:
                    bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode='HTML')
                    print("Message sent successfully")
                except Exception as e:
                    print(f"Error sending message: {str(e)}")
            else:
                print(f"No selection found in message: {last_message}")
                
        return jsonify({'status': 'success', 'message': 'Webhook processed'})
    except Exception as e:
        print(f"\n=== ERROR ===")
        print(f"Error in webhook: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
