import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from urllib.parse import quote

BOT_TOKEN = '8651719456:AAG1naOEDDLrD6JdeM3r7oVvlfyVJFYZq6Y'
TARGET_CHANNEL_ID = -1002161097295  # ID канала Makers Money

logging.basicConfig(level=logging.INFO)

async def forward_to_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем что сообщение не от бота
    if update.effective_user and update.effective_user.id == context.bot.id:
        return
    
    msg = update.effective_message
    author = update.effective_user
    message_text = msg.text or msg.caption or ""
    
    # Текст который подставится в поле ввода
    prefill = quote(f"Здравствуйте, я из канала Makers Money, я за заданием: {message_text[:100]}")
    
    # Ссылка на ЛС автора с готовым текстом
    if author.username:
        respond_url = f"https://t.me/{author.username}?text={prefill}"
    else:
        respond_url = f"https://t.me/{BOT_TOKEN.split(':')[0]}?text={prefill}"
    
    # Кнопки
    keyboard = [
        [InlineKeyboardButton("📋 ВЗЯТЬ ЗАДАНИЕ", url=respond_url)],
        [
            InlineKeyboardButton("💳 ВЫПЛАТЫ", url="https://t.me/Makersvuplaty"),
            InlineKeyboardButton("📚 ОБУЧЕНИЕ", url="https://t.me/djsjdhhfjd")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Отправляем в канал
    if msg.text:
        await context.bot.send_message(chat_id=TARGET_CHANNEL_ID, text=message_text, reply_markup=reply_markup)
    elif msg.photo:
        await context.bot.send_photo(chat_id=TARGET_CHANNEL_ID, photo=msg.photo[-1].file_id, caption=message_text, reply_markup=reply_markup)
    elif msg.video:
        await context.bot.send_video(chat_id=TARGET_CHANNEL_ID, video=msg.video.file_id, caption=message_text, reply_markup=reply_markup)
    elif msg.document:
        await context.bot.send_document(chat_id=TARGET_CHANNEL_ID, document=msg.document.file_id, caption=message_text, reply_markup=reply_markup)
    
    await update.message.reply_text("✅ Отправлено в канал!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Бот Makers Money запущен!\n\nОтправь любое сообщение, и оно улетит в канал с кнопками.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL, forward_to_channel))
    
    print("🚀 Бот Makers Money запущен")
    app.run_polling()

if __name__ == '__main__':
    main()
