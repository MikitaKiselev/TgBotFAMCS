from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
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
Для запуска поиска отправь команду \n/start_searching_for_new_job\nДля прекращения поиска отправь команду\
\n/stop_searching_for_new_job\n\nТакже у меня есть функция, позволяющая в любую минуту глянуть <b>свое расписание</b> 👀\
\n\nЕсли считаешь себя истиным ФПМовцом, то просто обязан пройти тест на принадлежность к студенческой организации😉\n\
Запуск теста \n/start_test\nДосрочное завершение\n/stop_test\n\n\
По всем вопросам и предложениям обращайтесь к @payalnik144 @starostarka", parse_mode="html", reply_markup=mk.startMenu)


@dp.message_handler(text='Вакансии за сегодня')
async def points_call(message: types.Message):
    total_list = all_posts()
    if total_list == "":
        await message.answer('Сегодня ничего нет(')
    else:
        await message.answer(total_list, parse_mode=types.ParseMode.HTML)

user_data = {}
test_data = {
    "Твой любимый предмет:": ["Прога0", "Алгебра0", "Матан0", "Не хожу на пары и не знаю предметы1"],
    "Любимый персонаж в доте:": ["Сф 1000-7 zxc0", "Кристалка0", "ПУДЖ1"],
    "Кто самая hot girl на ФПМИ?": ["Ульяна1", "Староста 12 группы0", "Спросите Матвеева0", "Никита1", "полина жос9", "тима9"],
    "Твой любимый сериал:": ["Великолепный век0", "Не смотрю сериалы, онли аниме0", "Только фильмы и только с Районом Гослингом1"],
    "Выбери стационарное линейное однородное уравнение": ["x'=-x+10", "t''+4t'+t=01", "Dx=10", "x''+2x'+x+5=00"],
    "Сори за предыдущий душный вопрос🤮\n\nЛюбимый фиксик": ["Нолик0", "Крестик1", "Папус0", "Анус0"],
    "Лучшая шаурма в городе": ["Жанчик0", "Жанчик0", "Жанчик1", "Жанчик0"],
    "117/20 = ?\n\nНа размышление 5 секунд...4...3...2...1": ["6.20", "6.150", "5.750", "Тут есть правильный ответ1"],
    "Лучшая игра": ["Майнкрафт0", "Дока20", "Написанная ФПМщиком0", "Написанная не ФПМщиком1"],
    "Любимое число": ["1000", "20", "41", "6660", "самое большое простое9"]
}
questions = ["Твой любимый предмет:",
             "Любимый персонаж в доте:",
             "Кто самая hot girl на ФПМИ?",
             "Твой любимый сериал:",
             "Выбери стационарное линейное однородное уравнение",
             "Сори за предыдущий душный вопрос🤮\n\nЛюбимый фиксик",
             "Лучшая шаурма в городе",
             "117/20 = ?\n\nНа размышление 5 секунд...4...3...2...1",
             "Лучшая игра",
             "Любимое число"
             ]

test_status = False
number = 0


@dp.message_handler(commands='start_test')
async def start_test(message: types.Message):
    chat_id = message.chat.id

    # Проверяем, нет ли уже активного теста для данного пользователя
    if chat_id not in user_data or not user_data[chat_id]['test_status']:
        # Создаем новую структуру данных для текущего пользователя
        '''user_data[chat_id] = {
            'test_status': True,
            'score': 0,
            'number': 0
        }'''
        user_data[chat_id]['test_status'] = True
        user_data[chat_id]['score'] = 0
        user_data[chat_id]['number'] = 0
        await message.answer("На ФПМИ есть большое количество организаций и активностей, где ты сможешь \
реализовать себя, ведь ФПМИ это не только об учебе! \nПройди тест и узнай, что тебе подходит больше всего.")
        await send_question(chat_id)


async def send_question(chat_id):
    user = user_data[chat_id]
    testButtons = ReplyKeyboardMarkup(resize_keyboard=True)

    # Получаем список вариантов ответов
    answer_options = test_data.get(questions[user['number']])

    for idx, button in enumerate(answer_options):
        if user['number'] == 2:
            if idx < len(answer_options) - 2:
                testButtons.add(button[:len(button) - 1])
        elif user['number'] == 9:
            if idx < len(answer_options) - 1:
                testButtons.add(button[:len(button) - 1])
        else:
            testButtons.add(button[:len(button) - 1])

    await bot.send_message(chat_id, questions[user['number']], reply_markup=testButtons)


