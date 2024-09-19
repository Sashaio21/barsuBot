from createBot import dp, bot
from aiogram.utils import executor
from aiogram.types import Message

from heandlers import client_heandlers
from heandlers import FSM
from callbacks import fsmcallback


FSM.register_FSM(dp)
client_heandlers.register_client_heandlers(dp)

fsmcallback.fsmcallback_register(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
