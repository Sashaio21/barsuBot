from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

buttonToKnow = KeyboardButton('Узнать расписание')
buttonReset = KeyboardButton('Сбросить') 

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.add(buttonToKnow).add(buttonReset)