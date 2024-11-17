@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        print("Parsed JSON data:", json.dumps(data, indent=2))
        
        if isinstance(data, list) and len(data) > 0:
            event = data[0]
            contact = event.get('contact', {})
            variables = contact.get('variables', {})
            event_type = event.get('title')
            last_message = contact.get('last_message', 'Нет сообщения')
            
            # Отправляем уведомление только при выборе опции
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
                
                print(f"Preparing to send message: {message}")
                bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode='HTML')
                print("Message sent successfully")
            
        return jsonify({'status': 'success', 'message': 'Webhook processed'})
    except Exception as e:
        print(f"Error in webhook: {str(e)}")
        return jsonify({'status': 'error', 'error': str(e)}), 500
