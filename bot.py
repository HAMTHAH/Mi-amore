import os
import json
import random
import secrets
import logging
from datetime import time
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# ============================================================
# SETTINGS
# ============================================================

TOKEN = os.environ["BOT_TOKEN"]

OWNER_USERNAME = "hamthah"

DATA_FILE = "love_bot_data.json"

TIMEZONE = ZoneInfo("Africa/Addis_Ababa")

DEFAULT_HOUR = 20
DEFAULT_MINUTE = 30

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ============================================================
# MESSAGES
# ============================================================

MESSAGES = [

    # SWEET ❤️

    "Just a little reminder: I love you more than you probably realize. ❤️",

    "I hope you know how special you are to me. I really do love you. 🥰",

    "Out of everyone in this world, somehow I got lucky enough to have you. ❤️",

    "You make ordinary days feel special just by being part of them.",

    "I don't need a special occasion to tell you that I love you. I just wanted you to know. ❤️",

    "You're one of my favorite thoughts every single day.",

    "If you could see yourself through my eyes, you'd understand how beautiful you are to me. ❤️",

    "I hope something makes you smile today. And if nothing does, remember that I'm here. 😘",

    "You're one of the best things in my life. ❤️",

    "My favorite notification will always be your name appearing on my phone. ❤️",

    "You make my days better without even trying.",

    "I just wanted to remind you that someone out here is thinking about you. ❤️",

    "You have a permanent place in my heart. No rent required. 😂❤️",

    "I love having you in my life more than I can put into words.",

    "You're one of the best things that has happened to me. ❤️",

    # ROMANTIC 💕

    "If I had to choose you all over again, I'd still choose you.",

    "I don't know what I did to deserve you, but I'm very happy I did it. 😘",

    "You somehow make my heart feel peaceful and crazy at the same time.",

    "I want more ordinary days with you. More laughs, conversations and memories. ❤️",

    "Sometimes I stop what I'm doing because I remembered you. That's how often you cross my mind.",

    "I love the way you make me feel like I can completely be myself.",

    "You're my favorite person to miss and my favorite person to come back to.",

    "No matter how busy my day gets, there is always a little part of it reserved for thinking about you. ❤️",

    "You somehow became my favorite part of everyday life.",

    "I love you today, and I'll probably find another reason to love you tomorrow. ❤️",

    "I don't just love you for how beautiful you are. I love the way you make me feel.",

    "If I could freeze one feeling, it would be the feeling of being close to you. ❤️",

    "I hope we get to make a ridiculous amount of memories together.",

    "You have a way of making my whole day better just by talking to me.",

    "You're someone I want beside me for all the little moments in life. ❤️",

    # FLIRTY 😏

    "Just so you know, you're looking dangerously good in my imagination today. 😏",

    "I was trying to concentrate today, then you crossed my mind. That was the end of that. 😂❤️",

    "You really should stop being so attractive. I'm trying to behave. 😏",

    "I don't know what's more dangerous: your smile or what it does to me. 😘",

    "If you were here right now, I'd probably forget whatever I was supposed to be doing. 😏",

    "You're becoming a serious distraction, and honestly, I don't want the problem fixed. ❤️",

    "I hope you're ready for me to flirt with you again today. 😏",

    "You have absolutely no business looking that good and expecting me to act normal.",

    "I miss your face. And maybe a few other things about you too. 😏❤️",

    "Today's reminder: you're ridiculously attractive. 😘",

    "I swear you get prettier every time I see you.",

    "You have a talent for making me smile at my phone like an idiot. 😏",

    "I should probably stop thinking about you so much. But where's the fun in that? 😂❤️",

    "If flirting with you were a job, I'd be employee of the month every month. 😂❤️",

    "You're dangerously close to becoming my favorite distraction. 😏",

    # SUGGESTIVE 🔥

    "I have a few thoughts about you that definitely shouldn't be sent during a family dinner. 😏🔥",

    "You're making it very difficult for me to keep my thoughts innocent today.",

    "If you were next to me right now, I don't think we'd spend much time talking. 😏",

    "I miss being close to you in ways that are probably better demonstrated than explained. ❤️",

    "There are certain things I want to whisper in your ear instead of typing here. 😏",

    "You're the reason some of my thoughts need a warning label. 😂🔥",

    "I can't decide whether I want to cuddle you or completely ruin your ability to concentrate. 😏",

    "Just thinking about being alone with you is enough to put a smile on my face. ❤️‍🔥",

    "You have a talent for making my imagination work overtime.",

    "You make innocent thoughts become suspiciously less innocent. 😏",

    "Some thoughts about you are definitely better kept between us. 🔥",

    "Let's just say... you're giving my imagination a lot to work with today. 😏❤️",

    "I miss your touch more than I probably should admit. ❤️‍🔥",

    "You have no idea how much trouble you cause inside my head. 😏",

    "I have a feeling we'd have a lot of fun if we were alone together. 😏🔥",

    # GOOD MORNING ☀️

    "Good morning, beautiful. I hope today treats you as kindly as you deserve. ❤️",

    "Wake up knowing that someone out here is already thinking about you. 😘",

    "Good morning, my favorite person. Go make today yours. ❤️",

    "I hope your morning starts with a smile. Consider this your first reason. 😘",

    "Morning reminder: you're loved, you're beautiful, and you're stuck with me. 😂❤️",

    "Good morning, gorgeous. I hope your day is as beautiful as you are. ❤️",

    "First thought of the day? You. Obviously. 😘",

    "Good morning, love. Just sending you a little reminder that you're special to me. ❤️",

    "I hope you woke up smiling because somebody definitely woke up thinking about you. 😏❤️",

    "Good morning, beautiful. Now go be amazing like you always are. ❤️",

    # PLAYFUL 😂

    "Daily reminder: yes, I still love you. Unfortunately for you, you're stuck with me. 😂❤️",

    "I considered sending you something normal today. Then I remembered who I was talking to. 😏",

    "Breaking news: I still have a crush on you. More details tomorrow. 😂❤️",

    "I love you. That's the message. There will be no further questions at this time. 😂",

    "You are officially today's favorite person. Don't let it go to your head. 😌❤️",

    "I was going to send you a boring message, but you're too cute for boring messages. 😏",

    "Reminder: you're beautiful. Also, yes, I'm still obsessed with you. 😂❤️",

    "I hope you're having a good day. If not, I'm officially volunteering to make it better. 😘",

    "You're lucky I like you this much. Actually, I'm the lucky one. ❤️😂",

    "I don't know how you managed to become this important to me, but here we are. ❤️",
]

