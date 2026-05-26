# =====================================================
# ❤️ ACHADATE BOT - FULL FINAL VERSION
# Python 3.14 + python-telegram-bot 20.7
# =====================================================

import asyncio
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

TOKEN = "8476171509:AAEQRPdV6n4BRYK01D82ivufhOjlPq2ny-4"

ADMINS = [
    8460165874,
]

# =====================================================
# LOGGING
# =====================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# =====================================================
# DATABASE
# =====================================================

conn = sqlite3.connect(
    "achadate.db",
    check_same_thread=False
)

cursor = conn.cursor()

# USERS
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

# LIKES
cursor.execute("""
CREATE TABLE IF NOT EXISTS likes (
    user_id INTEGER,
    liked_user INTEGER,
    UNIQUE(user_id, liked_user)
)
""")

# DISLIKES
cursor.execute("""
CREATE TABLE IF NOT EXISTS dislikes (
    user_id INTEGER,
    disliked_user INTEGER,
    UNIQUE(user_id, disliked_user)
)
""")

# MATCHES
cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    user1 INTEGER,
    user2 INTEGER,
    UNIQUE(user1, user2)
)
""")

# REPORTS
cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    reporter INTEGER,
    target INTEGER,
    reason TEXT
)
""")

# BLOCKS
cursor.execute("""
CREATE TABLE IF NOT EXISTS blocks (
    blocker INTEGER,
    blocked INTEGER
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

    "You look like my favorite notification ❤️",

    "Are you WiFi? Because I feel connected 😏",

    "You just upgraded my mood instantly 💫",

    "You must be magic because everyone disappears when I look at you ✨",

    "Are you a camera? Because you make me smile 📸",

    "You must be a keyboard because you're my type ⌨️",

    "You’re the reason this app feels worth downloading ❤️",
]

# =====================================================
# MENU
# =====================================================

def main_menu():

    keyboard = [

        ["❤️ Find Match"],

        ["👤 My Profile", "✏️ Edit Profile"],

        ["🔥 My Matches", "⚙️ Settings"],

    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

# =====================================================
# START
# =====================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    user_id = user.id

    # ADMIN NOTIFICATION
    for admin_id in ADMINS:

        try:

            username = (
                f"@{user.username}"
                if user.username
                else "No Username"
            )

            await context.bot.send_message(
                chat_id=admin_id,
                text=(
                    f"🆕 New User Started Bot\n\n"
                    f"👤 Name: {user.first_name}\n"
                    f"🆔 ID: {user.id}\n"
                    f"📩 Username: {username}"
                )
            )

        except Exception as e:
            print(e)

    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )

    profile = cursor.fetchone()

    # EXISTING USER
    if profile:

        await update.message.reply_text(
            f"❤️ Welcome Back {profile[2]}",
            reply_markup=main_menu()
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
❤️ ACHADATE BOT

✨ Ethiopian Dating Bot

🔥 Features:
• Smart Matching
• Pickup Lines
• Match Notifications
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
                "❌ Only 18+ allowed"
            )

            return AGE

        context.user_data["age"] = age

    except:

        await update.message.reply_text(
            "❌ Send valid age"
        )

        return AGE

    keyboard = ReplyKeyboardMarkup(
        [
            ["👨 Man", "👩 Woman"]
        ],
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

    gender = update.message.text

    if gender not in ["👨 Man", "👩 Woman"]:

        await update.message.reply_text(
            "❌ Choose valid gender"
        )

        return GENDER

    context.user_data["gender"] = gender

    keyboard = ReplyKeyboardMarkup(
        [
            ["👨 Man", "👩 Woman"]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        "❤️ Looking for:",
        reply_markup=keyboard
    )

    return LOOKING

# =====================================================
# LOOKING
# =====================================================

async def get_looking(update: Update, context: ContextTypes.DEFAULT_TYPE):

    looking = update.message.text

    if looking not in ["👨 Man", "👩 Woman"]:

        await update.message.reply_text(
            "❌ Choose valid option"
        )

        return LOOKING

    context.user_data["looking_for"] = looking

    keyboard = ReplyKeyboardMarkup(
        [
            ["📍 Addis Ababa", "📍 Adama"],
            ["📍 Hawassa", "📍 Dire Dawa"],
            ["📍 Bahir Dar", "📍 Mekelle"],
            ["📍 Gondar", "📍 Jimma"],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        "🌍 Choose your city:",
        reply_markup=keyboard
    )

    return CITY

# =====================================================
# CITY
# =====================================================

async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):

    city = update.message.text.replace("📍 ", "")

    context.user_data["city"] = city

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
            "❌ Please send a photo"
        )

        return PHOTO

    photo = update.message.photo[-1]

    photo_id = photo.file_id

    cursor.execute(
        """
        INSERT OR REPLACE INTO users
        (user_id, username, name, age, gender,
        looking_for, city, bio, photo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user.id,
            user.username,
            context.user_data["name"],
            context.user_data["age"],
            context.user_data["gender"],
            context.user_data["looking_for"],
            context.user_data["city"],
            context.user_data["bio"],
            photo_id,
        )
    )

    conn.commit()

    await update.message.reply_text(
        "✅ Profile Created Successfully ❤️",
        reply_markup=main_menu()
    )

    return ConversationHandler.END

