from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
import datetime
import FamcsBotMarkups as mk
import config
import asyncio
from parsing import all_posts
from parsing import new_post

TOKEN = config.TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

file_path_1 = "schedule1.txt"
with open(file_path_1, 'r', encoding='utf-8') as file:
    schedule_1_course = file.read()

file_path_2 = "schedule2.txt"
with open(file_path_2, 'r', encoding='utf-8') as file:
    schedule_2_course = file.read()


# Стартовая менюшка
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    # chat_id = message.chat.id
    await message.answer("Привет, друг\U0001FAE6\nЯ бот, который облегчит тебе жизнь!\n\n\
Я ищу новые вакансии на <b>LinkedIn</b>, связанные с IT и сразу же присылаю тебе уведомление.\n\n\
Для запуска поиска отправь команду \n/start_searching_for_new_job\nДля прекращения поиска отправь команду\
\n/stop_searching_for_new_job\n\nТакже у меня есть функция, позволяющая в любую минуту глянуть <b>свое расписание</b> 👀\
\n\nЕсли считаешь себя истиным ФПМовцом, то просто обязан пройти тест на принадлежность к студенческой организации😉\n\
Запуск теста \n/start_test\nДосрочное завершение\n/stop_test\n\n\
По всем вопросам и предложениям обращайтесь к @payalnik144 @starostarka", parse_mode="html", reply_markup=mk.startMenu)


@dp.message_handler(text='Вакансии за сегодня')
async def points_call(message: types.Message):
    global all_vacancies
    if all_vacancies == "":
        await message.answer('Сегодня ничего нет(')
    else:
        await message.answer(all_vacancies, parse_mode=types.ParseMode.HTML)

