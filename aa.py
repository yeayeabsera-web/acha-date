# =====================================================
# 🍋 ACHA DATING BOT - FULL FIXED VERSION
# =====================================================

import logging
import random
import sqlite3

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# =====================================================
# CONFIG
# =====================================================

TOKEN = ("8476171509:AAEQRPdV6n4BRYK01D82ivufhOjlPq2ny-4")

ADMINS = [8460165874]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# =====================================================
# DATABASE
# =====================================================

conn = sqlite3.connect("dating.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    looking_for TEXT,
    city TEXT,
    bio TEXT,
    photo TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS likes (
    user_id INTEGER,
    liked_user INTEGER,
    UNIQUE(user_id, liked_user)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    user1 INTEGER,
    user2 INTEGER,
    UNIQUE(user1, user2)
)
""")

conn.commit()

# =====================================================
# STATES
# =====================================================

(
    NAME,
    AGE,
    GENDER,
    LOOKING,
    CITY,
    BIO,
    PHOTO,
    EDIT_NAME,
) = range(8)

# =====================================================
# PICKUP LINES
# =====================================================

pickup_lines = [
    "You look amazing ❤️",
    "I think we matched for a reason 💕",
    "Your smile is beautiful 😍",
    "You have amazing energy ✨",
]

# =====================================================
# MENU
# =====================================================

def bottom_menu():
    keyboard = [
        ["❤️ Find Match"],
        ["👤 Profile", "✏️ Edit Profile"],
        ["🔥 My Matches", "🏠 Start"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

# =====================================================
# START
# =====================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )

    profile = cursor.fetchone()

    if profile:
        await update.message.reply_text(
            f"🍋 Welcome back {profile[2]} ❤️",
            reply_markup=bottom_menu()
        )
        return

    keyboard = [
        [
            InlineKeyboardButton(
                "❤️ Create Profile",
                callback_data="create_profile"
            )
        ]
    ]

    text = """
🍋 ACHA DATING BOT ❤️

🔥 Ethiopian Dating Bot

• Smart Matching
• Real Match Notifications
• Pickup Lines
• Real Connections
"""

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =====================================================
# CREATE PROFILE
# =====================================================

async def start_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "👤 Send your name:"
    )

    return NAME

# =====================================================
# NAME
# =====================================================

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["name"] = update.message.text

    await update.message.reply_text(
        "🎂 Send your age:"
    )

    return AGE

# =====================================================
# AGE
# =====================================================

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        age = int(update.message.text)

        if age < 18:
            await update.message.reply_text(
                "❌ Only 18+ users allowed."
            )
            return AGE

        context.user_data["age"] = age

    except:
        await update.message.reply_text(
            "❌ Please send a valid age."
        )
        return AGE

    keyboard = ReplyKeyboardMarkup(
        [["👨 Man", "👩 Woman"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        "🧑 Select your gender:",
        reply_markup=keyboard
    )

    return GENDER

# =====================================================
# GENDER
# =====================================================

async def get_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["gender"] = update.message.text

    keyboard = ReplyKeyboardMarkup(
        [["👨 Man", "👩 Woman"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        "❤️ Looking for:",
        reply_markup=keyboard
    )

    return LOOKING

# =====================================================
# LOOKING FOR
# =====================================================

async def get_looking(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["looking_for"] = update.message.text

    await update.message.reply_text(
        "🌍 Send your city:"
    )

    return CITY

# =====================================================
# CITY
# =====================================================

async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["city"] = update.message.text

    await update.message.reply_text(
        "📝 Write your bio:",
        reply_markup=ReplyKeyboardRemove()
    )

    return BIO

# =====================================================
# BIO
# =====================================================

async def get_bio(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["bio"] = update.message.text

    await update.message.reply_text(
        "📸 Send your profile photo:"
    )

    return PHOTO

# =====================================================
# PHOTO
# =====================================================

async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if not update.message.photo:
        await update.message.reply_text(
            "❌ Please send a photo."
        )
        return PHOTO

    photo_id = update.message.photo[-1].file_id

    cursor.execute("""
    INSERT OR REPLACE INTO users
    (user_id, username, name, age, gender,
    looking_for, city, bio, photo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user.id,
        user.username,
        context.user_data["name"],
        context.user_data["age"],
        context.user_data["gender"],
        context.user_data["looking_for"],
        context.user_data["city"],
        context.user_data["bio"],
        photo_id
    ))

    conn.commit()

    await update.message.reply_text(
        "✅ Profile created successfully ❤️",
        reply_markup=bottom_menu()
    )

    return ConversationHandler.END

# =====================================================
# FIND MATCH
# =====================================================

async def match(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )

    me = cursor.fetchone()

    if not me:
        return

    my_gender = me[4]
    looking_for = me[5]

    cursor.execute("""
    SELECT * FROM users
    WHERE user_id != ?
    AND gender = ?
    AND looking_for = ?
    AND user_id NOT IN (
        SELECT liked_user FROM likes WHERE user_id = ?
    )
    ORDER BY RANDOM()
    LIMIT 1
    """, (
        user_id,
        looking_for,
        my_gender,
        user_id
    ))

    target = cursor.fetchone()

    if not target:
        await update.message.reply_text(
            "😔 No more matches found."
        )
        return

    target_id = target[0]

    keyboard = [
        [
            InlineKeyboardButton(
                "❤️ Like",
                callback_data=f"like_{target_id}"
            ),
            InlineKeyboardButton(
                "❌ Skip",
                callback_data=f"skip_{target_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                "💌 Pickup Line",
                callback_data=f"pickup_{target_id}"
            )
        ]
    ]

    caption = f"""
❤️ {target[2]}

🎂 Age: {target[3]}
🌍 City: {target[6]}

📝 Bio:
{target[7]}
"""

    await update.message.reply_photo(
        photo=target[8],
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =====================================================
# PROFILE
# =====================================================

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )

    profile_data = cursor.fetchone()

    if not profile_data:
        return

    caption = f"""
👤 {profile_data[2]}

🎂 Age: {profile_data[3]}
🧑 Gender: {profile_data[4]}
❤️ Looking For: {profile_data[5]}
🌍 City: {profile_data[6]}

📝 Bio:
{profile_data[7]}
"""

    await update.message.reply_photo(
        photo=profile_data[8],
        caption=caption
    )