# ============================================================
# DATA
# ============================================================

def default_data():
    return {
        "recipients": {},
        "connect_code": None,
        "hour": DEFAULT_HOUR,
        "minute": DEFAULT_MINUTE,
        "paused": False,
    }


def load_data():
    if not os.path.exists(DATA_FILE):
        return default_data()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            saved = json.load(file)

        data = default_data()
        data.update(saved)

        return data

    except Exception:
        return default_data()


def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


data = load_data()

# ============================================================
# OWNER CHECK
# ============================================================

def is_owner(update: Update):

    user = update.effective_user

    if not user:
        return False

    if not user.username:
        return False

    return user.username.lower() == OWNER_USERNAME.lower()


# ============================================================
# OWNER PANEL
# ============================================================

async def owner(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):
        await update.message.reply_text(
            "❌ Owner only."
        )
        return

    await update.message.reply_text(
        "❤️ LOVE BOT CONTROL\n\n"

        "/connect - Create recipient connection code\n"
        "/list - List all recipients\n"
        "/remove ID - Remove a recipient\n\n"

        "/test - Send a test message to everyone\n"
        "/time 20:30 - Set daily sending time\n"
        "/pause - Pause daily messages\n"
        "/resume - Resume daily messages\n"
        "/status - Show bot status\n"
    )


