from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from google_services.sheets import sheet
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

vacancies = {
    "Разработка": {
        "Full-Stack Разработчик": "Инфа про фулстакера",
        "UI/UX дизайнер": "Инфа про юайюэксера"},
    "Финансы": {
        "Директор финансового офиса": "Описание вакансии директора",
        "Казначей": "Описание вакансии казначея"},
    "HR": {
        "Менеджер HR": "Описание вакансии менеджера HR",
        "Директор HR": "Описание вакансии HR дира",
        "Ресепшионист": "Описание вакансии ресепшиониста"}
}

internships = {
    "Стажер в HR офис": "Вставьте описание стажировки HR сюда",
    "Стажер в PR офис": "Вставьте описание стажировки PR сюда",
    "Стажер в образовательный офис": "Вставьте описание образвательной стажировки сюда"
}

data = sheet.get_all_records()
row = len(data) + 2


class ApplyForVacancy(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_email = State()
    waiting_for_cv = State()
    waiting_for_occupation = State()
    waiting_for_specialty = State()
    waiting_for_vacancies = State()
    waiting_for_internship = State()
    waiting_for_test_to_end = State()


async def update_sheet(state: FSMContext):
    user_data = await state.get_data()
    sheet.update_cell(row, 1, user_data['full_name'])
    sheet.update_cell(row, 2, user_data['email'])
    sheet.update_cell(row, 3, user_data['chosen_specialty'])
    sheet.update_cell(row, 4, user_data['chosen_vacancy'])
    sheet.update_cell(row, 5, user_data['cv_link'])


async def apply_start(message: types.Message):
    await message.answer("Введите Ваше имя и фамилию:")
    await ApplyForVacancy.waiting_for_full_name.set()


# Обратите внимание: есть второй аргумент
async def name_gotten(message: types.Message, state: FSMContext):
    if len(message.text.split()) != 2:
        await message.answer("Пожалуйста, введите корректную информацию")
        return
    await state.update_data(full_name=message.text.title())
    # sheet.update_cell(row, 1, message.text.title())
    await message.answer("Введите Ваш Email:")
    await ApplyForVacancy.next()


async def email_gotten(message: types.Message, state: FSMContext):
    if not re.match(regex, message.text):
        await message.answer("Пожалуйста, введите корректный адрес электронной почты")
        return
    await state.update_data(email=message.text.lower())
    await message.answer("Теперь отправьте ссылку на Ваше резюме:"
                         "\n (Можете использовать любой файловый хостинг, "
                         "но удостоверьтерсь, что доступ по ссылке включен)")
    await ApplyForVacancy.waiting_for_cv.set()


async def cv_gotten(message: types.Message, state: FSMContext):
    await state.update_data(cv_link=message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Полный день", "Стажировка")
    await message.answer("Теперь выберите тип занятости:", reply_markup=keyboard)
    await ApplyForVacancy.waiting_for_occupation.set()


async def occupation_chosen(message: types.Message, state: FSMContext):
    if message.text == "Полный день":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for key, value in vacancies.items():
            keyboard.add(key)
        await message.answer("Теперь выберите специализацию:", reply_markup=keyboard)
        await ApplyForVacancy.waiting_for_specialty.set()
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for key, value in internships.items():
            keyboard.add(key)
        await state.update_data(chosen_specialty="Стажировка")
        await message.answer("Теперь выберите тип стажировки:", reply_markup=keyboard)
        await ApplyForVacancy.waiting_for_internship.set()


async def specialty_chosen(message: types.Message, state: FSMContext):
    if message.text not in vacancies.keys():
        await message.answer("Пожалуйста, выберите специализацию, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_specialty=message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_data = await state.get_data()
    for vacancy, description in vacancies[user_data['chosen_specialty']].items():
        keyboard.add(vacancy)
    await ApplyForVacancy.waiting_for_vacancies.set()
    await message.answer("Теперь выберите подходящую вакансию:", reply_markup=keyboard)


async def vacancy_chosen(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text not in vacancies[user_data['chosen_specialty']].keys():
        await message.answer("Пожалуйста, выберите вакансию используя клавиатуру ниже.")
        return
    await state.update_data(chosen_vacancy=message.text)
    await message.answer(f"Поздравляю, {user_data['full_name']}, Вы успешно подали заявку на "
                         f"вакансию '{message.text}'!\n", reply_markup=types.ReplyKeyboardRemove())
    await update_sheet(state)
    await state.finish()


async def internship_chosen(message: types.Message, state: FSMContext):
    if message.text not in internships.keys():
        await message.answer("Пожалуйста, выберите стажировку из списка:")
        return
    user_data = await state.get_data()
    await state.update_data(chosen_vacancy=message.text.capitalize())
    await message.answer(f"Поздравляю, {user_data['full_name']}, Вы успешно подали заявку на "
                         f"вакансию '{message.text}'!\n", reply_markup=types.ReplyKeyboardRemove())
    await update_sheet(state)
    await state.finish()


def register_handlers_apply(dp: Dispatcher):
    dp.register_message_handler(apply_start, commands="apply", state="*")
    dp.register_message_handler(name_gotten, state=ApplyForVacancy.waiting_for_full_name)
    dp.register_message_handler(email_gotten, state=ApplyForVacancy.waiting_for_email)
    dp.register_message_handler(specialty_chosen, state=ApplyForVacancy.waiting_for_specialty)
    dp.register_message_handler(vacancy_chosen, state=ApplyForVacancy.waiting_for_vacancies)
    dp.register_message_handler(internship_chosen, state=ApplyForVacancy.waiting_for_internship)
    dp.register_message_handler(occupation_chosen, state=ApplyForVacancy.waiting_for_occupation)
    dp.register_message_handler(cv_gotten, state=ApplyForVacancy.waiting_for_cv)
