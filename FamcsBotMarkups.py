from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

inlBtnPoints = InlineKeyboardButton(text='Узнать баллы', callback_data='Узнать баллы')
inlBtnTimetable = InlineKeyboardButton(text='Расписание', callback_data='Расписание')
startMenu = InlineKeyboardMarkup(resize_keyboard=True).add(inlBtnPoints, inlBtnTimetable)

inlBtnFrstCourse = InlineKeyboardButton(text='1', callback_data='1')
inlBtnScnCourse = InlineKeyboardButton(text='2', callback_data='2')
inlBtnThirdCourse = InlineKeyboardButton(text='3', callback_data='3')
inlBtnFourthCourse = InlineKeyboardButton(text='4', callback_data='4')
courseMenu = InlineKeyboardMarkup(resize_keyboard=True).add(inlBtnFrstCourse, inlBtnScnCourse, inlBtnThirdCourse, inlBtnFourthCourse)
