from aiogram import Bot, Dispatcher, types, executor

bot = Bot(token="7806464278:AAFBJdyAPKYhCZ7d1EKMxy1sIjkFuQIkZFY")
dp = Dispatcher(bot)

@dp.message_handler(commands='start' )
async def start(message:types.Message):
    await message.answer("Добро пожаловать на наш Бот!")

executor.start_polling(dp)