user_data = {}
test_data = {
    "Твой любимый предмет:": ["Прога0", "Алгебра0", "Матан0", "Не хожу на пары и не знаю предметы1"],
    "Любимый персонаж в доте:": ["Сф 1000-7 zxc0", "Кристалка0", "ПУДЖ1"],
    "Кто самая hot girl на ФПМИ?": ["Ульяна1", "Староста 12 группы0", "Спросите Матвеева0", "Никита1", "полина жос9",
                                    "тима9"],
    "Твой любимый сериал:": ["Великолепный век0", "Не смотрю сериалы, онли аниме0",
                             "Только фильмы и только с Районом Гослингом1"],
    "Выбери стационарное линейное однородное уравнение": ["x'=-x+10", "t''+4t'+t=01", "Dx=10", "x''+2x'+x+5=00"],
    "Сори за предыдущий душный вопрос🤮\n\nЛюбимый фиксик": ["Нолик0", "Крестик1", "Папус0", "Янус0"],
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

    # Check if chat_id is in user_data and if there's an active test for this user
    if chat_id in user_data and user_data[chat_id]['test_status']:
        await message.answer("Ты уже начал тест. Если хочешь остановить его, нажми /stop_test.")
        return

    # Initialize user_data[chat_id] if it doesn't exist
    if chat_id not in user_data:
        user_data[chat_id] = {}

    # Initialize the test data for the user
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
        await bot.send_message(chat_id, "Ого, ничего себе! Тебе очень повезло, ты на 100% \
подходишь для лучшей организации БГУ - БРСМ!", reply_markup=mk.startMenu)
    elif user['score'] == 7 or user['score'] == 6:
        await bot.send_message(chat_id, "Хочу тебя поздравить, милый мой, твоя стихия - это СКС",
                               reply_markup=mk.startMenu)
    elif user['score'] == 8:
        await bot.send_message(chat_id, "А ты хорош, твоя дорога лежит в Творческий Союз!!!", reply_markup=mk.startMenu)
    else:
        await bot.send_message(chat_id, 'Что ж... Ты определенно настоящий ФПМовец и обязан \
пополнить ряды Студенческого союза ФПМИ!', reply_markup=mk.startMenu)
    # print(user['score'])


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


@dp.message_handler(text='Расписание')
async def timetable_call(message: types.Message):
    chat_id = message.chat.id
    if chat_id in user_data and 'course' in user_data[chat_id]:
        await message.answer('Что будем смотреть?', reply_markup=mk.mainCourseMenu)
    else:
        await message.answer('Выбери свой курс', reply_markup=mk.courseMenu)
        user_data[chat_id] = {}
        user_data[chat_id]['test_status'] = False
        user_data[chat_id]['schedule_course_status'] = True
        user_data[chat_id]['schedule_group_status'] = True


def get_weekday(request="today"):
    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    if request == "tomorrow":
        index = (datetime.datetime.today().weekday() + 1) % 7
    elif request == "after_tomorrow":
        index = (datetime.datetime.today().weekday() + 2) % 7
    else:
        index = datetime.datetime.today().weekday()
    return days[index]


async def get_week_schedule(course, group):
    if course == "1":
        schedule_course = schedule_1_course
        group_range = range(1, 12)
    elif course == "2":
        schedule_course = schedule_2_course
        group_range = range(1, 14)
    else:
        return None

    for i in group_range:
        if group == str(i):
            schedule_part = schedule_course[
                 schedule_course.find("{} группа".format(i)) - 6:schedule_course.find("{} группа".format(i + 1)) - 9]
            return schedule_part

    return None


@dp.callback_query_handler(text='Расписание на сегодня')
async def today_timetable(callback: types.CallbackQuery):
    current_day = get_weekday()
    if current_day == "воскресенье":
        await callback.message.answer("Сегодня воскресенье, ты чё, какие пары")
        await callback.answer()
        return

    course = user_data[callback.message.chat.id]['course']
    group = user_data[callback.message.chat.id]['group']

    schedule_part = await get_week_schedule(course, group)
    if schedule_part is not None:
        schedule_part = schedule_part[schedule_part.find(get_weekday()):schedule_part.find(
            get_weekday(request="tomorrow"))]
        await send_schedule_for_day(schedule_part, callback, group)
    else:
        await callback.message.answer("Сорри, расписание не найдено.")

    await callback.answer()


@dp.callback_query_handler(text='Расписание на завтра')
async def tomorrow_timetable(callback: types.CallbackQuery):
    current_day = get_weekday()
    if current_day == "суббота":
        await callback.message.answer("Завтра воскресенье, ты чё, какие пары")
        await callback.answer()
        return

    course = user_data[callback.message.chat.id]['course']
    group = user_data[callback.message.chat.id]['group']

    schedule_part = await get_week_schedule(course, group)
    if schedule_part is not None:
        schedule_part = schedule_part[schedule_part.find(get_weekday(request="tomorrow")):schedule_part.find(
            get_weekday(request="after_tomorrow"))]
        await send_schedule_for_day(schedule_part, callback, group)
    else:
        await callback.message.answer("Сорри, расписание не найдено.")

    await callback.answer()


@dp.callback_query_handler(text='Расписание на неделю')
async def week_timetable(callback: types.CallbackQuery):
    course = user_data[callback.message.chat.id]['course']
    group = user_data[callback.message.chat.id]['group']

    schedule_part = await get_week_schedule(course, group)
    if schedule_part is not None:
        await callback.message.answer(schedule_part)
    else:
        await callback.message.answer("Сорри, расписание не найдено.")

    await callback.answer()


async def send_schedule_for_day(schedule, callback, group):
    await callback.message.answer(f"{group} группа\n\n{schedule}")


@dp.callback_query_handler(text='Изменить курс и группу')
async def change_group_course(callback: types.CallbackQuery):
    chat_id = callback.message.chat.id
    user_data[chat_id]['schedule_course_status'] = True
    user_data[chat_id]['schedule_group_status'] = True
    await callback.message.answer('Выбери свой курс', reply_markup=mk.courseMenu)
    await callback.answer()


async def get_group(chat_id):
    if user_data[chat_id]['course'] == "1":
        await bot.send_message(chat_id, 'Выбери свою группу', reply_markup=mk.frst_course_menu)
    elif user_data[chat_id]['course'] == "2":
        await bot.send_message(chat_id, 'Выбери свою группу', reply_markup=mk.second_course_menu)
    else:
        await bot.send_message(chat_id, 'Напиши свою группу', reply_markup=mk.startMenu)


@dp.message_handler(text='Поддержка')
async def timetable_call(message: types.Message):
    await message.answer('Тут можно поддержать наш проект и скинуть Ульяне на брови 💅\n(тут будет мой студак потом)\n\
\nУльяна обойдётся без бровей, а вот Никита без пива никак. Вы знаете, что делать😉\n(тут будет мой студак потом)')


chat_states = {}
search_interval = 1200  # Интервал между поисками вакансий

all_vacancies = ""


async def search_for_new_jobs():
    global all_vacancies
    while True:
        for chat_id in chat_states:
            if chat_states[chat_id]:
                post = new_post()  # Замените на свою функцию поиска вакансий
                if post is not None:
                    await bot.send_message(chat_id, post, parse_mode=types.ParseMode.HTML)

        all_vacancies = all_posts()

        await asyncio.sleep(search_interval)


@dp.message_handler(commands=['start_searching_for_new_job'])
async def start_searching_for_new_job(message: types.Message):
    global chat_states

    chat_id = message.chat.id
    if chat_id not in chat_states or not chat_states[chat_id]:
        chat_states[chat_id] = True
        await message.answer("Поиск запущен")
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


# Запускаем фоновый процесс поиска вакансий при старте бота
async def on_startup(dp):
    asyncio.create_task(search_for_new_jobs())


bool_group_1_course = False
bool_group_2_course = False
groups_1_course = [i for i in range(1, 12)]
groups_2_course = [i for i in range(1, 14)]


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
            # print(current_question_index)
            # print(f"Сравниваем: {message.text.strip().lower()} и {line[:len(line) - 1].strip().lower()}")

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
            if user_data[chat_id]['schedule_course_status']:
                if message.text == "1" or message.text == "2" or message.text == "3" or message.text == "4":
                    user_data[message.chat.id]['course'] = message.text
                    user_data[chat_id]['schedule_course_status'] = False
                    await get_group(message.chat.id)
                else:
                    await message.answer("Нет такого курса, подумай ещё:)")
            else:
                if user_data[chat_id]['schedule_group_status']:
                    global bool_group_1_course
                    global bool_group_2_course
                    if user_data[message.chat.id]["course"] == "1":
                        for group in groups_1_course:
                            if message.text == str(group):
                                bool_group_1_course = True

                        if bool_group_1_course:
                            user_data[message.chat.id]['group'] = message.text
                            bool_group_1_course = False
                            user_data[chat_id]['schedule_group_status'] = False
                            await message.answer('Что будем смотреть?', reply_markup=mk.mainCourseMenu)
                            await message.answer('Наслаждайся 😎😉', reply_markup=mk.startMenu)
                        else:
                            await message.answer("Нет такой группы, друг, но не переживай, у тебя ещё есть попытки:)")

                    elif user_data[message.chat.id]["course"] == "2":
                        for group in groups_2_course:
                            if message.text == str(group):
                                bool_group_2_course = True

                        if bool_group_2_course:
                            user_data[message.chat.id]['group'] = message.text
                            bool_group_2_course = False
                            user_data[chat_id]['schedule_group_status'] = False
                            await message.answer('Что будем смотреть?', reply_markup=mk.mainCourseMenu)
                            await message.answer('Наслаждайся 😎😉', reply_markup=mk.startMenu)
                        else:
                            await message.answer("Нет такой группы, друг, но не переживай, у тебя ещё есть попытки:)")
                    elif user_data[message.chat.id]["course"] == "3":
                        await message.answer("Сорри,расписание на 3 и 4 курс не сделали((( Бюджет кончился",
                                             reply_markup=mk.startMenu)
                    elif user_data[message.chat.id]["course"] == "4":
                        await message.answer("Сорри,расписание на 3 и 4 курс не сделали((( Бюджет кончился",
                                             reply_markup=mk.startMenu)
                else:
                    await bot.send_message(chat_id, 'Братишка, я хз чего ты от меня хочешь, ознакомься с доступными \
командами, а потом уже пукай сообщение')
        else:
            await bot.send_message(chat_id, 'Братишка, я хз чего ты от меня хочешь, ознакомься с доступными командами,\
а потом уже пукай сообщение')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
