import os
import json
import random
import logging
from datetime import time
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# =========================================================
# SETTINGS
# =========================================================

TOKEN = os.environ.get("BOT_TOKEN")

OWNER_USERNAME = "hamthah"

DATA_FILE = "/data/love_bot_data.json"

TIMEZONE = ZoneInfo("Africa/Addis_Ababa")

DEFAULT_HOUR = 20
DEFAULT_MINUTE = 30


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# =========================================================
# MESSAGES
# =========================================================

MESSAGES = [

    "Just a reminder: I love you more than you probably realize ❤️",

    "You randomly crossed my mind again. Honestly, you live there rent-free 😏❤️",

    "I hope you're having a beautiful day, because someone is definitely thinking about you right now ❤️",

    "You're my favorite notification, my favorite thought, and probably my favorite distraction 😌❤️",

    "I don't need a reason to miss you. It just happens ❤️",

    "You're dangerously easy to fall for 😏❤️",

    "Just checking in to remind you that you're loved, wanted, and very much on my mind ❤️",

    "If thinking about you counted as exercise, I'd be in incredible shape by now 😂❤️",

    "You have no idea how often I smile because of you ❤️",

    "I hope you know how special you are to me ❤️",

    "Some people make your day better. You make mine better just by existing ❤️",

    "I still get that little feeling every time I think about you 😏❤️",

    "You're cute. You're beautiful. You're trouble. And somehow I want all three 😂❤️",

    "I miss your face. And maybe a few other things about you too 😏",

    "If I could teleport right now, you'd probably have to deal with me hugging you for a very long time ❤️",

    "You make ordinary days feel special ❤️",

    "I hope someone reminds you today that you're amazing. If nobody does, I'm volunteering ❤️",

    "You're one of those people I could never get tired of talking to ❤️",

    "I wish I could steal a little time with you right now 😏❤️",

    "You are honestly becoming a very serious problem for my concentration 😂❤️",

    "I don't know what you did to me, but whatever it is... keep doing it 😏",

    "You're the kind of distraction I would never complain about ❤️",

    "Just imagine me looking at you right now with that stupid smile you give me 😏❤️",

    "I hope your day is treating you gently. You deserve that ❤️",

    "You're my favorite person to annoy, flirt with, and love ❤️",

    "If I had one wish right now, I'd probably use it to be next to you ❤️",

    "You make my heart act like it has absolutely no self-control 😏",

    "I was going to send something normal, but then I remembered who I'm talking to 😏❤️",

    "You're cute enough to be dangerous and attractive enough to make it worse 😏",

    "I love the way you make me feel ❤️",

    "Every day I find another reason to love you ❤️",

    "You're not just someone I like. You're someone I genuinely care about ❤️",

    "I hope you smiled when you saw this. If not, I'm sending another one 😂❤️",

    "Missing you is becoming a daily habit ❤️",

    "I want to be the reason you randomly smile at your phone ❤️",

    "You're pretty much my favorite thought of the day ❤️",

    "I don't say it every minute, but I hope you know I love you every minute ❤️",

    "You have this annoying ability to make me miss you even when we just talked 😂❤️",

    "If I were beside you right now, I'd probably refuse to let you go 😏❤️",

    "You are absolutely worth every bit of affection I have ❤️",

    "I hope you know that somewhere out there, someone is thinking about you and smiling ❤️",

    "You make my heart feel ridiculously soft ❤️",

    "I want more memories with you. A lot more ❤️",

    "You're my favorite kind of trouble 😏❤️",

    "I would choose you again. And again. And again ❤️",

    "You're beautiful in ways that have nothing to do with looks ❤️",

    "I love hearing from you. Even a simple message from you can change my mood ❤️",

    "I wish I could give you a hug right now. A very long one ❤️",

    "You're the person I want to tell all my random thoughts to 😂❤️",

    "You make me want to be closer to you every day ❤️",

    "I hope you never forget how wanted and appreciated you are ❤️",

    "I have a confession: I think about you way more than I should 😏❤️",

    "You're slowly becoming my favorite part of every day ❤️",

    "If missing someone was illegal, I'd already be in serious trouble 😂❤️",

    "I like you. A lot. Possibly an unreasonable amount 😏❤️",

    "You have my attention, my affection, and probably way too much of my imagination 😏",

    "I hope today gives you at least one reason to smile. I'll happily be that reason ❤️",

    "You're the kind of person I'd happily get lost with ❤️",

    "I don't need perfect days. I just need more days with you ❤️",

    "You're my little daily reminder that life can be really sweet ❤️",

    "I love you. Just thought you should know that today ❤️",

]


