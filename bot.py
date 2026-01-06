import os
import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

QUESTIONS = [
    {
        "question": "IBPS AFO exam is conducted by?",
        "options": ["RBI", "IBPS", "NABARD", "SBI"],
        "answer": "IBPS",
    },
    {
        "question": "Main focus of AFO is?",
        "options": ["IT", "Agriculture", "Law", "Marketing"],
        "answer": "Agriculture",
    },
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to IBPS AFO Quiz Bot!\n\nType /quiz to start quiz."
    )


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = random.choice(QUESTIONS)
    text = f"❓ {q['question']}\n\n"
    for i, opt in enumerate(q["options"], 1):
        text += f"{i}. {opt}\n"
    text += "\nReply with option number (1-4)."

    context.user_data["answer"] = q["answer"]
    context.user_data["options"] = q["options"]

    await update.message.reply_text(text)


async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "answer" not in context.user_data:
        return

    try:
        choice = int(update.message.text) - 1
        selected = context.user_data["options"][choice]
        correct = context.user_data["answer"]

        if selected == correct:
            await update.message.reply_text("✅ Correct!")
        else:
            await update.message.reply_text(f"❌ Wrong! Correct answer: {correct}")
    except:
        await update.message.reply_text("Please reply with a number (1-4).")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(
        CommandHandler("answer", check_answer)
    )

    app.add_handler(
        telegram.ext.MessageHandler(
            telegram.ext.filters.TEXT & ~telegram.ext.filters.COMMAND,
            check_answer,
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()