from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.handlers.apply import vacancies, internships


class ShowVacancies(StatesGroup):
    waiting_for_occupation = State()
    waiting_for_specialty = State()
    waiting_for_vacancy = State()
    waiting_for_internship = State()


async def show_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Работа")
    keyboard.add("Стажировка")
    await message.answer("Выберите занятость:", reply_markup=keyboard)
    await ShowVacancies.waiting_for_occupation.set()


# Обратите внимание: есть второй аргумент
async def occupation_chosen(message: types.Message, state: FSMContext):
    if message.text == "Стажировка":
        await state.update_data(chosen_occupation=message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for internship, description in internships.items():
            keyboard.add(internship)
        await ShowVacancies.waiting_for_internship.set()
        await message.answer("Выберите интересующую стажировку:", reply_markup=keyboard)

    elif message.text == "Работа":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for key, value in vacancies.items():
            keyboard.add(key)
        # Для последовательных шагов можно не указывать название состояния, обходясь next()
        await ShowVacancies.waiting_for_specialty.set()
        await message.answer("Теперь выберите специализацию:", reply_markup=keyboard)


async def specialty_chosen(message: types.Message, state: FSMContext):
    await state.update_data(chosen_specialty=message.text.capitalize())
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_data = await state.get_data()
    for vacancy in vacancies[user_data['chosen_specialty']]:
        keyboard.add(vacancy)
    await ShowVacancies.waiting_for_vacancy.set()
    await message.answer("Теперь выберите подходящую вакансию:", reply_markup=keyboard)


async def vacancy_chosen(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(chosen_vacancy=message.text.capitalize())
    print(user_data['chosen_specialty'])
    await message.answer(f"Информация о вакансии '{message.text}'\n"
                         f"тут инфа про вакансию\n", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def internship_chosen(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(chosen_internship=message.text)
    await message.answer(f"Описание стажировки: \n {message.text}\n",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_show_vacancies(dp: Dispatcher):
    dp.register_message_handler(show_start, commands="show_vacancies", state="*")
    dp.register_message_handler(occupation_chosen, state=ShowVacancies.waiting_for_occupation)
    dp.register_message_handler(specialty_chosen, state=ShowVacancies.waiting_for_specialty)
    dp.register_message_handler(vacancy_chosen, state=ShowVacancies.waiting_for_vacancy)
    dp.register_message_handler(internship_chosen, state=ShowVacancies.waiting_for_internship)