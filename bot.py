import os
from flask import Flask, request, jsonify
import telebot
from dotenv import load_dotenv
from datetime import datetime
import json

# Инициализация всех компонентов
def create_app():
    # Загрузка переменных окружения
    load_dotenv()
    
    # Создание Flask приложения
    app = Flask(__name__)
    
    # Инициализация бота
    bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    # Определение маршрутов
    @app.route('/')
    def home():
        try:
            if not os.getenv('TELEGRAM_BOT_TOKEN'):
                return 'Error: TELEGRAM_BOT_TOKEN not set'
            if not chat_id:
                return 'Error: TELEGRAM_CHAT_ID not set'
                
            bot.send_message(chat_id, "✅ Бот успешно запущен!")
            return 'Bot is running and telegram message sent successfully!'
        except Exception as e:
            return f'Error: {str(e)}'

    @app.route('/test')
    def test():
        return jsonify({
            'status': 'ok',
            'telegram_token': bool(os.getenv('TELEGRAM_BOT_TOKEN')),
            'chat_id': bool(chat_id)
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
                
                # Получаем данные пользователя
                username = contact.get('username') or contact.get('telegram_id', 'Не указано')
                name = contact.get('name', 'Не указано')
                last_message = contact.get('last_message', 'Нет сообщения')
                
                # Обрабатываем все возможные события
                if event_type in ['new_subscriber', 'bot_unblock', 'unsubscribe', 'bot_block']:
                    action_map = {
                        'new_subscriber': '✅ подписался на бота',
                        'bot_unblock': '🔓 разблокировал бота',
                        'unsubscribe': '❌ отписался от бота',
                        'bot_block': '🚫 заблокировал бота'
                    }
                    
                    message = f"""
<b>Действие пользователя</b>
👤 Пользователь {action_map.get(event_type)}

Имя: {name}
Telegram: {username}
Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                elif event_type == 'run_custom_flow':
                    message = f"""
🔄 <b>Сделан выбор в боте</b>

👤 Имя: {name}
📱 Telegram: {username}
💬 Выбор: {last_message}
🔄 Переменные: {json.dumps(variables, ensure_ascii=False)}
⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                elif event_type == 'incoming_message' and last_message != '/start':
                    message = f"""
📝 <b>Новое сообщение</b>

👤 Имя: {name}
📱 Telegram: {username}
💬 Сообщение: {last_message}
⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                else:
                    print(f"Skipping event: {event_type}")
                    return jsonify({'status': 'skipped'})
                    
                print("\n=== SENDING MESSAGE ===")
                print(message)
                bot.send_message(chat_id, message, parse_mode='HTML')
                print("Message sent successfully")
                
            return jsonify({'status': 'success', 'message': 'Webhook processed'})
        except Exception as e:
            print(f"\n=== ERROR ===")
            print(f"Error in webhook: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return jsonify({'status': 'error', 'error': str(e)}), 500

    return app

# Создаем приложение
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
