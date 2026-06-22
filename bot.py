from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8841113029:AAEBh_BtZuyGZzhrCxG59ZJAHbG632_aaoI"

CHANNELS = ["@channel1", "@channel2"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("عضو شدم ✅", callback_data="check")]
    ]
    await update.message.reply_text(
        "برای استفاده از ربات اول باید عضو کانال‌ها بشی 👇",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def check_membership(user_id, context):
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(channel, user_id)
            if member.status in ["left", "kicked"]:
                return False
        except:
            return False
    return True

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if await check_membership(user_id, context):
        msg = await query.message.reply_video(
            video="VIDEO_FILE_ID",
            caption="اینم فیلم 😎"
        )

        # حذف بعد از 30 ثانیه
        import asyncio
        await asyncio.sleep(30)
        await context.bot.delete_message(chat_id=msg.chat_id, message_id=msg.message_id)

    else:
        await query.message.reply_text("هنوز عضو کانال‌ها نشدی ❌")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