# =====================================================
# EDIT PROFILE
# =====================================================

async def edit_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "✏️ Send your new name:"
    )

    return EDIT_NAME

async def save_new_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    new_name = update.message.text

    cursor.execute(
        "UPDATE users SET name = ? WHERE user_id = ?",
        (new_name, user_id)
    )

    conn.commit()

    await update.message.reply_text(
        "✅ Profile updated successfully.",
        reply_markup=bottom_menu()
    )

    return ConversationHandler.END

# =====================================================
# BUTTONS
# =====================================================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    action, target_id = data.split("_")
    target_id = int(target_id)

    user_id = query.from_user.id

    # LIKE
    if action == "like":

        try:
            cursor.execute(
                "INSERT INTO likes VALUES (?, ?)",
                (user_id, target_id)
            )
            conn.commit()

        except:
            pass

        # CHECK MATCH
        cursor.execute("""
        SELECT * FROM likes
        WHERE user_id = ?
        AND liked_user = ?
        """, (
            target_id,
            user_id
        ))

        already_liked = cursor.fetchone()

        if already_liked:

            try:
                cursor.execute(
                    "INSERT INTO matches VALUES (?, ?)",
                    (user_id, target_id)
                )
                conn.commit()
            except:
                pass

            await context.bot.send_message(
                chat_id=user_id,
                text="🎉 It's a MATCH ❤️"
            )

            await context.bot.send_message(
                chat_id=target_id,
                text="🎉 It's a MATCH ❤️"
            )

        await query.edit_message_caption(
            caption="❤️ Liked"
        )

    # SKIP
    elif action == "skip":

        await query.edit_message_caption(
            caption="❌ Skipped"
        )

    # PICKUP LINE
    elif action == "pickup":

        line = random.choice(pickup_lines)

        await context.bot.send_message(
            chat_id=target_id,
            text=f"💌 Pickup Line:\n\n{line}"
        )

# =====================================================
# MY MATCHES
# =====================================================

async def my_matches(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    cursor.execute("""
    SELECT * FROM matches
    WHERE user1 = ? OR user2 = ?
    """, (
        user_id,
        user_id
    ))

    matches = cursor.fetchall()

    if not matches:
        await update.message.reply_text(
            "😔 No matches yet."
        )
        return

    text = "🔥 Your Matches:\n\n"

    for match_data in matches:

        other_user = (
            match_data[1]
            if match_data[0] == user_id
            else match_data[0]
        )

        cursor.execute(
            "SELECT name FROM users WHERE user_id = ?",
            (other_user,)
        )

        user_data = cursor.fetchone()

        if user_data:
            text += f"❤️ {user_data[0]}\n"

    await update.message.reply_text(text)

# =====================================================
# ADMIN
# =====================================================

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMINS:

        await update.message.reply_text(
            "❌ Admin only."
        )
        return

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    await update.message.reply_text(
        f"👑 ADMIN PANEL\n\n👥 Users: {total_users}"
    )

# =====================================================
# MENU BUTTONS
# =====================================================

async def menu_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "❤️ Find Match":
        await match(update, context)

    elif text == "👤 Profile":
        await profile(update, context)

    elif text == "🔥 My Matches":
        await my_matches(update, context)

    elif text == "🏠 Start":
        await start(update, context)

# =====================================================
# CANCEL
# =====================================================

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "❌ Cancelled."
    )

    return ConversationHandler.END

# =====================================================
# MAIN
# =====================================================

def main():

    app = Application.builder().token(TOKEN).build()

    # CREATE PROFILE
    create_profile_handler = ConversationHandler(

        entry_points=[
            CallbackQueryHandler(
                start_profile,
                pattern="^create_profile$"
            )
        ],

        states={

            NAME: [
                MessageHandler(filters.TEXT, get_name)
            ],

            AGE: [
                MessageHandler(filters.TEXT, get_age)
            ],

            GENDER: [
                MessageHandler(filters.TEXT, get_gender)
            ],

            LOOKING: [
                MessageHandler(filters.TEXT, get_looking)
            ],

            CITY: [
                MessageHandler(filters.TEXT, get_city)
            ],

            BIO: [
                MessageHandler(filters.TEXT, get_bio)
            ],

            PHOTO: [
                MessageHandler(filters.PHOTO, get_photo)
            ],
        },

        fallbacks=[
            CommandHandler("cancel", cancel)
        ]
    )

    # EDIT PROFILE
    edit_handler = ConversationHandler(

        entry_points=[
            MessageHandler(
                filters.Regex("^✏️ Edit Profile$"),
                edit_profile
            )
        ],

        states={
            EDIT_NAME: [
                MessageHandler(filters.TEXT, save_new_name)
            ]
        },

        fallbacks=[
            CommandHandler("cancel", cancel)
        ]
    )

    # HANDLERS
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))

    app.add_handler(create_profile_handler)
    app.add_handler(edit_handler)

    app.add_handler(CallbackQueryHandler(buttons))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            menu_buttons
        )
    )

    print("🍋 ACHA DATING BOT RUNNING...")

    app.run_polling()

# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":
    main()