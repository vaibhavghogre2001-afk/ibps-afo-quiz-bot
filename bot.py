import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

QUESTIONS = [
    {"q": "Which nutrient is most important for plant growth?", "a": "Nitrogen"},
    {"q": "Full form of NPK?", "a": "Nitrogen Phosphorus Potassium"},
    {"q": "Which hormone causes cell elongation?", "a": "Auxin"},
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to IBPS AFO Quiz Bot 📘\nUse /quiz to get a question."
    )

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = random.choice(QUESTIONS)
    await update.message.reply_text(
        f"❓ {q['q']}\n\n✅ Answer: {q['a']}"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.run_polling()

if __name__ == "__main__":
    main()