# =========================================================
# DATA
# =========================================================

def default_data():
    return {
        "recipients": {},
        "connect_code": None,
        "hour": DEFAULT_HOUR,
        "minute": DEFAULT_MINUTE,
        "paused": False,
    }


def load_data():
    try:
        if not os.path.exists(DATA_FILE):
            return default_data()

        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Make sure missing keys don't break the bot
        defaults = default_data()

        for key, value in defaults.items():
            if key not in data:
                data[key] = value

        return data

    except Exception as e:
        logger.error("Could not load data: %s", e)
        return default_data()


def save_data(data):
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        logger.error("Could not save data: %s", e)


# =========================================================
# OWNER CHECK
# =========================================================

def is_owner(update: Update):

    user = update.effective_user

    if not user:
        return False

    username = user.username

    if not username:
        return False

    return username.lower() == OWNER_USERNAME.lower()


# =========================================================
# START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if not user:
        return

    logger.info(
        "START received from %s (%s)",
        user.username,
        user.id,
    )

    if is_owner(update):

        await update.message.reply_text(
            "❤️ Love Reminder Bot is online!\n\n"
            "You are the owner.\n\n"
            "Commands:\n"
            "/connect - Add a recipient\n"
            "/list - Show recipients\n"
            "/remove - Remove a recipient\n"
            "/test - Send a test message\n"
            "/pause - Pause daily messages\n"
            "/resume - Resume daily messages\n"
            "/time - Change sending time\n"
            "/status - Show bot status"
        )

    else:

        await update.message.reply_text(
            "❤️ Hey!\n\n"
            "This is a private Love Reminder Bot.\n\n"
            "If someone gave you a connection code, use:\n\n"
            "/join CODE\n\n"
            "Example:\n"
            "/join ABC123"
        )


# =========================================================
# CONNECT
# =========================================================

async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):
        await update.message.reply_text(
            "⛔ Only the owner can create a connection code."
        )
        return

    code = "".join(
        random.choices(
            "ABCDEFGHJKLMNPQRSTUVWXYZ23456789",
            k=6
        )
    )

    data = load_data()
    data["connect_code"] = code
    save_data(data)

    await update.message.reply_text(
        "🔗 CONNECTION CODE\n\n"
        f"Your code is:\n\n"
        f"👉 {code}\n\n"
        "Send this code to the person you want to add.\n\n"
        "They should open the bot and send:\n"
        f"/join {code}"
    )


