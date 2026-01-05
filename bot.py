
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import random

TOKEN = os.getenv("BOT_TOKEN")

questions = [
    {
        "q": "Which hormone regulates milk production in animals?",
        "a": "Prolactin"
    },
    {
        "q": "What is the normal gestation period of cow?",
        "a": "280 days"
    },
    {
        "q": "Which vitamin is responsible for blood clotting?",
        "a": "Vitamin K"
    },
    {
        "q": "Which fodder is rich in protein?",
        "a": "Lucerne"
    }
]

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🐄 IBPS AFO Quiz Bot\n\nCommands:\n/quiz - Get a question\n/answer - Show answer"
    )

def quiz(update: Update, context: CallbackContext):
    q = random.choice(questions)
    context.user_data["answer"] = q["a"]
    update.message.reply_text("❓ Question:\n" + q["q"])

def answer(update: Update, context: CallbackContext):
    ans = context.user_data.get("answer")
    if ans:
        update.message.reply_text("✅ Answer:\n" + ans)
    else:
        update.message.reply_text("First use /quiz")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("quiz", quiz))
    dp.add_handler(CommandHandler("answer", answer))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()