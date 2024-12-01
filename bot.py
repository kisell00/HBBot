import os
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

# Зберігатимемо дні народження в словнику (можна замінити на базу даних)
birthdays = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я допоможу вам слідкувати за днями народження. Використовуйте /add_birthday, щоб додати.")

async def add_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 2:
            raise ValueError("Вкажіть ім'я і дату (у форматі: ДД.ММ)")
        
        name = args[0]
        date = datetime.datetime.strptime(args[1], "%d.%m").date()
        birthdays[name] = date
        await update.message.reply_text(f"День народження {name} додано на {date.strftime('%d.%m')}")
    except Exception as e:
        await update.message.reply_text(f"Помилка: {str(e)}")

async def check_birthdays(context: ContextTypes.DEFAULT_TYPE):
    today = datetime.date.today()
    for name, date in birthdays.items():
        if date.day == today.day and date.month == today.month:
            await context.bot.send_message(chat_id=context.job.chat_id, text=f"🎉 Вітаємо {name} з Днем народження!")

async def schedule_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    context.job_queue.run_daily(check_birthdays, time=datetime.time(9, 0), chat_id=chat_id)
    await update.message.reply_text("Щоденна перевірка днів народження запланована на 9:00.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_birthday", add_birthday))
    app.add_handler(CommandHandler("schedule", schedule_jobs))

    print("Бот запущено!")
    app.run_polling()
