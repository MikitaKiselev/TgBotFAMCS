from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

inlBtnVacancies = KeyboardButton(text='Вакансии за сегодня', callback_data='Вакансии за сегодня')
inlBtnTimetable = KeyboardButton(text='Расписание', callback_data='Расписание')
inlSupport = KeyboardButton(text='Поддержка', callback_data='Поддержка')
startMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(inlBtnTimetable, inlBtnVacancies, inlSupport)

inlBtnFrstCourse = KeyboardButton(text='1', callback_data='1')
inlBtnScnCourse = KeyboardButton(text='2', callback_data='2')
inlBtnThirdCourse = KeyboardButton(text='3', callback_data='3')
inlBtnFourthCourse = KeyboardButton(text='4', callback_data='4')
courseMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(inlBtnFrstCourse, inlBtnScnCourse, inlBtnThirdCourse,
                                                           inlBtnFourthCourse)

inlTodayTimetable = InlineKeyboardButton(text='Расписание на сегодня', callback_data='Расписание на сегодня')
inlTomorrowTimetable = InlineKeyboardButton(text='Расписание на завтра', callback_data='Расписание на завтра')
inlWeekTimetable = InlineKeyboardButton(text='Расписание на неделю', callback_data='Расписание на неделю')
inlChangeGroupCourse = InlineKeyboardButton(text='Изменить курс и группу', callback_data='Изменить курс и группу')
mainCourseMenu = InlineKeyboardMarkup(resize_keyboard=True, row_width=1).add(inlTodayTimetable, inlTomorrowTimetable,
                                                                             inlWeekTimetable, inlChangeGroupCourse)

buttons_frst_course = [InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(1, 12)]
frst_course_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
frst_course_menu.add(*buttons_frst_course)

buttons_second_course = [InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(1, 14)]
second_course_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
second_course_menu.add(*buttons_second_course)
