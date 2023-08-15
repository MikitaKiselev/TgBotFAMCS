from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
import FamcsBotMarkups as mk
import config
import asyncio
import json
from parsing import all_posts
from parsing import new_post

TOKEN = config.TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

selected_language = 'ru'

with open('package.json', 'r', encoding='utf-8') as file:
    translations = json.load(file)

# Стартовая менюшка
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.answer("Привет, друг\U0001FAE6\nЯ бот, который облегчит тебе жизнь!\n\n Я ищу новые вакансии на <b>LinkedIn</b>, связанные с IT и сразу же присылаю тебе уведомление.\n\nДля запуска поиска отправь команду \n/start_searching_for_new_job\nДля прекращения поиска отправь команду \n/stop_searching_for_new_job\n\nТакже у меня есть функция, позволяющая в любую минуту глянуть <b>свое расписание</b> 👀\n\nПо всем вопросам и предложениям обращайтесь к @payalnik144 @starostarka", parse_mode="html", reply_markup=mk.startMenu)


@dp.message_handler(text='Вакансии за сегодня')
async def points_call(message: types.Message):
    total_list = all_posts()
    if total_list == "":
        await message.answer('Сегодня ничего нет(')
    else:
        await message.answer(total_list, parse_mode=types.ParseMode.HTML)


test_data = {
    'Твой любимый предмет:': ["Прога0", "Алгебра0", "Матан0", "Не хожу на пары и не знаю предметы1"],
    "Любимый персонаж в доте:": ["Сф 1000-7 zxc0", "Кристалка0", "ПУДЖ1"],
    "Кто самая hot girl на ФПМИ?": ["Ульяна1", "Староста 12 группы0", "Спросите Матвеева0"],
    "Твой любимый сериал:": ["Великолепный век0", "Не смотрю сериалы, онли аниме0", "Только фильмы и только с Районом Гослингом1"],
    "Выбери стационарное линейное однородное уравнение": ["x'=-x+10", "t''+4t'+t=01", "Dx=10", "x''+2x'+x+5=00"],
}
questions = ['Твой любимый предмет:', "Любимый персонаж в доте:", "Кто самая hot girl на ФПМИ?", "Твой любимый сериал:", "Выбери стационарное линейное однородное уравнение"]

test_status = False
number = 0


@dp.message_handler(text='Пройти тест')
async def start_test(message: types.Message):
    global test_status
    global score
    test_status = True
    score = 0
    await message.answer("На ФПМИ есть большое количество организаций и активностей, где ты сможешь реализовать себя, ведь ФПМИ это не только об учебе! \nПройди тест и узнай, что тебе подходит больше всего.")
    chat_id = message.chat.id
    await send_question(number, chat_id)


async def send_question(n, chat_id):
    testButtons = ReplyKeyboardMarkup(resize_keyboard=True)
    for button in test_data.get(questions[n]):
        testButtons.add(button[:len(button)-1])
    await bot.send_message(chat_id, questions[n], reply_markup=testButtons)
    global number
    number += 1


async def test_result(chat_id):
    global test_status
    test_status = False
    global number
    number = 0
    if score == 5:
        await bot.send_message(chat_id, "Что ж... Ты определенно настоящий ФПМовец и обязан пополнить ряды Студенческого союза ФПМИ!", reply_markup=mk.startMenu)
    else:
        await bot.send_message(chat_id, 'Ого, ничего себе! Тебе очень повезло, ты на 100% подходишь для лучшей организации БГУ - БРСМ!', reply_markup=mk.startMenu)


# Всплывающая менюшка выбора курса обучения (надо добавить ещё выбор спецухи, но эт позже)
@dp.message_handler(text='Расписание')
async def timetable_call(message: types.Message):
    await message.answer('Выбери свой курс', reply_markup=mk.courseMenu)


@dp.message_handler(text='Поддержка')
async def timetable_call(message: types.Message):
    await message.answer('Тут можно поддержать наш проект и скинуть Ульяне на брови 💅\n(тут будет мой студак потом)')


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
            post = new_post()
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


@dp.message_handler()
async def check_answer(message: types.Message):
    if test_status:
        chat_id = message.chat.id
        check = False
        answer = ""
        for line in test_data.get(questions[number-1]):
            if message.text == line[:len(line)-1]:
                check = True
                answer = line
        if not check:
            await bot.send_message(chat_id, 'Выбери вариант из списка🤬')
        else:
            global score
            score += int(answer[len(answer)-1])
            if number == len(questions):
                await test_result(chat_id)
            else:
                await send_question(number, chat_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
