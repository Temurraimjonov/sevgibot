from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7684977647:AAEAGnzAIabgR4sj71b5yKmi8P9Rp_e6VR0"  # bu yerga o'z bot tokeningizni yozing

# Ma'lumot to'plash bosqichlari
STEPS = ['name', 'age', 'height', 'girl_name', 'girl_age', 'girl_height']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["step"] = 0
    await update.message.reply_text("Salom! Sevgi mosligini aniqlovchi o'yinga xush kelibsiz!\nIsmingizni kiriting:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    step = context.user_data.get("step", 0)

    try:
        if step == 0:
            context.user_data["name"] = user_input
            await update.message.reply_text("Yoshingizni kiriting:")
        elif step == 1:
            context.user_data["age"] = int(user_input)
            await update.message.reply_text("Bo'yingizni sm da kiriting (masalan: 175):")
        elif step == 2:
            context.user_data["height"] = int(user_input)
            await update.message.reply_text("Sevgan qizingizning ismini kiriting:")
        elif step == 3:
            context.user_data["girl_name"] = user_input
            await update.message.reply_text("Uning yoshini kiriting:")
        elif step == 4:
            context.user_data["girl_age"] = int(user_input)
            await update.message.reply_text("Uning bo'yini sm da kiriting:")
        elif step == 5:
            context.user_data["girl_height"] = int(user_input)

            current_data = {
                "age": context.user_data['age'],
                "height": context.user_data['height'],
                "girl_age": context.user_data['girl_age'],
                "girl_height": context.user_data['girl_height']
            }

            prev_data = context.user_data.get("prev_info")

            if prev_data == current_data:
                love = context.user_data.get("prev_love_level", 50)
            else:
                love = calculate_love_level(
                    current_data["age"], current_data["height"],
                    current_data["girl_age"], current_data["girl_height"]
                )
                context.user_data["prev_info"] = current_data
                context.user_data["prev_love_level"] = love

            msg = f"💑 {context.user_data['name']} ❤️ {context.user_data['girl_name']}\n"
            msg += f"❤️ Sevgi darajasi: {love}%\n"
            msg += "🔁 /start buyrug‘i bilan yangidan boshlang"

            await update.message.reply_text(msg)
            context.user_data["step"] = 6
            return
        context.user_data["step"] += 1
    except:
        await update.message.reply_text("⚠️ Ma'lumot noto'g'ri. Iltimos, raqam ko'rinishida yozing.")

def calculate_love_level(age1, h1, age2, h2):
    love = 50
    age_diff = abs(age1 - age2)
    height_diff = abs(h1 - h2)

    if age_diff <= 3 and height_diff <= 5:
        love += 30
    elif age_diff <= 5 and height_diff <= 10:
        love += 20
    elif age_diff <= 10 and height_diff <= 15:
        love += 10

    # 5 lik sistema bo‘yicha yaxlitlash
    love = min(round(love / 5) * 5, 100)
    return love

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
