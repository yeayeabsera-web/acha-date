# =====================================================
# 🍋 LEMONADE DATING BOT - FULL VERSION
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
ADMIN_ID = 8460165874

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# =====================================================
# DATABASE
# =====================================================

conn = sqlite3.connect(
    "lemonade.db",
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
    photo TEXT,
    online INTEGER DEFAULT 1
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
    user2 INTEGER
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
) = range(7)

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

    "I think Spotify is missing you from the hottest singles list 🎵",

    "You’re the reason this app feels worth downloading ❤️",

    "You look expensive in the best way 😌",

    "You just turned my bad day into a good one 💕",

]

# =====================================================
# MAIN MENU
# =====================================================

def main_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "❤️ Find Match",
                callback_data="find_match"
            )
        ],

        [
            InlineKeyboardButton(
                "👤 My Profile",
                callback_data="my_profile"
            ),

            InlineKeyboardButton(
                "✏️ Edit Profile",
                callback_data="edit_profile"
            )
        ],

        [
            InlineKeyboardButton(
                "🔥 My Matches",
                callback_data="my_matches"
            )
        ],

        [
            InlineKeyboardButton(
                "⚙️ Settings",
                callback_data="settings"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)

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

    # EXISTING USER
    if profile:

        await update.message.reply_text(
            f"🍋 Welcome Back {profile[2]} ❤️",
            reply_markup=main_menu()
        )

        return

    # NEW USER
    keyboard = [
        [
            InlineKeyboardButton(
                "❤️ Create Profile",
                callback_data="create_profile"
            )
        ]
    ]

    text = """
🍋 LEMONADE DATING BOT ❤️

✨ Premium Modern Dating Bot

🔥 Features:
• Smart Matching
• Pickup Lines
• Match Notifications
• Tinder Style Matching
• Ethiopian Dating
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

    context.user_data["gender"] = update.message.text

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
# LOOKING FOR
# =====================================================

async def get_looking(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["looking_for"] = update.message.text

    keyboard = ReplyKeyboardMarkup(
        [
            ["Addis Ababa", "Adama"],
            ["Hawassa", "Dire Dawa"],
            ["Bahir Dar", "Mekelle"]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        "🌍 Select your city:",
        reply_markup=keyboard
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
            "❌ Please send photo"
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
# FIND MATCH
# =====================================================

async def match(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.callback_query:

        query = update.callback_query
        user_id = query.from_user.id

    else:

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

        ORDER BY RANDOM()
        LIMIT 1
        """,
        (
            user_id,
            looking_for,
            my_gender,
            user_id,
            user_id,
        )
    )

    target = cursor.fetchone()

    if not target:

        text = "😔 No matches found"

        if update.callback_query:

            await update.callback_query.message.reply_text(text)

        else:

            await update.message.reply_text(text)

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

🟢 Online Now
"""

    if update.callback_query:

        await update.callback_query.message.reply_photo(
            photo=target[8],
            caption=caption,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    else:

        await update.message.reply_photo(
            photo=target[8],
            caption=caption,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# =====================================================
# BUTTONS
# =====================================================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data

    user_id = query.from_user.id

    # FIND MATCH
    if data == "find_match":

        await match(update, context)
        return

    # MY PROFILE
    if data == "my_profile":

        cursor.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )

        profile = cursor.fetchone()

        caption = f"""
👤 {profile[2]}

🎂 Age: {profile[3]}
🧑 Gender: {profile[4]}
❤️ Looking For: {profile[5]}
🌍 City: {profile[6]}

