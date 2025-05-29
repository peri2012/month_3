from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
import sqlite3, logging, time
from config import lesson_2

bot = Bot(token=lesson_2)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

u_connect = sqlite3.connect("data_bases/users.db", check_same_thread=False)
u_cursor = u_connect.cursor()

u_cursor.execute("""CREATE TABLE IF NOT EXISTS user(
                 id INTEGER PRIMARY KEY,
                 user_id VARCHAR(255),
                 first_name VARCHAR(255),
                 last_name VARCHAR(255),
                 wallet_id VARCHAR(16),
                 balance INTEGER DEFAULT 0,
                 created_at VARCHAR(255)
)""")
u_connect.commit()

t_connect = sqlite3.connect("data_bases/transfers.db", check_same_thread=False)
t_cursor = t_connect.cursor()

t_cursor.execute("""CREATE TABLE IF NOT EXISTS transfer(
                 id INTEGER PRIMARY KEY,
                 fullname VARCHAR(255),
                 wallet_id VARCHAR(16),
                 amount INTEGER,
                 created_at VARCHAR(255)
)""")
t_connect.commit()

class TransferState(StatesGroup):
    recipient_wallet_id = State()
    amount = State()

@dp.message_handler(commands="transfer")
async def transfer(message:types.Message, state:FSMContext):
    u_cursor.execute("SELECT * FROM user WHERE user_id = ?", (message.from_user.id,))
    result = u_cursor.fetchall()

    async with state.proxy() as data:
            data["fullname"] = result[0][2] + " " + result[0][3]
            data["wallet_id"] = result[0][4]
    
    await message.answer("Введите лицевой счет вашего получателя:")
    await TransferState.recipient_wallet_id.set()

@dp.message_handler(state=TransferState.recipient_wallet_id)
async def get_recipient_wallet_id(message:types.Message, state:FSMContext):
    u_cursor.execute("SELECT * FROM user WHERE wallet_id = ?", (message.text,))
    result = u_cursor.fetchall()

    if result == []:
        await message.answer("Такой лицевой счет не существует")
    else:
       

        await message.answer("Введите сумму которую хотите перевести:")
        await TransferState.next()

@dp.message_handler(state=TransferState.amount)
async def amount(message:types.Message, state:FSMContext):
    u_cursor.execute("SELECT balance FROM user WHERE user_id = ?", (message.from_user.id,))
    result = u_cursor.fetchall()

    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите корректную сумму (целое число).")
        return

    amount = int(message.text)

    
    if amount > result[0][0]:
        async with state.proxy() as data:
            data["amount"] = message.text
            data["created_at"] = time.asctime()
        await TransferState.last()

        u_cursor.execute("SELECT user_id FROM user WHERE wallet_id = ?", (data["recipient_wallet_id"],))
        result = u_cursor.fetchall()

        t_cursor.execute(
        "INSERT INTO transfer(fullname, wallet_id,  amount, created_at) VALUES(?, ?, ?, ?, ?, ?)",
            (
                data["fullname"],
                data["wallet_id"],
                data["amount"],
                data["created_at"]
            )
        )
        t_connect.commit()
 

        await state.finish()
        await bot.send_message(result[0][0], f"Ваш баланс пополнен на: {data['amount']} сом")
        await message.answer("Вы успешно перевели деньги.")
        

executor.start_polling(dp)