async def test_result(chat_id):
    user = user_data[chat_id]
    user['test_status'] = False
    user['number'] = 0
    if user['score'] <= 5:
        await bot.send_message(chat_id, "Ого, ничего себе! Тебе очень повезло, ты на 100% подходишь для лучшей организации БГУ - БРСМ!", reply_markup=mk.startMenu)
    elif user['score'] == 7 or user['score'] == 6:
        await bot.send_message(chat_id, "Хочу тебя поздравить, милый мой, твоя стихия - это СКС", reply_markup=mk.startMenu)
    elif user['score'] == 8:
        await bot.send_message(chat_id, "А ты хорош, твоя дорога лежит в Творческий Союз!!!", reply_markup=mk.startMenu)
    else:
        await bot.send_message(chat_id, 'Что ж... Ты определенно настоящий ФПМовец и обязан пополнить ряды Студенческого союза ФПМИ!', reply_markup=mk.startMenu)
    print(user['score'])


@dp.message_handler(commands=['stop_test'])
async def stop_test(message: types.Message):
    chat_id = message.chat.id
    if chat_id in user_data and user_data[chat_id]['test_status']:
        # Остановка теста и сброс данных пользователя
        user_data[chat_id]['test_status'] = False
        user_data[chat_id]['number'] = 0
        user_data[chat_id]['score'] = 0
        await message.answer("Жаль, что ты так и не узнал свою ориентацию...\n\
Но ты всегда можешь вернуться и пройти тест снова!", reply_markup=mk.startMenu)
    else:
        await message.answer("Ты еще даже не начал тест, чтоб его заканчивать...\nТыкай сюда /start_test, чтобы начать")


# Всплывающая менюшка выбора курса обучения (надо добавить ещё выбор спецухи, но эт позже)
@dp.message_handler(text='Расписание')
async def timetable_call(message: types.Message):
    chat_id = message.chat.id
    if chat_id in user_data and 'course' in user_data[chat_id]:
        await message.answer('Что будем смотреть?', reply_markup=mk.mainCoourseMenu)
    else:
        await message.answer('Выбери свой курс', reply_markup=mk.courseMenu)
        user_data[chat_id] = {}
        user_data[chat_id]['test_status'] = False

    #await message.answer('Какая у тебя группа?')


async def get_group(chat_id):
    await bot.send_message(chat_id, 'Напиши свою группу', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(text='Поддержка')
async def timetable_call(message: types.Message):
    await message.answer('Тут можно поддержать наш проект и скинуть Ульяне на брови 💅\n(тут будет мой студак потом)\n\
\nУльяна обойдётся без бровей, а вот Никита без пива никак. Вы знаете, что делать😉\n(тут будет мой студак потом)')


# Ответ на выбранный курс
'''
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
'''

chat_states = {}


@dp.message_handler(commands=['start_searching_for_new_job'])
async def start_searching_for_new_job(message: types.Message):
    global chat_states

    chat_id = message.chat.id
    if chat_id not in chat_states or not chat_states[chat_id]:
        chat_states[chat_id] = True
        await message.answer("Поиск запущен")
        while chat_states[chat_id]:
            post = new_post()
            if post is not None:
                await message.answer(post, parse_mode=types.ParseMode.HTML)
            await asyncio.sleep(1200)
    else:
        await message.answer("Поиск идёт")


@dp.message_handler(commands=['stop_searching_for_new_job'])
async def stop_searching_for_new_job(message: types.Message):
    global chat_states

    chat_id = message.chat.id
    if chat_id in chat_states and chat_states[chat_id]:
        chat_states[chat_id] = False
        await message.answer("Поиск прекращён")
    else:
        await message.answer("Поиск не запущен")


@dp.message_handler()
async def check_answer(message: types.Message):
    chat_id = message.chat.id

    # Проверяем, есть ли активный тест для данного пользователя
    if chat_id in user_data and user_data[chat_id]['test_status']:
        user = user_data[chat_id]
        check = False
        answer = ""

        current_question_index = user['number']
        for line in test_data.get(questions[current_question_index]):
            # Отладочный вывод для сравниваемых строк
            print(current_question_index)
            print(f"Сравниваем: {message.text.strip().lower()} и {line[:len(line) - 1].strip().lower()}")

            if message.text.strip().lower() == line[:len(line) - 1].strip().lower():
                check = True
                answer = line
                break  # Прекращаем поиск, так как нашли соответствие

        if not check:
            await bot.send_message(chat_id, 'Выбери вариант из списка🤬')
        else:
            # Обновляем счет пользователя и переходим к следующему вопросу или завершаем тест
            user['score'] += int(answer[len(answer) - 1])
            if current_question_index == len(questions) - 1:
                await test_result(chat_id)
            else:
                user['number'] += 1
                await send_question(chat_id)
    else:
        # Если нет активного теста, можно обработать другие сценарии здесь
        if message.text.isdigit():
            if 'course' not in user_data[chat_id]:
                user_data[message.chat.id]['course'] = message.text
                await get_group(message.chat.id)
            else:
                user_data[message.chat.id]['group'] = message.text
                await message.answer('Что будем смотреть?', reply_markup=mk.mainCoourseMenu)
        else:
            await bot.send_message(chat_id, 'Братишка, я хз чего ты от меня хочешь, ознакомься с доступными командами,\
а потом уже пукай сообщение')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
