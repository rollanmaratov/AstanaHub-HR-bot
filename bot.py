import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand

from app.handlers.apply import register_handlers_apply
from app.handlers.common import register_handlers_common, register_callback_query_handlers
from app.handlers.show_vacancies import register_handlers_show_vacancies

from loader import bot, dp


# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Стартовое приветствие"),
        BotCommand(command="/menu", description="Показать меню бота"),
        BotCommand(command="/apply", description="Подать на вакансию"),
        BotCommand(command="/show_vacancies", description="Посмотреть доступные вакансии"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_apply(dp)
    register_handlers_show_vacancies(dp)
    register_callback_query_handlers(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
