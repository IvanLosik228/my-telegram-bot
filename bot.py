from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackContext, CallbackQueryHandler

import os

TOKEN = 7635202405:AAE-tCdzreZG2ywTXoz-dJfYSWnuz3rS874  # <-- вставь сюда свой токен

bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

# Старт
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Описание услуги", callback_data='desc')],
        [InlineKeyboardButton("Оплатить", url='https://example.com/pay')],
        [InlineKeyboardButton("Техподдержка", url='https://t.me/your_support_bot')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Привет! Выбери действие:", reply_markup=reply_markup)

# Обработка кнопок
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'desc':
        query.edit_message_text(text="Описание услуги: это очень полезная штука!")

# Привязка хендлеров
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(button_handler))

# Вебхук обработка
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

# Проверка запуска
@app.route('/')
def index():
    return "Бот работает!"

if __name__ == '__main__':
    app.run(debug=True)