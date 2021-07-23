from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sheets.sheets import sheet


vacancies = {
    "Разработка": ["Full-Stack Разработчик", "UI/UX дизайнер"],
    "Финансы": ["Директор финансового офиса", "Казначей"],
    "HR": ["Менеджер HR", "Директор HR", "Ресепшионист"]
}

internships = {
    "Стажер в HR офис": "Вставьте описание стажировки HR сюда",
    "Стажер в PR офис": "Вставьте описание стажировки PR сюда",
    "Стажер в образовательный офис": "Вставьте описание образвательной стажировки сюда"
}


class ApplyForVacancy(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_specialty = State()
    # waiting_for_cv = State()
    waiting_for_vacancies = State()
    waiting_for_test_to_end = State()


async def apply_start(message: types.Message):
    await message.answer("Введите Ваше имя и фамилию:")
    await ApplyForVacancy.waiting_for_full_name.set()


# Обратите внимание: есть второй аргумент
async def name_gotten(message: types.Message, state: FSMContext):
    if len(message.text.split()) != 2:
        await message.answer("Пожалуйста, введите корректную информацию")
        return
    await state.update_data(full_name=message.text.capitalize())
    sheet.update_cell(2, 1, message.text)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for key, value in vacancies.items():
        keyboard.add(key)
    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await ApplyForVacancy.next()
    await message.answer("Теперь выберите специализацию:", reply_markup=keyboard)


async def specialty_chosen(message: types.Message, state: FSMContext):
    if message.text not in vacancies.keys():
        await message.answer("Пожалуйста, выберите специализацию, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_specialty=message.text)
    sheet.update_cell(2, 3, message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_data = await state.get_data()
    for vacancy in vacancies[user_data['chosen_specialty']]:
        keyboard.add(vacancy)
    await ApplyForVacancy.next()
    await message.answer("Теперь выберите подходящую вакансию:", reply_markup=keyboard)


async def vacancy_chosen(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    print(*vacancies[user_data['chosen_specialty']])
    if message.text not in vacancies[user_data['chosen_specialty']]:
        await message.answer("Пожалуйста, выберите вакансию используя клавиатуру ниже.")
        return
    sheet.update_cell(2, 4, message.text)
    await state.update_data(chosen_vacancy=message.text)
    await message.answer(f"Поздравляю, {user_data['full_name']}, Вы успешно подали заявку на"
                         f"вакансию {message.text}!\n", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_apply(dp: Dispatcher):
    dp.register_message_handler(apply_start, commands="apply", state="*")
    dp.register_message_handler(name_gotten, state=ApplyForVacancy.waiting_for_full_name)
    dp.register_message_handler(specialty_chosen, state=ApplyForVacancy.waiting_for_specialty)
    dp.register_message_handler(vacancy_chosen, state=ApplyForVacancy.waiting_for_vacancies)
