from aiogram import Bot, Dispatcher, types, executor
from config import lesson_2
import logging, sqlite3, time
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext

bot = Bot(token=lesson_2)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

connect = sqlite3.connect("data_bases/lesson_2.db")
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS user(
               id INTEGER PRIMARY KEY,
               user_id VARCHAR(255),
               first_name VARCHAR(255),
               last_name VARCHAR(255),
               username VARCHAR(255),
               created_at VARCHAR(255)
)""")

connect.commit()

connect_2 = sqlite3.connect("data_bases/to_applicate_2.db")
cursor_2 = connect_2.cursor()

cursor_2.execute("""CREATE TABLE IF NOT EXISTS application(
               id INTEGER PRIMARY KEY,
               user_id VARCHAR(255),
               first_name VARCHAR(255),
               last_name VARCHAR(255),
               phone_number VARCHAR(255),
               direction VARCHAR(255),
               created_at VARCHAR(255)
)""")

connect_2.commit()

start_buttons = [
    types.KeyboardButton("О нас"),
    types.KeyboardButton("Адрес"),
    types.KeyboardButton("Курсы"),
    types.KeyboardButton("Подать заявку"),
]
start_keybords = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    cursor.execute(f"""SELECT user_id FROM user WHERE user_id = {message.from_user.id}""")
    data = cursor.fetchall()

    if data == []:
        cursor.execute("""INSERT INTO user(user_id, first_name, last_name, username, created_at) VALUES(?, ?, ?, ?, ?)""", (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, time.ctime()))
        connect.commit()
    
    await message.answer(f"Здраствуйте {message.from_user.full_name}", reply_markup=start_keybords)

@dp.message_handler(text="О нас")
async def about_us(message:types.Message):
    await message.answer("Мы IT компания")

@dp.message_handler(text="Адрес")
async def adres(message:types.Message):
    await message.answer("Наш адрес: Ресторан Кубаныч")
    await message.answer_location(40.70568720630816, 72.87988369964728)

courses_buttons = [
    types.KeyboardButton("BackEnd"),
    types.KeyboardButton("FrontEnd"),
    types.KeyboardButton("IOS"),
    types.KeyboardButton("Назад"),
]
courses_keybords = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*courses_buttons)

@dp.message_handler(text="Курсы")
async def course(message:types.Message):
    await message.answer("Наш курсы: ", reply_markup=courses_keybords)

@dp.message_handler(text='BackEnd')
async def backend(message:types.Message):
    await message.reply("BackEnd - it's back side of site that you never see")

@dp.message_handler(text='FrontEnd')
async def frontend(message:types.Message):
    await message.reply("FrontEnd - it's front side of site that you always see")

@dp.message_handler(text='IOS')
async def ios(message:types.Message):
    await message.reply("IOS - it's an app for OS Apple")

@dp.message_handler(text='Назад')
async def rollback(message:types.Message):
    await start(message)


class ApplicationState(StatesGroup):
    first_name = State()
    last_name = State()
    phone_number = State()
    direction = State()

@dp.message_handler(text="Подать заявку")
async def to_applicate(message:types.Message):
    await message.answer("Ваша имя?")
    await ApplicationState.first_name.set()

@dp.message_handler(state=ApplicationState.first_name)
async def get_last_name(message:types.Message, state:FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Ваша фамилия?")
    await ApplicationState.next()

@dp.message_handler(state=ApplicationState.last_name)
async def get_phone_number(message:types.Message, state:FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer("Номер телефона?")
    await ApplicationState.next()

@dp.message_handler(state=ApplicationState.phone_number)
async def get_direction(message:types.Message, state:FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer("Направление?", reply_markup=courses_keybords)
    await ApplicationState.next()

@dp.message_handler(state=ApplicationState.direction)
async def get_direction(message:types.Message, state:FSMContext):
    await state.update_data(direction=message.text)
    await ApplicationState.last()
    await message.answer("Ваши данные успешно сохранены.")
    result = await storage.get_data(user=message.from_user.id)
    send_message = f"""{time.ctime()}
Заявка на курсы
Имя: {result['first_name']}
Фамилия: {result['last_name']}
Номер телефона: {result['phone_number']}
Направление: {result['direction']}"""
    
    cursor_2.execute("""INSERT INTO application(user_id, first_name, last_name, phone_number, direction, created_at) VALUES(?, ?, ?, ?, ?, ?)""", (message.from_user.id, result['first_name'], result['last_name'], result['phone_number'], result['direction'], time.ctime()))
    connect_2.commit()

    await message.answer(send_message)
    await bot.send_message(-4750747214, f"{send_message}")

executor.start_polling(dp)