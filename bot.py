# ... существующий код ...

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    if isinstance(data, list) and len(data) > 0:
        event = data[0]
        contact = event.get('contact', {})
        
        # Получаем основную информацию
        username = contact.get('username', 'Не указано')
        name = contact.get('variables', {}).get('name', 'Не указано')
        event_type = event.get('title')
        
        # Формируем сообщение в зависимости от типа события
        if event_type == 'new_subscriber':
            message = f"""
🎉 <b>Новый подписчик!</b>
👤 Имя: {name}
📱 Telegram: @{username}
⏰ Время: {datetime.fromtimestamp(event.get('date', 0)/1000).strftime('%Y-%m-%d %H:%M:%S')}
"""
        elif event_type == 'run_custom_flow':
            selected_option = contact.get('variables', {}).get('selected_option', 'Не указано')
            message = f"""
🔄 <b>Сделан выбор!</b>
👤 Имя: {name}
📱 Telegram: @{username}
🎯 Выбрал: {selected_option}
⏰ Время: {datetime.fromtimestamp(event.get('date', 0)/1000).strftime('%Y-%m-%d %H:%M:%S')}
"""
        else:
            message = f"""
ℹ️ <b>Новое событие в SendPulse</b>
Тип: {event_type}
👤 Имя: {name}
📱 Telegram: @{username}
⏰ Время: {datetime.fromtimestamp(event.get('date', 0)/1000).strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # Отправляем уведомление в Telegram
        bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode='HTML')
        
    return 'OK'

# ... остальной код ...
