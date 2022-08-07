from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import os
import random
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

storage = MemoryStorage()

date_photo = []
date_text = []

bot = Bot(token='1835934279:AAHdYeZ5zW3gLNZDXEe8JL5DTjDuEelpnhA')
dp = Dispatcher(bot, storage=storage)

b1 = KeyboardButton('❤')
b2 = KeyboardButton('👎')

kb_client = ReplyKeyboardMarkup()

kb_client.row(b1, b2)

class FSMAdmin(StatesGroup):
    photo = State()
    discription = State()

@dp.message_handler(commands='отмена', state=[FSMAdmin.photo, FSMAdmin])
async def cancel_handler(message: types.Message, state: FSMContext):
    print(state)
    current_state = await state.get_state()
    if (current_state is None):
        return
    await state.finish()
    await message.reply('OK')

@dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message : types.Message):
    await FSMAdmin.photo.set()
    await bot.send_message(message.from_user.id, 'Загрузи фото')

@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await bot.send_message(message.from_user.id, 'Загрузи описание')

@dp.message_handler(state=FSMAdmin)
async def load_discription(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['discription'] = message.text
    async with state.proxy() as data:
        date_photo.append(data['photo'])
        date_text.append(data['discription'])
    await cm_start(message)

@dp.message_handler(commands='Лента')
async def lenta(message : types.Message):
    i = random.randint(0, len(date_text) - 1)
    await bot.send_photo(message.from_user.id, date_photo[i], caption=date_text[i], reply_markup=kb_client)

@dp.message_handler()
async def mark(message : types.Message):
    if (message.text == '❤'):
        print('like')
    if (message.text == '👎'):
        print('dislike')
    await lenta(message)
executor.start_polling(dp, skip_updates=True)
