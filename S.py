from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import JobQueue
import itertools

# --- CONFIG ---
BOT_TOKEN = '7620447701:AAHI49UiMBSDEo-dJku132fS4TnKl7jHeKY'
AUTHORIZED_USER_ID = 7660776851      # <-- apna Telegram ID daalo
CHAT_ID = -1002176107287            # <-- group ka ID daalo

# --- Globals ---
job = None 
message_cycle = None

# --- Command Handlers ---

def startloop(update: Update, context: CallbackContext):
    global job, message_cycle
    user_id = update.effective_user.id
    if user_id != AUTHORIZED_USER_ID:
        return

    if job is not None:
        update.message.reply_text("⚠️ Already looping!")
        return

    if not context.args:
        update.message.reply_text("Usage: /startloop msg1 | msg2 | msg3 ...")
        return

    full_text = ' '.join(context.args)
    messages = [msg.strip() for msg in full_text.split('|') if msg.strip()]
    
    if not messages:
        update.message.reply_text("❌ No valid messages.")
        return

    # Infinite cycle of messages
    message_cycle = itertools.cycle(messages)

    def send_next(context: CallbackContext):
        next_msg = next(message_cycle)
        context.bot.send_message(chat_id=CHAT_ID, text=next_msg)

    job = context.job_queue.run_repeating(send_next, interval=5, first=0)
    update.message.reply_text(f"✅ Started looping {len(messages)} messages every 5 seconds.")

def stoploop(update: Update, context: CallbackContext):
    global job
    user_id = update.effective_user.id
    if user_id != AUTHORIZED_USER_ID:
        return

    if job:
        job.schedule_removal()
        job = None
        update.message.reply_text("🛑 Loop stopped.")
    else:
        update.message.reply_text("⚠️ Loop is not running.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("startloop", startloop))
    dp.add_handler(CommandHandler("stoploop", stoploop))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
