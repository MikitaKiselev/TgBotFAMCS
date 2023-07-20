from aiogram import Bot, Dispatcher, executor, types
import FamcsBotMarkups as mk
import config
import asyncio
from parsing import all_posts
from parsing import new_post

TOKEN = config.TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# Стартовая менюшка
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.answer("Привет, друг\U0001FAE6\nЯ бот, который облегчит тебе жизнь!\n\n\
Я ищу новые вакансии на <b>LinkedIn</b>, связанные с IT и сразу же присылаю тебе уведомление.\n\n\
Для запуска поиска отправь команду \n/start_searching_for_new_job\n\
Для прекращения поиска отправь команду \n/stop_searching_for_new_job\n\n\
Также у меня есть функция, позволяющая в любую минуту глянуть <b>свое расписание</b> 👀\n\n\
По всем вопросам и предложениям обращайтесь к @payalnik144 @starostarka", parse_mode="html", reply_markup=mk.startMenu)


@dp.message_handler(text='Вакансии за сегодня')
async def points_call(message: types.Message):
    total_list = all_posts()
    await message.answer(total_list, parse_mode=types.ParseMode.HTML)


# Всплывающая менюшка выбора курса обучения (надо добавить ещё выбор спецухи, но эт позже)
@dp.message_handler(text='Расписание')
async def timetable_call(message: types.Message):
    await message.answer('Выбери свой курс', reply_markup=mk.courseMenu)


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

chat_states = {}


@dp.message_handler(commands=['start_searching_for_new_job'])
async def start_searching_for_new_job(message: types.Message):
    global chat_states

    chat_id = message.chat.id
    if chat_id not in chat_states or not chat_states[chat_id]:
        chat_states[chat_id] = True
        back_list = []
        await message.answer("Поиск запущен")
        while chat_states[chat_id]:
            post, back_list = new_post(back_list)
            if post is not None:
                await message.answer(post, parse_mode=types.ParseMode.HTML)
            await asyncio.sleep(1800)


@dp.message_handler(commands=['stop_searching_for_new_job'])
async def stop_searching_for_new_job(message: types.Message):
    global chat_states

    chat_id = message.chat.id
    if chat_id in chat_states and chat_states[chat_id]:
        chat_states[chat_id] = False
        await message.answer("Поиск прекращён")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
