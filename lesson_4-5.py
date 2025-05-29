from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
import sqlite3, logging, time, random, asyncio
from config import lesson_2

bot = Bot(token=lesson_2)
storage  = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)


u_connect = sqlite3.connect("databases/users.db", check_same_thread=False)
u_cursor = u_connect.cursor()

u_cursor.execute("""CREATE TABLE IF NOT EXISTS user(
                 id INTEGER PRIMARY KEY,
                 user_id VARCHAR   )
""")