# =========================================================
# JOIN
# =========================================================

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if not user:
        return

    if not context.args:

        await update.message.reply_text(
            "Please enter your connection code.\n\n"
            "Example:\n"
            "/join ABC123"
        )

        return

    entered_code = context.args[0].upper().strip()

    data = load_data()

    saved_code = data.get("connect_code")

    if not saved_code:

        await update.message.reply_text(
            "❌ There is no active connection code right now."
        )

        return

    if entered_code != saved_code:

        await update.message.reply_text(
            "❌ Invalid connection code."
        )

        return

    user_id = str(user.id)

    name = user.first_name or "Recipient"

    username = user.username or ""

    data["recipients"][user_id] = {
        "name": name,
        "username": username,
        "added": True,
    }

    # Code becomes invalid after use
    data["connect_code"] = None

    save_data(data)

    await update.message.reply_text(
        "❤️ You're connected!\n\n"
        "You'll now receive a daily love reminder. 💕\n\n"
        "No action is needed from you."
    )

    # Tell owner
    try:

        owner = await context.bot.get_chat(
            f"@{OWNER_USERNAME}"
        )

        await context.bot.send_message(
            chat_id=owner.id,
            text=(
                "❤️ NEW RECIPIENT ADDED\n\n"
                f"Name: {name}\n"
                f"Username: @{username if username else 'none'}\n"
                f"ID: {user.id}"
            ),
        )

    except Exception as e:

        logger.warning(
            "Could not notify owner: %s",
            e
        )


# =========================================================
# LIST
# =========================================================

async def list_recipients(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not is_owner(update):

        await update.message.reply_text(
            "⛔ Owner only."
        )

        return

    data = load_data()

    recipients = data.get("recipients", {})

    if not recipients:

        await update.message.reply_text(
            "📭 No recipients connected yet."
        )

        return

    lines = ["❤️ RECIPIENTS\n"]

    for i, (user_id, person) in enumerate(
        recipients.items(),
        start=1
    ):

        name = person.get("name", "Unknown")
        username = person.get("username")

        if username:
            display = f"@{username}"
        else:
            display = f"ID: {user_id}"

        lines.append(
            f"{i}. {name} — {display}"
        )

    await update.message.reply_text(
        "\n".join(lines)
    )


# =========================================================
# REMOVE
# =========================================================

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):

        await update.message.reply_text(
            "⛔ Owner only."
        )

        return

    if not context.args:

        await update.message.reply_text(
            "Use:\n"
            "/remove USER_ID"
        )

        return

    user_id = context.args[0]

    data = load_data()

    if user_id not in data["recipients"]:

        await update.message.reply_text(
            "❌ Recipient not found."
        )

        return

    removed = data["recipients"].pop(user_id)

    save_data(data)

    await update.message.reply_text(
        f"✅ Removed {removed.get('name', 'recipient')}."
    )


# =========================================================
# TEST
# =========================================================

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):

        await update.message.reply_text(
            "⛔ Owner only."
        )

        return

    data = load_data()

    recipients = data.get("recipients", {})

    if not recipients:

        await update.message.reply_text(
            "📭 No recipients connected."
        )

        return

    message = random.choice(MESSAGES)

    sent = 0

    for user_id in recipients:

        try:

            await context.bot.send_message(
                chat_id=int(user_id),
                text=message,
            )

            sent += 1

        except Exception as e:

            logger.error(
                "Could not send test to %s: %s",
                user_id,
                e
            )

    await update.message.reply_text(
        f"💌 Test message sent to {sent} recipient(s)."
    )


# =========================================================
# DAILY MESSAGE
# =========================================================

async def send_daily_messages(
    context: ContextTypes.DEFAULT_TYPE
):

    data = load_data()

    if data.get("paused"):

        logger.info("Daily messages are paused.")

        return

    recipients = data.get("recipients", {})

    if not recipients:

        logger.info("No recipients.")

        return

    message = random.choice(MESSAGES)

    for user_id in list(recipients.keys()):

        try:

            await context.bot.send_message(
                chat_id=int(user_id),
                text=message,
            )

            logger.info(
                "Daily message sent to %s",
                user_id
            )

        except Exception as e:

            logger.error(
                "Failed sending to %s: %s",
                user_id,
                e
            )


# =========================================================
# PAUSE
# =========================================================

async def pause(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):

        await update.message.reply_text(
            "⛔ Owner only."
        )

        return

    data = load_data()

    data["paused"] = True

    save_data(data)

    await update.message.reply_text(
        "⏸ Daily messages paused."
    )


# =========================================================
# RESUME
# =========================================================