# ============================================================
# CREATE CONNECTION CODE
# ============================================================

async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):
        await update.message.reply_text(
            "❌ Owner only."
        )
        return

    code = secrets.token_hex(3).upper()

    data["connect_code"] = code

    save_data()

    await update.message.reply_text(
        "💕 NEW RECIPIENT CODE\n\n"

        f"🔐 {code}\n\n"

        "Send this code to the person you want to add.\n\n"

        "They must open your bot and send:\n\n"

        f"/join {code}"
    )


# ============================================================
# RECIPIENT JOINS
# ============================================================

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:

        await update.message.reply_text(
            "Please enter your connection code.\n\n"
            "Example:\n"
            "/join ABC123"
        )

        return

    code = context.args[0].upper()

    if not data.get("connect_code"):

        await update.message.reply_text(
            "❌ No active connection code.\n"
            "Ask the bot owner for a new one."
        )

        return

    if code != data["connect_code"]:

        await update.message.reply_text(
            "❌ Invalid connection code."
        )

        return

    user = update.effective_user

    chat_id = update.effective_chat.id

    username = user.username

    name = user.first_name or "Unknown"

    # Save recipient
    data["recipients"][str(chat_id)] = {
        "name": name,
        "username": username,
        "last_message": None,
    }

    # Code becomes invalid after use
    data["connect_code"] = None

    save_data()

    await update.message.reply_text(
        "❤️ You're connected!\n\n"
        "You'll now receive a little reminder "
        "every day. 💕"
    )


# ============================================================
# LIST RECIPIENTS
# ============================================================

async def list_recipients(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not is_owner(update):

        await update.message.reply_text(
            "❌ Owner only."
        )

        return

    recipients = data["recipients"]

    if not recipients:

        await update.message.reply_text(
            "📋 No recipients connected yet.\n\n"
            "Use /connect to create a connection code."
        )

        return

    text = "👥 RECIPIENTS\n\n"

    number = 1

    for chat_id, person in recipients.items():

        name = person.get("name", "Unknown")
        username = person.get("username")

        if username:
            display = f"@{username}"
        else:
            display = name

        text += (
            f"{number}. ❤️ {display}\n"
            f"   ID: `{chat_id}`\n\n"
        )

        number += 1

    await update.message.reply_text(
        text,
        parse_mode="Markdown"
    )


# ============================================================
# REMOVE RECIPIENT
# ============================================================

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):

        await update.message.reply_text(
            "❌ Owner only."
        )

        return

    if not context.args:

        await update.message.reply_text(
            "Use:\n"
            "/remove CHAT_ID\n\n"
            "Get the ID from /list."
        )

        return

    chat_id = context.args[0]

    if chat_id not in data["recipients"]:

        await update.message.reply_text(
            "❌ Recipient not found."
        )

        return

    person = data["recipients"].pop(chat_id)

    save_data()

    await update.message.reply_text(
        f"✅ Removed {person.get('name', 'recipient')}."
    )


# ============================================================
# TEST
# ============================================================

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):

        await update.message.reply_text(
            "❌ Owner only."
        )

        return

    recipients = data["recipients"]

    if not recipients:

        await update.message.reply_text(
            "❌ No recipients connected."
        )

        return

    sent = 0

    for chat_id, person in recipients.items():

        message = random.choice(MESSAGES)

        try:

            await context.bot.send_message(
                chat_id=int(chat_id),
                text=message,
            )

            person["last_message"] = message

            sent += 1

        except Exception as e:

            logging.error(
                f"Could not message {chat_id}: {e}"
            )

    save_data()

    await update.message.reply_text(
        f"✅ Test message sent to {sent} recipient(s). ❤️"
    )


# ============================================================
# PAUSE
# ============================================================

