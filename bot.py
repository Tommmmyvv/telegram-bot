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
            print("Variables:", json.dumps(variables, indent=2))
            print("Contact:", json.dumps(contact, indent=2))
            
            # Получаем данные пользователя
            username = contact.get('username') or contact.get('telegram_id', 'Не указано')
            name = contact.get('name', 'Не указано')
            last_message = contact.get('last_message', 'Нет сообщения')
            
            # Отправляем сообщение для любого события, кроме /start
            if last_message != '/start':
                message = f"""
📝 <b>Новое событие в боте</b>

👤 Имя: {name}
📱 Telegram: {username}
📋 Тип события: {event_type}
💬 Последнее сообщение: {last_message}
🔄 Переменные: {json.dumps(variables, ensure_ascii=False)}
⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                
                print("\n=== SENDING MESSAGE ===")
                print(message)
                bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode='HTML')
                print("Message sent successfully")
            else:
                print("Skipping /start command")
            
        return jsonify({'status': 'success', 'message': 'Webhook processed'})
    except Exception as e:
        print(f"\n=== ERROR ===")
        print(f"Error in webhook: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'status': 'error', 'error': str(e)}), 500
