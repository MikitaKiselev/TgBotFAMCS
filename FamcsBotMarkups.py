from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup,\
    InlineKeyboardButton

inlBtnVacancies = KeyboardButton(text='Вакансии за сегодня', callback_data='Вакансии за сегодня')
inlBtnTimetable = KeyboardButton(text='Расписание', callback_data='Расписание')
inlSupport = KeyboardButton(text='Поддержка', callback_data='Поддержка')
inlTest = KeyboardButton(text='Пройти тест', callback_data='Пройти тест')
startMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(inlTest, inlBtnTimetable, inlSupport, inlBtnVacancies)

inlBtnFrstCourse = InlineKeyboardButton(text='1', callback_data='1')
inlBtnScnCourse = InlineKeyboardButton(text='2', callback_data='2')
inlBtnThirdCourse = InlineKeyboardButton(text='3', callback_data='3')
inlBtnFourthCourse = InlineKeyboardButton(text='4', callback_data='4')
courseMenu = InlineKeyboardMarkup(resize_keyboard=True).add(inlBtnFrstCourse, inlBtnScnCourse, inlBtnThirdCourse,\
                                                            inlBtnFourthCourse)