async def pause(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):

        await update.message.reply_text(
            "❌ Owner only."
        )

        return

    data["paused"] = True

    save_data()

    await update.message.reply_text(
        "⏸️ Daily messages paused."
    )


# ============================================================
# RESUME
# ============================================================

async def resume(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):

        await update.message.reply_text(
            "❌ Owner only."
        )

        return

    data["paused"] = False

    save_data()

    await update.message.reply_text(
        "▶️ Daily messages resumed. ❤️"
    )


# ============================================================
# CHANGE TIME
# ============================================================

async def set_time(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):

        await update.message.reply_text(
            "❌ Owner only."
        )

        return

    if not context.args:

        await update.message.reply_text(
            "Use:\n"
            "/time 20:30\n\n"
            "Time zone: Ethiopia 🇪🇹"
        )

        return

    try:

        hour, minute = map(
            int,
            context.args[0].split(":")
        )

        if not (
            0 <= hour <= 23
            and 0 <= minute <= 59
        ):
            raise ValueError

        data["hour"] = hour
        data["minute"] = minute

        save_data()

        # Remove old scheduled job
        jobs = context.job_queue.get_jobs_by_name(
            "daily_love"
        )

        for job in jobs:
            job.schedule_removal()

        # Create new schedule
        context.job_queue.run_daily(
            send_daily_messages,
            time=time(
                hour=hour,
                minute=minute,
                tzinfo=TIMEZONE,
            ),
            name="daily_love",
        )

        await update.message.reply_text(
            f"⏰ Daily time changed to "
            f"{hour:02d}:{minute:02d} Ethiopia time."
        )

    except ValueError:

        await update.message.reply_text(
            "❌ Invalid time.\n\n"
            "Example:\n"
            "/time 20:30"
        )


# ============================================================
# STATUS
# ============================================================

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):

        await update.message.reply_text(
            "❌ Owner only."
        )

        return

    count = len(data["recipients"])

    state = (
        "⏸️ PAUSED"
        if data["paused"]
        else "▶️ ACTIVE"
    )

    await update.message.reply_text(
        "❤️ LOVE BOT STATUS\n\n"

        f"Status: {state}\n"
        f"Recipients: {count}\n"
        f"Daily time: "
        f"{data['hour']:02d}:{data['minute']:02d} "
        f"Ethiopia time\n"
        f"Messages available: {len(MESSAGES)}"
    )


# ============================================================
# DAILY MESSAGE
# ============================================================

async def send_daily_messages(
    context: ContextTypes.DEFAULT_TYPE
):

    if data["paused"]:
        logging.info("Daily messages are paused.")
        return

    recipients = data["recipients"]

    if not recipients:

        logging.info(
            "No recipients connected."
        )

        return

    for chat_id, person in list(recipients.items()):

        message = random.choice(MESSAGES)

        # Don't immediately repeat the same message
        if len(MESSAGES) > 1:

            while (
                message == person.get("last_message")
            ):
                message = random.choice(MESSAGES)

        try:

            await context.bot.send_message(
                chat_id=int(chat_id),
                text=message,
            )

            person["last_message"] = message

            logging.info(
                f"Message sent to {chat_id}"
            )

        except Exception as e:

            logging.error(
                f"Failed to send to {chat_id}: {e}"
            )

    save_data()


# ============================================================
# SCHEDULE
# ============================================================

def setup_daily_job(application):

    application.job_queue.run_daily(
        send_daily_messages,
        time=time(
            hour=data["hour"],
            minute=data["minute"],
            tzinfo=TIMEZONE,
        ),
        name="daily_love",
    )


# ============================================================
# MAIN
# ============================================================

def main():

    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    # Owner commands
    application.add_handler(
        CommandHandler("owner", owner)
    )

    application.add_handler(
        CommandHandler("connect", connect)
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

    # Recipient command
    application.add_handler(
        CommandHandler("join", join)
    )

    setup_daily_job(application)

    print("❤️ Multi-Recipient Love Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
