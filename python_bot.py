import logging
import os
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("httpx").setLevel(
    logging.WARNING
)  # for disabling not informative messages from httpx


TOKEN_BOT = os.environ.get("TGBOT_API_KEY")
WHITE_LIST = {358201765: "Taras", 1049316533: "Dmitriy Demyanenko"}  # TODO del

client_ai = OpenAI()  # todo move to another class and file


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in WHITE_LIST:
        return
    # TODO change send_message to send_message_to_sender ? partitial or something like this
    await context.bot.send_message( 
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to ms"
    )


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in WHITE_LIST:
        msg = f"I Don't know you. But your id is {update.effective_chat.id}"
    else:
        msg = f"Hello, {WHITE_LIST[update.effective_chat.id]}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


async def open_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in WHITE_LIST:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Go away\n/start /hello")
        return

    text = update.message.text
    completion = client_ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": text},
        ],
    )
    answer_chatgpt = completion.choices[0].message
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=answer_chatgpt
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN_BOT).build()

    start_handler = CommandHandler("start", start)
    hello_handler = CommandHandler("hello", hello)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), open_ai)
    application.add_handler(start_handler)
    application.add_handler(hello_handler)
    application.add_handler(echo_handler)

    application.run_polling()
