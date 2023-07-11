import random
from aiogram import Bot, Dispatcher, executor, types
import FamcsBotMarkups as mk
import config
import time

TOKEN = config.TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# Стартовая менюшка
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(message.from_user.id, 'Привет, {0.first_name}'.format(message.from_user), reply_markup=mk.startMenu)


# Ответ на запрос про баллы (пока сделал так, потом будем менять)
@dp.callback_query_handler(text='Узнать баллы')
async def points_call(callback: types.CallbackQuery):
    await callback.message.answer('Ульяна гей')
    await callback.answer()


# Всплывающая менюшка выбора курса обучения (надо добавить ещё выбор спецухи, но эт позже)
@dp.callback_query_handler(text='Расписание')
async def timetable_call(callback: types.CallbackQuery):
    await callback.message.answer('Выбери свой курс', reply_markup=mk.courseMenu)
    await callback.answer()


# Ответ на выбранный курс
@dp.callback_query_handler(text='1')
async def timetable1_call(callback: types.CallbackQuery):
    await callback.message.answer('гавно\n*Расписание 1*')
    await callback.answer()


@dp.callback_query_handler(text='2')
async def timetable2_call(callback: types.CallbackQuery):
    await callback.message.answer('залупа\n*Расписание 2*')
    await callback.answer()


@dp.callback_query_handler(text='3')
async def timetable3_call(callback: types.CallbackQuery):
    await callback.message.answer('пенис\n*Расписание 3*')
    await callback.answer()


@dp.callback_query_handler(text='4')
async def timetable4_call(callback: types.CallbackQuery):
    await callback.message.answer('хер\n*Расписание 4*')
    await callback.answer()


async def message_sender(user_id):
    while True:
        await bot.send_message(user_id, 'pussy')
        time.sleep(10)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
