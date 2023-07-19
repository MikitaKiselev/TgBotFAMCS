import random
from aiogram import Bot, Dispatcher, executor, types
import FamcsBotMarkups as mk
import config
import time
from parsing import all_posts
from parsing import new_post

TOKEN = config.TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Стартовая менюшка
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет, {0.first_name}'.format(message.from_user), reply_markup=mk.startMenu)


@dp.message_handler(text='pussy')
async def get_list(message: types.Message):
    total_list = all_posts()
    await bot.send_message(message.from_user.id, total_list, parse_mode=types.ParseMode.HTML)


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


@dp.message_handler(commands=['pizda'])
async def send_message(message: types.Message):
    back_list = []
    while True:
        post = new_post(back_list)[0]
        back_list = new_post(back_list)[1]
        if post is not None:
            await bot.send_message(message.from_user.id, post, parse_mode=types.ParseMode.HTML)
        time.sleep(1800)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
