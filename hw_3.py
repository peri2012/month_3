from aiogram import Bot, Dispatcher, types, executor
from config import lesson_3
import logging, sqlite3, time
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext



bot = Bot(token=lesson_3)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
bot = Bot(token=lesson_3)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)  

connect = sqlite3.connect("data_bases/lesson_2.db")
cursor = connect.cursor()




connect = sqlite3.connect("data.db")
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS user(
               id INTEGER PRIMARY KEY,
               user_id VARCHAR(255),
               first_name VARCHAR(255),
               last_name VARCHAR(255),
               age INTEGER,
               experince UNTEGER,
               created_at VARCHAR(255)
)""")

@dp.message_handler(commands='start' )
async def start(message:types.Message):
    await message.answer("заполнение анкеты")
 
class ApplicationState(StatesGroup):
    first_name = State()
    last_name = State()
    age = State()
    experince = State()
    created_at = State()

@dp.message_handler(text="Заполнить анкету")
async def to_applicate(message:types.Message):
    await message.answer("Ваше имя?")
    await ApplicationState.first_name.set()

@dp.message_handler(state=ApplicationState.first_name)
async def get_last_name(message:types.Message, state:FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Ваша фамилия?")
    await ApplicationState.next()

@dp.message_handler(state=ApplicationState.last_name)
async def get_last_name(message:types.Message, state:FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer("ваш возраст?")
    await ApplicationState.next()

@dp.message_handler(state=ApplicationState.age)
async def get_last_name(message:types.Message, state:FSMContext):
    await state.update_data(age=message.text)
    await message.answer("ваш опыт работы?")
    await ApplicationState.next()

@dp.message_handler(state=ApplicationState.experince)
async def get_last_name(message:types.Message, state:FSMContext):
    await state.update_data(experince=message.text)
    await message.answer("дата регистрации?", reply_markup=courses_keybords)
    await ApplicationState.next