# =====================================================
# SEND NEXT MATCH
# =====================================================

async def send_next_match(message, user_id, context):

    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )

    me = cursor.fetchone()

    if not me:
        return

    my_gender = me[4]
    looking_for = me[5]

    cursor.execute(
        """
        SELECT * FROM users
        WHERE user_id != ?
        AND gender = ?
        AND looking_for = ?

        AND user_id NOT IN (
            SELECT liked_user FROM likes
            WHERE user_id = ?
        )

        AND user_id NOT IN (
            SELECT disliked_user FROM dislikes
            WHERE user_id = ?
        )

        AND user_id NOT IN (
            SELECT blocked FROM blocks
            WHERE blocker = ?
        )

        ORDER BY RANDOM()
        LIMIT 1
        """,
        (
            user_id,
            looking_for,
            my_gender,
            user_id,
            user_id,
            user_id,
        )
    )

    target = cursor.fetchone()

    if not target:

        await message.reply_text(
            "😔 No more matches found"
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
                callback_data=f"dislike_{target_id}"
            )
        ],

        [
            InlineKeyboardButton(
                "💬 Pickup Line",
                callback_data=f"pickup_{target_id}"
            )
        ],

        [
            InlineKeyboardButton(
                "🚨 Report",
                callback_data=f"report_{target_id}"
            ),

            InlineKeyboardButton(
                "🚫 Block",
                callback_data=f"block_{target_id}"
            )
        ]
    ]

    caption = f"""
❤️ {target[2]}

🎂 Age: {target[3]}
🧑 Gender: {target[4]}
🌍 City: {target[6]}

📝 Bio:
{target[7]}
"""

    await message.reply_photo(
        photo=target[8],
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =====================================================
# FIND MATCH
# =====================================================

async def match(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    await send_next_match(
        update.message,
        user_id,
        context
    )

# =====================================================
# PROFILE
# =====================================================

async def my_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )

    profile = cursor.fetchone()

    if not profile:

        await update.message.reply_text(
            "❌ Create profile first"
        )

        return

    caption = f"""
👤 {profile[2]}

🎂 Age: {profile[3]}
🧑 Gender: {profile[4]}
❤️ Looking For: {profile[5]}
🌍 City: {profile[6]}

📝 Bio:
{profile[7]}
"""

    await update.message.reply_photo(
        photo=profile[8],
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
        "✅ Profile Updated",
        reply_markup=main_menu()
    )

    return ConversationHandler.END

# =====================================================
# BUTTONS
# =====================================================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data

    user_id = query.from_user.id

    action, target_id = data.split("_")

    target_id = int(target_id)

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

        cursor.execute(
            """
            SELECT * FROM likes
            WHERE user_id = ?
            AND liked_user = ?
            """,
            (target_id, user_id)
        )

        match_found = cursor.fetchone()

        if match_found:

            try:

                cursor.execute(
                    "INSERT OR IGNORE INTO matches VALUES (?, ?)",
                    (user_id, target_id)
                )

                conn.commit()

            except:
                pass

            cursor.execute(
                "SELECT name, username FROM users WHERE user_id = ?",
                (user_id,)
            )

            me = cursor.fetchone()

            cursor.execute(
                "SELECT name, username FROM users WHERE user_id = ?",
                (target_id,)
            )

            other = cursor.fetchone()

            my_username = (
                f"@{me[1]}"
                if me[1]
                else "No Username"
            )

            other_username = (
                f"@{other[1]}"
                if other[1]
                else "No Username"
            )

            await context.bot.send_message(
                chat_id=user_id,
                text=(
                    f"🎉 IT'S A MATCH ❤️\n\n"
                    f"👤 {other[0]}\n"
                    f"📩 {other_username}"
                )
            )

            await context.bot.send_message(
                chat_id=target_id,
                text=(
                    f"🎉 IT'S A MATCH ❤️\n\n"
                    f"👤 {me[0]}\n"
                    f"📩 {my_username}"
                )
            )

            await query.edit_message_caption(
                caption="🎉 IT'S A MATCH ❤️"
            )

        else:

            await context.bot.send_message(
                chat_id=target_id,
                text="❤️ Someone liked your profile"
            )

            await query.edit_message_caption(
                caption="❤️ Liked"
            )

        await send_next_match(
            query.message,
            user_id,
            context
        )

    # DISLIKE
    elif action == "dislike":

        try:

            cursor.execute(
                "INSERT INTO dislikes VALUES (?, ?)",
                (user_id, target_id)
            )

            conn.commit()

        except:
            pass

        await query.edit_message_caption(
            caption="❌ Skipped"
        )

        await send_next_match(
            query.message,
            user_id,
            context
        )

    # PICKUP
    elif action == "pickup":

        line = random.choice(pickup_lines)

        await context.bot.send_message(
            chat_id=target_id,
            text=f"💌 Pickup Line:\n\n{line}"
        )

        await query.answer(
            "💬 Pickup line sent"
        )

    # REPORT
    elif action == "report":

        cursor.execute(
            "INSERT INTO reports VALUES (?, ?, ?)",
            (user_id, target_id, "Bad behavior")
        )

        conn.commit()

        await query.answer(
            "🚨 User reported"
        )

    # BLOCK
    elif action == "block":

        cursor.execute(
            "INSERT INTO blocks VALUES (?, ?)",
            (user_id, target_id)
        )

        conn.commit()

        await query.answer(
            "🚫 User blocked"
        )

        await send_next_match(
            query.message,
            user_id,
            context
        )

# =====================================================
# MATCHES
# =====================================================

async def my_matches(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    cursor.execute(
        """
        SELECT * FROM matches
        WHERE user1 = ? OR user2 = ?
        """,
        (user_id, user_id)
    )

    matches = cursor.fetchall()

    if not matches:

        await update.message.reply_text(
            "😔 No matches yet"
        )

        return

    text = "🔥 YOUR MATCHES\n\n"

    for m in matches:

        other = m[1] if m[0] == user_id else m[0]

        cursor.execute(
            "SELECT name, username FROM users WHERE user_id = ?",
            (other,)
        )

        user = cursor.fetchone()

        if user:

            username = (
                f"@{user[1]}"
                if user[1]
                else "NoUsername"
            )

            text += f"❤️ {user[0]} - {username}\n"

    await update.message.reply_text(text)

# =====================================================
# ADMIN PANEL
# =====================================================

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMINS:

        await update.message.reply_text(
            "❌ Admin only"
        )

        return

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM matches")
    total_matches = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports")
    total_reports = cursor.fetchone()[0]

    text = f"""
👑 ACHADATE ADMIN PANEL

👥 Users: {total_users}
❤️ Matches: {total_matches}
🚨 Reports: {total_reports}
"""

    await update.message.reply_text(text)

# =====================================================
# MENU BUTTONS
# =====================================================

async def menu_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "❤️ Find Match":
        await match(update, context)

    elif text == "👤 My Profile":
        await my_profile(update, context)

    elif text == "🔥 My Matches":
        await my_matches(update, context)

    elif text == "⚙️ Settings":

        await update.message.reply_text(
            "⚙️ Settings Coming Soon"
        )

# =====================================================
# CANCEL
# =====================================================

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "❌ Cancelled"
    )

    return ConversationHandler.END

# =====================================================
# MAIN
# =====================================================

async def run_bot():

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
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_name
                )
            ],

            AGE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_age
                )
            ],

            GENDER: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_gender
                )
            ],

            LOOKING: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_looking
                )
            ],

            CITY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_city
                )
            ],

            BIO: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_bio
                )
            ],

            PHOTO: [
                MessageHandler(
                    filters.PHOTO,
                    get_photo
                )
            ],
        },

        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
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
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_new_name
                )
            ]
        },

        fallbacks=[
            CommandHandler("cancel", cancel)
        ]
    )

    # COMMANDS
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))

    # CONVERSATIONS
    app.add_handler(create_profile_handler)
    app.add_handler(edit_handler)

    # CALLBACKS
    app.add_handler(CallbackQueryHandler(buttons))

    # MENU
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            menu_buttons
        )
    )

    print("❤️ ACHADATE BOT RUNNING")

    # PYTHON 3.14 FIX
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:

        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("Bot stopped")

    finally:

        await app.updater.stop()
        await app.stop()
        await app.shutdown()

# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":

    asyncio.run(run_bot())