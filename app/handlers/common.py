from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from app.handlers.apply import apply_start


async def cmd_start(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    menu_button = types.InlineKeyboardButton(text="Перейти в меню▶️", callback_data='/menu')
    keyboard.add(menu_button)
    await message.answer(
        "Добро пожаловать в HR чат бот Astana Hub!\n"
        "Чтобы перейти в меню бота, нажмите команду /menu",
        reply_markup=keyboard
    )
    await state.finish()


async def cmd_menu(message: types.Message, state: FSMContext):
    await message.answer(
        "Подайте на вакансию через команду /apply\n"
        "Посмотрите вакансии через команду /show_vacancies",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.finish()


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


async def go_to_menu(call: types.CallbackQuery):
    print("spmethong "+ call.data)
    await call.message.answer(
        "Подайте на вакансию через команду /apply\n"
        "Посмотрите вакансии через команду /show_vacancies"
    )
    await call.answer()


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_menu, commands="menu", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")


def register_callback_query_handlers(dp: Dispatcher):
    dp.callback_query_handler(apply_start, func=lambda message: True)
    dp.callback_query_handler(go_to_menu, Text)
