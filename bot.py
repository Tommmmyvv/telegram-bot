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
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    try:
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
            
            # Получаем данные пользователя
            username = contact.get('username', 'Не указано')
            name = contact.get('name', 'Не указано')
            last_message = contact.get('last_message', '')
            
            # Отправляем сообщение только если это выбор опции
            if event_type == 'run_custom_flow' and last_message in ['Модель', 'Чатер']:
                message = f"""
👤 <b>{name}</b> (@{username})
✅ Выбрал: <b>{last_message}</b>
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                
                try:
                    bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode='HTML')
                    print("Message sent successfully")
                except Exception as e:
                    print(f"Error sending message: {str(e)}")
                
        return jsonify({'status': 'success', 'message': 'Webhook processed'})
    except Exception as e:
        print(f"Error in webhook: {str(e)}")
        return jsonify({'status': 'error', 'error': str(e)}), 500
