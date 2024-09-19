import json
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


keyboard = [[InlineKeyboardButton(text="Студент", callback_data="student"),InlineKeyboardButton(text="Преподаватель", callback_data="teacher")], [InlineKeyboardButton(text="Отмена", callback_data="cancel")]]
firstKB = InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_button(listButton, count_row = 3, count = 0):
    keyboard = []
    
    while count!=len(listButton):
        OneRow = []
        lastRow = []
        if len(listButton) - count >= count_row:
            for i in range(count_row):
                # print("1" +listButton[count])
                OneRow.append(InlineKeyboardButton(text=listButton[count], callback_data=count))
                count+=1
        else:
            for i in range(len(listButton) - count):
                lastRow.append(InlineKeyboardButton(text=listButton[count], callback_data=count))
                count+=1
            keyboard.append(lastRow)
            break
        keyboard.append(OneRow)
    keyboard.append([InlineKeyboardButton(text="Отмена", callback_data="cancel")])
    choice = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return choice