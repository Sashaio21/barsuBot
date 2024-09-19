from createBot import bot
from aiogram import Dispatcher
from aiogram.types import CallbackQuery


async def test(callback : CallbackQuery):
    await bot.send_message(callback.chat.id, callback.text)


def fsmcallback_register(dp : Dispatcher):
    dp.register_callback_query_handler(test, text="inj")