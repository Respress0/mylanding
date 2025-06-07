from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = '7536316813:AAEIdU7-lJvaYrHxHgrk8AeURy1_Ppt3J-g'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Нажми кнопку в Mini App, чтобы отправить свою геолокацию.")

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    latitude = location.latitude
    longitude = location.longitude

    await update.message.reply_text(f"Ты сейчас тут: 🌍\nШирота: {latitude}\nДолгота: {longitude}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))

    print("Бот запущен...")
    app.run_polling()
