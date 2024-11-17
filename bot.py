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
Installing collected packages: werkzeug, urllib3, python-dotenv, MarkupSafe, itsdangerous, idna, gunicorn, click, charset-normalizer, certifi, requests, Jinja2, pyTelegramBotAPI, flask
Successfully installed Jinja2-3.1.4 MarkupSafe-3.0.2 certifi-2024.8.30 charset-normalizer-3.4.0 click-8.1.7 flask-2.0.1 gunicorn-20.1.0 idna-3.10 itsdangerous-2.2.0 pyTelegramBotAPI-4.12.0 python-dotenv-0.19.0 requests-2.32.3 urllib3-2.2.3 werkzeug-2.0.1
[notice] A new release of pip is available: 24.0 -> 24.3.1
[notice] To update, run: pip install --upgrade pip
==> Uploading build...
==> Build uploaded in 7s
==> Build successful 🎉
==> Deploying...
==> No open ports detected, continuing to scan...
==> Docs on specifying a port: https://render.com/docs/web-services#port-binding
