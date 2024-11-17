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
            
            # Получаем данные пользователя
            username = contact.get('username') or contact.get('telegram_id', 'Не указано')
            name = contact.get('name', 'Не указано')
            last_message = contact.get('last_message', 'Нет сообщения')
            
            # Обрабатываем разные типы событий
            if event_type == 'bot_block':
                message = f"""
🚫 <b>Пользователь заблокировал бота</b>

👤 Имя: {name}
📱 Telegram: {username}
⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            elif event_type == 'new_subscriber':
                message = f"""
✅ <b>Пользователь возобновил работу с ботом</b>

👤 Имя: {name}
📱 Telegram: {username}
⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            elif event_type == 'run_custom_flow':
                message = f"""
🔄 <b>Пользователь сделал выбор</b>

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
            bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode='HTML')
            print("Message sent successfully")
            
        return jsonify({'status': 'success', 'message': 'Webhook processed'})
    except Exception as e:
        print(f"\n=== ERROR ===")
        print(f"Error in webhook: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'status': 'error', 'error': str(e)}), 500
