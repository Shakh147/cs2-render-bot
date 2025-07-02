import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta
import random

API_TOKEN = os.environ.get("API_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

users = {}

skins = ['AK-47 | Redline', 'AWP | Asiimov', 'M4A1-S | Hyper Beast', 'Desert Eagle | Blaze', 'Glock-18 | Fade']

start_coins = 300
case_cost = 100

def get_keyboard():
    buttons = [
        [KeyboardButton("🎁 Tekin key ochish")],
        [KeyboardButton("💰 Coin holati"), KeyboardButton("🎮 Case ochish")],
        [KeyboardButton("📤 Withdraw"), KeyboardButton("ℹ️ Yordam")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    uid = message.from_user.id
    if uid not in users:
        users[uid] = {
            'coins': start_coins,
            'last_bonus': datetime.min
        }
    await message.answer("🎮 CS2 Free Key botiga xush kelibsiz!", reply_markup=get_keyboard())

@dp.message_handler(lambda m: m.text == "🎁 Tekin key ochish")
async def daily_key(message: types.Message):
    uid = message.from_user.id
    now = datetime.now()
    if uid not in users:
        users[uid] = {
            'coins': start_coins,
            'last_bonus': datetime.min
        }
    if now - users[uid]['last_bonus'] >= timedelta(days=1):
        users[uid]['last_bonus'] = now
        reward = random.choice(skins)
        await message.answer(f"🎉 Sizga tushdi: {reward}")
    else:
        await message.answer("⏳ Siz bugungi tekin keyni allaqachon ochgansiz. Ertaga yana urinib ko'ring!")

@dp.message_handler(lambda m: m.text == "💰 Coin holati")
async def check_coins(message: types.Message):
    uid = message.from_user.id
    if uid not in users:
        users[uid] = {
            'coins': start_coins,
            'last_bonus': datetime.min
        }
    coins = users[uid]['coins']
    await message.answer(f"💳 Sizda {coins} coin mavjud.")

@dp.message_handler(lambda m: m.text == "🎮 Case ochish")
async def open_case(message: types.Message):
    uid = message.from_user.id
    if uid not in users:
        users[uid] = {
            'coins': start_coins,
            'last_bonus': datetime.min
        }
    if users[uid]['coins'] >= case_cost:
        users[uid]['coins'] -= case_cost
        reward = random.choice(skins)
        await message.answer(f"🎉 Siz ochdingiz: {reward}")
    else:
        await message.answer("❌ Coin yetarli emas. Coin yig'ing yoki tekin key kuting.")

@dp.message_handler(lambda m: m.text == "📤 Withdraw")
async def withdraw(message: types.Message):
    await bot.send_message(ADMIN_ID, f"💸 Withdraw so'rovi: {message.from_user.id}")
    await message.answer("✅ So‘rovingiz yuborildi. Admin tez orada siz bilan bog‘lanadi.")

@dp.message_handler(lambda m: m.text == "ℹ️ Yordam")
async def help_message(message: types.Message):
    await message.answer("❓ Savollar uchun @admin bilan bog‘laning.
Har kuni tekin key ochish, coin orqali case ochish va withdraw mavjud.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)