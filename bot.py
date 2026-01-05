import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8535395184:AAFZZNc2q1GeS7qZV_ppNDakz0Aq4eYzxlQ"

# Question Bank (Add unlimited questions here)
QUESTIONS = [
    {
        "question": "Which hormone promotes cell elongation in plants?",
        "options": ["Auxin", "Gibberellin", "Cytokinin", "Ethylene"],
        "answer": "Auxin"
    },
    {
        "question": "What is the optimum pH range for most agricultural crops?",
        "options": ["4.0–5.0", "5.5–7.0", "7.5–9.0", "3.0–4.0"],
        "answer": "5.5–7.0"
    },
    {
        "question": "Which fertilizer contains the highest nitrogen content?",
        "options": ["DAP", "Urea", "Ammonium sulphate", "NPK"],
        "answer": "Urea"
    }
]

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id] = {
        "score": 0,
        "asked": []
    }
    await update.message.reply_text(
        "🌾 *IBPS AFO Mains Quiz Bot*\n\n"
        "Type /quiz to start practicing\n"
        "Type /score to see your score",
        parse_mode="Markdown"
    )

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    data = user_data.get(chat_id)

    remaining = [q for i, q in enumerate(QUESTIONS) if i not in data["asked"]]

    if not remaining:
        await update.message.reply_text("✅ You have attempted all questions!")
        return

    question = random.choice(remaining)
    q_index = QUESTIONS.index(question)
    data["asked"].append(q_index)

    buttons = [
        [InlineKeyboardButton(opt, callback_data=f"{q_index}|{opt}")]
        for opt in question["options"]
    ]

    await update.message.reply_text(
        f"❓ *{question['question']}*",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown"
    )

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    q_index, selected = query.data.split("|")
    q_index = int(q_index)

    correct = QUESTIONS[q_index]["answer"]
    chat_id = query.message.chat.id

    if selected == correct:
        user_data[chat_id]["score"] += 1
        text = "✅ Correct!"
    else:
        text = f"❌ Wrong!\nCorrect Answer: *{correct}*"

    await query.edit_message_text(text, parse_mode="Markdown")

async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s = user_data.get(update.effective_chat.id, {}).get("score", 0)
    await update.message.reply_text(f"📊 Your Score: *{s}*", parse_mode="Markdown")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("quiz", quiz))
app.add_handler(CommandHandler("score", score))
app.add_handler(CallbackQueryHandler(answer))

app.run_polling()
