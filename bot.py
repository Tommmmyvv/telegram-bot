@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    if isinstance(data, list) and len(data) > 0:
        event = data[0]
        contact = event.get('contact', {})
        variables = contact.get('variables', {})
        event_type = event.get('title')  # Добавили эту строку
        
        # Получаем значения из существующих переменных
        username = contact.get('username', 'Не указано')
        name = variables.get('$name', 'Не указано')
        selected_option = variables.get('$selected_option', 'Не указано')
        current_datetime = variables.get('$current_datetime', 'Не указано')
        
        # Добавим логирование для отладки
        print(f"Received event: {event_type}")
        print(f"Variables: {variables}")
        
        # Формируем сообщение в зависимости от типа события
        if event_type == 'new_subscriber':
            message = f"""
🎉 <b>Новый подписчик в {variables.get('$bot_name', 'боте')}</b>
👤 Имя: {name}
📱 Telegram: @{username}
⏰ Время: {current_datetime}
"""
        elif event_type == 'incoming_message':
            message = f"""
✍️ <b>Пользователь ввел имя</b>
👤 Введенное имя: {name}
📱 Telegram: @{username}
⏰ Время: {current_datetime}
"""
        elif event_type == 'run_custom_flow':
            message = f"""
🔄 <b>Сделан выбор!</b>
👤 Имя: {name}
📱 Telegram: @{username}
🎯 Выбрал: {selected_option}
⏰ Время: {current_datetime}
"""
        else:
            message = f"""
ℹ️ <b>Новое событие в боте</b>
📋 Тип события: {event_type}
👤 Имя: {name}
📱 Telegram: @{username}
⏰ Время: {current_datetime}
"""
        
        # Отправляем уведомление в Telegram
        bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode='HTML')
        
    return 'OK'
