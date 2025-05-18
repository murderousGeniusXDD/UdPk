import telebot
from telebot import types
import os
import tkinter as tk
import pyautogui

# pip install telebot
#pip install pyautogui
#pip install tkinter

token = 'Your_bot_token'
allowed_chat_id = 'You_chat_id'  # Разрешенный chat_id

bot = telebot.TeleBot(token)

def is_authorized(chat_id):
    return str(chat_id) == allowed_chat_id

@bot.message_handler(commands=['screen'])
def screen(message):
    if not is_authorized(message.chat.id):
        bot.send_message(message.chat.id, "Извините, этот бот не для вас.")
        return

    # Создаем скриншот и сохраняем его в файл
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')

    # Открываем файл скриншота для отправки
    with open('screenshot.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption="Твой скриншот!")

@bot.message_handler(commands=['start'])
def start(message):
    if not is_authorized(message.chat.id):
        bot.send_message(message.chat.id, "Извините, этот бот не для вас.")
        return

    markup = types.InlineKeyboardMarkup()
    
    # Добавляем кнопки
    item1 = types.InlineKeyboardButton("Скриншот", callback_data='button1')
    item2 = types.InlineKeyboardButton("Выключить", callback_data='button2')
    item3 = types.InlineKeyboardButton("Отправить Сообщение", callback_data='button3')
    markup.add(item1, item2, item3)
    
    # Отправляем сообщение с клавиатурой
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if not is_authorized(call.message.chat.id):
        bot.send_message(call.message.chat.id, "Извините, этот бот не для вас.")
        return

    if call.data == 'button1':
        screen(call.message)
    elif call.data == 'button2':
        bot.send_message(call.message.chat.id, "Выключение...")
        os.system("shutdown /s /t 30")
    elif call.data == "button3":
        bot.send_message(call.message.chat.id, "Пожалуйста, введите сообщение для отображения:")
        bot.register_next_step_handler(call.message, receive_message)

def receive_message(message):
    if not is_authorized(message.chat.id):
        bot.send_message(message.chat.id, "Извините, этот бот не для вас.")
        return

    # Получаем текст сообщения от пользователя
    message_text = message.text
    show_message(message_text)

def show_message(message):
    # Создаем главное окно
    root = tk.Tk()
    root.title("Сообщение")
    
    # Устанавливаем окно поверх всех
    root.attributes('-topmost', True)
    
    # Создаем метку с сообщением
    label = tk.Label(root, text=message, font=("Arial", 16))
    label.pack(padx=20, pady=20)
    
    # Устанавливаем таймер на закрытие окна через 60 секунд
    def close_window():
        root.destroy()
    
    # Закрываем окно через 60 секунд
    root.after(60000, close_window)

    # Запускаем главный цикл
    root.mainloop()

bot.infinity_polling()