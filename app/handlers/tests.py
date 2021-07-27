from app.handlers.apply import ApplyForVacancy
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from google_services.tests_sheets import test_sheet

data = test_sheet.get_all_records()

async def test():
    pass