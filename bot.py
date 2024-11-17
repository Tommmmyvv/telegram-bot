@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Логируем заголовки запроса
        print("Headers:", dict(request.headers))
        
        # Логируем сырые данные
        raw_data = request.get_data().decode('utf-8')
        print("Raw data:", raw_data)
        
        data = request.json
        print("Parsed JSON:", json.dumps(data, indent=2))
        
        if isinstance(data, list) and len(data) > 0:
            event = data[0]
            print("Event:", json.dumps(event, indent=2))
            
            contact = event.get('contact', {})
            print("Contact:", json.dumps(contact, indent=2))
            
            variables = contact.get('variables', {})
            print("Variables:", json.dumps(variables, indent=2))
            
            event_type = event.get('title')
            print("Event type:", event_type)
            
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
                
                print(f"Sending message to {TELEGRAM_CHAT_ID}: {message}")
                bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode='HTML')
                print("Message sent successfully")
            else:
                print(f"Skipping event type: {event_type}")
            
        return jsonify({'status': 'success', 'message': 'Webhook processed'})
    except Exception as e:
        print(f"Error in webhook: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'status': 'error', 'error': str(e)}), 500