📝 Bio:
{profile[7]}
"""

        await query.message.reply_photo(
            photo=profile[8],
            caption=caption
        )

        return

    # MY MATCHES
    if data == "my_matches":

        cursor.execute(
            """
            SELECT * FROM matches
            WHERE user1 = ? OR user2 = ?
            """,
            (user_id, user_id)
        )

        all_matches = cursor.fetchall()

        if not all_matches:

            await query.message.reply_text(
                "😔 No matches yet"
            )

            return

        text = "🔥 Your Matches:\n\n"

        for m in all_matches:

            other = m[1] if m[0] == user_id else m[0]

            cursor.execute(
                "SELECT name, username FROM users WHERE user_id = ?",
                (other,)
            )

            user = cursor.fetchone()

            text += (
                f"❤️ {user[0]} - "
                f"@{user[1] if user[1] else 'NoUsername'}\n"
            )

        await query.message.reply_text(text)

        return

    # SETTINGS
    if data == "settings":

        await query.message.reply_text(
            "⚙️ Settings Coming Soon"
        )

        return

    # EDIT PROFILE
    if data == "edit_profile":

        await query.message.reply_text(
            "✏️ Send your new name"
        )

        return NAME

    # ACTIONS
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

        await context.bot.send_message(
            chat_id=target_id,
            text="❤️ Someone liked your profile"
        )

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

            cursor.execute(
                "INSERT INTO matches VALUES (?, ?)",
                (user_id, target_id)
            )

            conn.commit()

            cursor.execute(
                "SELECT username, name FROM users WHERE user_id = ?",
                (user_id,)
            )

            me = cursor.fetchone()

            cursor.execute(
                "SELECT username, name FROM users WHERE user_id = ?",
                (target_id,)
            )

            target = cursor.fetchone()

            await context.bot.send_message(
                chat_id=user_id,
                text=(
                    f"🎉 IT'S A MATCH ❤️\n\n"
                    f"👤 {target[1]}\n"
                    f"📩 @{target[0]}"
                )
            )

            await context.bot.send_message(
                chat_id=target_id,
                text=(
                    f"🎉 IT'S A MATCH ❤️\n\n"
                    f"👤 {me[1]}\n"
                    f"📩 @{me[0]}"
                )
            )

            await query.edit_message_caption(
                caption="🎉 IT'S A MATCH ❤️"
            )

        else:

            await query.edit_message_caption(
                caption="❤️ Liked"
            )

        await match(update, context)

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

        await match(update, context)

    # PICKUP LINE
    elif action == "pickup":

        line = random.choice(pickup_lines)

        await context.bot.send_message(
            chat_id=target_id,
            text=(
                f"💌 Someone sent you a pickup line:\n\n"
                f"{line}"
            )
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

# =====================================================
# ADMIN PANEL
# =====================================================

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id != ADMIN_ID:

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
👑 LEMONADE ADMIN PANEL

👥 Total Users: {total_users}
❤️ Total Matches: {total_matches}
🚨 Reports: {total_reports}

⚡ Commands:
/stats
/users
/reports
/ban USER_ID
/broadcast MESSAGE
"""

    await update.message.reply_text(text)

# =====================================================
# STATS
# =====================================================

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    cursor.execute("SELECT COUNT(*) FROM users")
    users_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM likes")
    likes_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM matches")
    matches_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports")
    reports_count = cursor.fetchone()[0]

    text = f"""
📊 BOT STATS

👥 Users: {users_count}
❤️ Likes: {likes_count}
🎉 Matches: {matches_count}
🚨 Reports: {reports_count}
"""

    await update.message.reply_text(text)

# =====================================================
# USERS
# =====================================================

async def all_users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    cursor.execute(
        "SELECT name, username FROM users LIMIT 50"
    )

    users = cursor.fetchall()

    if not users:

        await update.message.reply_text(
            "No users"
        )

        return

    text = "👥 USERS LIST\n\n"

    for user in users:

        text += (
            f"👤 {user[0]} - "
            f"@{user[1] if user[1] else 'NoUsername'}\n"
        )

    await update.message.reply_text(text)

# =====================================================
# REPORTS
# =====================================================

async def reports(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    cursor.execute(
        "SELECT * FROM reports LIMIT 20"
    )

    all_reports = cursor.fetchall()

    if not all_reports:

        await update.message.reply_text(
            "✅ No reports"
        )

        return

    text = "🚨 USER REPORTS\n\n"

    for report in all_reports:

        text += (
            f"👤 Reporter: {report[0]}\n"
            f"🚫 Target: {report[1]}\n"
            f"📝 Reason: {report[2]}\n\n"
        )

    await update.message.reply_text(text)

# =====================================================
# BAN USER
# =====================================================

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    try:

        target_id = int(context.args[0])

    except:

        await update.message.reply_text(
            "Usage: /ban USER_ID"
        )

        return

    cursor.execute(
        "DELETE FROM users WHERE user_id = ?",
        (target_id,)
    )

    conn.commit()

    await update.message.reply_text(
        f"🚫 User {target_id} banned"
    )

# =====================================================
# BROADCAST
# =====================================================

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:

        await update.message.reply_text(
            "Usage: /broadcast message"
        )

        return

    message = " ".join(context.args)

    cursor.execute(
        "SELECT user_id FROM users"
    )

    users = cursor.fetchall()

    sent = 0

    for user in users:

        try:

            await context.bot.send_message(
                chat_id=user[0],
                text=f"📢 ADMIN MESSAGE\n\n{message}"
            )

            sent += 1

        except:
            pass

    await update.message.reply_text(
        f"✅ Broadcast sent to {sent} users"
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

def main():

    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(

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

    # USER COMMANDS
    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("match", match)
    )

    # ADMIN COMMANDS
    app.add_handler(
        CommandHandler("admin", admin_panel)
    )

    app.add_handler(
        CommandHandler("stats", stats)
    )

    app.add_handler(
        CommandHandler("users", all_users)
    )

    app.add_handler(
        CommandHandler("reports", reports)
    )

    app.add_handler(
        CommandHandler("ban", ban)
    )

    app.add_handler(
        CommandHandler("broadcast", broadcast)
    )

    # HANDLERS
    app.add_handler(conv_handler)

    app.add_handler(
        CallbackQueryHandler(buttons)
    )

    print("🍋 LEMONADE BOT RUNNING")

    app.run_polling()

# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":
    main()