async def resume(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):

        await update.message.reply_text(
            "⛔ Owner only."
        )

        return

    data = load_data()

    data["paused"] = False

    save_data(data)

    await update.message.reply_text(
        "▶️ Daily messages resumed."
    )


# =========================================================
# TIME
# =========================================================

async def set_time(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):

        await update.message.reply_text(
            "⛔ Owner only."
        )

        return

    if not context.args:

        data = load_data()

        await update.message.reply_text(
            "⏰ Current time: "
            f"{data['hour']:02d}:{data['minute']:02d} Ethiopia time.\n\n"
            "To change it:\n"
            "/time 21:00"
        )

        return

    value = context.args[0]

    try:

        hour, minute = map(
            int,
            value.split(":")
        )

        if hour < 0 or hour > 23:
            raise ValueError

        if minute < 0 or minute > 59:
            raise ValueError

    except Exception:

        await update.message.reply_text(
            "❌ Invalid time.\n\n"
            "Use:\n"
            "/time 21:00"
        )

        return

    data = load_data()

    data["hour"] = hour
    data["minute"] = minute

    save_data(data)

    # Rebuild scheduled job
    schedule_daily_job(context.application)

    await update.message.reply_text(
        f"⏰ Daily message time changed to "
        f"{hour:02d}:{minute:02d} Ethiopia time."
    )


# =========================================================
# STATUS
# =========================================================

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):

        await update.message.reply_text(
            "⛔ Owner only."
        )

        return

    data = load_data()

    recipients = data.get("recipients", {})

    paused = data.get("paused", False)

    hour = data.get("hour", DEFAULT_HOUR)
    minute = data.get("minute", DEFAULT_MINUTE)

    await update.message.reply_text(
        "❤️ LOVE BOT STATUS\n\n"
        f"Recipients: {len(recipients)}\n"
        f"Daily time: {hour:02d}:{minute:02d}\n"
        f"Timezone: Ethiopia\n"
        f"Status: {'⏸ Paused' if paused else '▶️ Active'}"
    )


# =========================================================
# SCHEDULE
# =========================================================

def schedule_daily_job(application):

    job_queue = application.job_queue

    if job_queue is None:
        logger.error(
            "Job queue is unavailable."
        )
        return

    # Remove old daily job
    for job in job_queue.get_jobs_by_name(
        "love_daily_message"
    ):
        job.schedule_removal()

    data = load_data()

    hour = data.get(
        "hour",
        DEFAULT_HOUR
    )

    minute = data.get(
        "minute",
        DEFAULT_MINUTE
    )

    job_queue.run_daily(
        send_daily_messages,
        time=time(
            hour=hour,
            minute=minute,
            tzinfo=TIMEZONE,
        ),
        name="love_daily_message",
    )

    logger.info(
        "Daily message scheduled for %02d:%02d Ethiopia time",
        hour,
        minute,
    )


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.error(
        "Bot error: %s",
        context.error,
        exc_info=True,
    )


# =========================================================
# MAIN
# =========================================================

def main():

    if not TOKEN:

        raise RuntimeError(
            "BOT_TOKEN environment variable is missing."
        )

    logger.info("Starting Love Reminder Bot...")

    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    # Commands
    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("connect", connect)
    )

    application.add_handler(
        CommandHandler("join", join)
    )

    application.add_handler(
        CommandHandler("list", list_recipients)
    )

    application.add_handler(
        CommandHandler("remove", remove)
    )

    application.add_handler(
        CommandHandler("test", test)
    )

    application.add_handler(
        CommandHandler("pause", pause)
    )

    application.add_handler(
        CommandHandler("resume", resume)
    )

    application.add_handler(
        CommandHandler("time", set_time)
    )

    application.add_handler(
        CommandHandler("status", status)
    )

    application.add_error_handler(
        error_handler
    )

    # Schedule daily messages
    schedule_daily_job(application)

    logger.info("Bot is running.")

    application.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
