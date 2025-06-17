from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import itertools

BOT_TOKEN = '7620447701:AAHI49UiMBSDEo-dJku132fS4TnKl7jHeKY'
AUTHORIZED_USER_ID = 7660776851
CHAT_ID = -1002176107287

message_cycle = None
job_ref = None

async def startloop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global message_cycle, job_ref

    if update.effective_user.id != AUTHORIZED_USER_ID:
        return

    if job_ref is not None:
        await update.message.reply_text("⚠️ Already looping!")
        return

    if not context.args:
        await update.message.reply_text("Usage: /startloop msg1 | msg2 | msg3 ...")
        return

    full_text = ' '.join(context.args)
    messages = [msg.strip() for msg in full_text.split('|') if msg.strip()]
    message_cycle = itertools.cycle(messages)

    async def send_next(context: ContextTypes.DEFAULT_TYPE):
        next_msg = next(message_cycle)
        await context.bot.send_message(chat_id=CHAT_ID, text=next_msg)

    job_ref = context.job_queue.run_repeating(send_next, interval=5, first=0)
    await update.message.reply_text("✅ Loop started.")

async def stoploop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global job_ref

    if update.effective_user.id != AUTHORIZED_USER_ID:
        return

    if job_ref:
        job_ref.schedule_removal()
        job_ref = None
        await update.message.reply_text("🛑 Loop stopped.")
    else:
        await update.message.reply_text("⚠️ Loop not running.")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("startloop", startloop))
    application.add_handler(CommandHandler("stoploop", stoploop))

    application.run_polling()

if __name__ == "__main__":
    main()
