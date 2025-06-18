from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from fastapi import FastAPI, Request
import asyncio
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

BOT_TOKEN = '7536316813:AAEIdU7-lJvaYrHxHgrk8AeURy1_Ppt3J-g'
CHAT_ID = 678901234  # <-- ЗАМЕНИ на свой chat_id, когда узнаешь

bot = Bot(token=BOT_TOKEN)
app = FastAPI()

# --- Telegram bot handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Нажми кнопку в Mini App, чтобы отправить свою геолокацию.")

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    latitude = location.latitude
    longitude = location.longitude
    await update.message.reply_text(f"Ты сейчас тут: 🌍\nШирота: {latitude}\nДолгота: {longitude}")

async def handle_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print(f"[DEBUG] chat_id пользователя: {chat_id}")
    await update.message.reply_text(f"Ваш chat_id: `{chat_id}`", parse_mode="Markdown")

# --- FastAPI route for receiving coordinates from website ---

@app.post("/send-location")
async def send_location(request: Request):
    data = await request.json()
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude is None or longitude is None:
        return {"message": "Недостаточно данных"}

    try:
        await bot.send_location(chat_id=CHAT_ID, latitude=latitude, longitude=longitude)
        return {"message": "Геопозиция отправлена!"}
    except Exception as e:
        return {"message": f"Ошибка: {str(e)}"}

# --- Запуск Telegram бота ---

async def start_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_any_message))
    print("Бот запущен...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

# --- Запуск и FastAPI, и Telegram одновременно ---


# --- Lifespan: инициализация при старте приложения ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(start_bot())
    yield  # здесь FastAPI "ждёт", пока приложение работает

app = FastAPI(lifespan=lifespan)