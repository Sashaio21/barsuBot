from createBot import bot
from aiogram import Dispatcher
from aiogram.types import Message
from keyboards.keyboardsNotInline import greet_kb
# from keyboards.inlinebutton import choice


async def start_command(message: Message):
    await bot.send_message(chat_id=message.chat.id,text="Привет! 👋", reply_markup=greet_kb)

async def cmd_echo2(message: Message):
    await message.delete()

def register_client_heandlers(dp : Dispatcher):
    dp.register_message_handler(start_command, commands='start')
    dp.register_message_handler(cmd_echo2)