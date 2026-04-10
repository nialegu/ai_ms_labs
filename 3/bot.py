import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from config import BOT_TOKEN
from chat_handler import init_chat_system, get_response

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger("bot")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте. Я бот-консультант по смартфонам.\n\n"
        "Я могу рассказать про:\n"
        "- iPhone\n"
        "- Samsung Galaxy\n"
        "- Google Pixel\n\n"
        "Напишите ваш вопрос."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доступные возможности:\n"
        "- информация о смартфонах\n"
        "- сравнение моделей\n"
        "- помощь в выборе\n"
        "- ответы на общие вопросы\n\n"
        "Введите сообщение."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    reply = get_response(text, user_id)
    await update.message.reply_text(reply)


def main():
    init_chat_system()
    logger.info("Bot started")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()