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
            print("Chat ID:", chat_id)
            print("Message:", message)
            
            try:
                bot.send_message(chat_id, message, parse_mode='HTML')
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
