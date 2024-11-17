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
        print("\n=== NEW WEBHOOK REQUEST ===")
        print("Method:", request.method)
        print("Headers:", dict(request.headers))
        
        if request.method == 'GET':
            return jsonify({
                'status': 'webhook is working',
                'method': 'GET'
            })
            
        # Проверяем наличие данных
        if not request.is_json:
            print("Error: Not JSON request")
            return jsonify({'status': 'error', 'message': 'Not JSON'}), 400
            
        data = request.json
        print("\n=== WEBHOOK DATA ===")
        print("Raw data:", json.dumps(data, indent=2))
        
        if not isinstance(data, list) or len(data) == 0:
            print("Error: Invalid data format")
            return jsonify({'status': 'error', 'message': 'Invalid data format'}), 400
            
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
        
        # Проверяем все возможные места, где может быть выбор
        print("\n=== CHECKING SELECTI
