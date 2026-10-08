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

# ============================================================
# SETTINGS
# ============================================================

TOKEN = os.environ["BOT_TOKEN"]

DATA_FILE = "love_bot_data.json"

# Ethiopia time
TIMEZONE = ZoneInfo("Africa/Addis_Ababa")

# Default sending time: 9:00 PM
DEFAULT_HOUR = 21
DEFAULT_MINUTE = 0

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ============================================================
# LOVE MESSAGES
# No good-night messages
# ============================================================

MESSAGES = [

    # ========================================================
    # SWEET ❤️
    # ========================================================

    "Just a little reminder: I love you more than you probably realize. ❤️",

    "I hope you know how special you are to me. I don't say it enough, but I really do love you. 🥰",

    "Out of everyone in this world, somehow I got lucky enough to have you. ❤️",

    "You make ordinary days feel special just by being part of them.",

    "I don't need a special occasion to tell you that I love you. I just wanted you to know. ❤️",

    "You're one of my favorite thoughts every single day.",

    "If I could give you one thing today, it would be the ability to see yourself through my eyes. You'd understand how beautiful you are. ❤️",

    "I hope something makes you smile today. And if nothing does, remember that I'm here. 😘",

    "You're not just someone I love. You're someone I genuinely enjoy having in my life.",

    "My favorite notification will always be your name appearing on my phone. ❤️",

    "You make my days better without even trying.",

    "I just wanted to remind you that someone out here is thinking about you. ❤️",

    "You have a permanent place in my heart. No rent required. 😂❤️",

    "I love having you in my life more than I can put into words.",

    "You're one of the best things that has happened to me. ❤️",

    # ========================================================
    # ROMANTIC 💕
    # ========================================================

    "I still get that little feeling in my chest when I think about you. ❤️",

    "If I had to choose you all over again, I'd still choose you.",

    "I don't know what I did to deserve you, but I'm very happy I did it. 😘",

    "You somehow make my heart feel both peaceful and completely crazy at the same time.",

    "I want more ordinary days with you. More random conversations, more laughs, more memories. ❤️",

    "You have become one of those people I can't imagine my life without.",

    "Sometimes I randomly stop what I'm doing because I remembered you. That's how often you cross my mind. ❤️",

    "I love the way you make me feel like I can be completely myself.",

    "You're my favorite person to miss and my favorite person to come back to.",

    "No matter how busy my day gets, there is always a little part of it reserved for thinking about you. ❤️",

    "I don't just love you for how beautiful you are. I love the way you make me feel.",

    "If I could freeze one feeling, it would be the feeling of being close to you. ❤️",

    "I hope we get to make a ridiculous amount of memories together.",

    "You somehow became my favorite part of my everyday life.",

    "I love you today, and I'll probably find another reason to love you tomorrow. ❤️",

    # ========================================================
    # FLIRTY 😏
    # ========================================================

    "Just so you know, you're looking dangerously good in my imagination today. 😏",

    "I was trying to concentrate today, then you crossed my mind. That was the end of that. 😂❤️",

    "You really should stop being so attractive. I'm trying to behave. 😏",

    "I don't know what's more dangerous: your smile or what it does to me. 😘",

    "If you were here right now, I’m pretty sure I'd forget whatever I was supposed to be doing. 😏",

    "You're becoming a serious distraction, and honestly, I don't want the problem fixed. ❤️",

    "I hope you're ready for me to flirt with you again today. 😏",

    "You have absolutely no business looking that good and expecting me to act normal.",

    "I miss your face. And maybe a few other things about you too. 😏❤️",

    "Today's reminder: you're ridiculously attractive. That is all. 😘",

    "I swear you get prettier every time I see you.",

    "You're dangerously close to becoming my favorite distraction. 😏",

    "I should probably stop thinking about you so much. But where's the fun in that? 😂❤️",

    "You have a talent for making me smile at my phone like an idiot. 😏",

    "If flirting with you were a job, I'd be employee of the month every month. 😂❤️",

    # ========================================================
    # SPICY / SUGGESTIVE 🔥
    # ========================================================

    "I have a few thoughts about you that definitely shouldn't be sent during a family dinner. 😏🔥",

    "You're making it very difficult for me to keep my thoughts innocent today.",

    "If you were next to me right now, I don't think we'd spend much time talking. 😏",

    "I miss being close to you in ways that are probably better demonstrated than explained. ❤️",

    "There are certain things I want to whisper in your ear instead of typing here. 😏",

    "You're the reason some of my thoughts need a 'not safe for work' warning. 😂🔥",

    "I can't decide whether I want to cuddle you or completely ruin your ability to concentrate. 😏",

    "Just thinking about being alone with you is enough to put a smile on my face. ❤️‍🔥",

    "You have a talent for making my imagination work overtime.",

    "I have a feeling that if we were alone together right now, we'd find plenty of ways to entertain ourselves. 😏🔥",

    "You make innocent thoughts become suspiciously less innocent. 😏",

    "I miss your touch more than I probably should admit. ❤️‍🔥",

    "You have no idea how much trouble you cause inside my head. 😏",

    "Some thoughts about you are definitely better kept between us. 🔥",

    "Let's just say... you're giving my imagination a lot to work with today. 😏❤️",

    # ========================================================
    # GOOD MORNING ☀️
    # ========================================================

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

    # ========================================================
    # PLAYFUL 😂
    # ========================================================

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

def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "girl_chat_id": None,
            "hour": DEFAULT_HOUR,
            "minute": DEFAULT_MINUTE,
            "paused": False,
            "last_message": None,
        }

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return {
            "girl_chat_id": None,
            "hour": DEFAULT_HOUR,
            "minute": DEFAULT_MINUTE,
            "paused": False,
            "last_message": None,
        }


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


data = load_data()

# ============================================================
# START
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    data["girl_chat_id"] = chat_id
    save_data(data)

    await update.message.reply_text(
        "❤️ Love Bot is ready!\n\n"
        "This chat is now registered for daily love messages.\n\n"
        "Commands:\n"
        "/test - Send a message now\n"
        "/time 21:00 - Change daily sending time\n"
        "/pause - Pause daily messages\n"
        "/resume - Resume messages\n"
        "/status - Show settings"
    )

# ============================================================
# TEST
# ============================================================

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = random.choice(MESSAGES)

    await update.message.reply_text(message)

    data["last_message"] = message
    save_data(data)

# ============================================================
# PAUSE
# ============================================================

async def pause(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data["paused"] = True
    save_data(data)

    await update.message.reply_text(
        "⏸️ Daily love messages are paused."
    )

# ============================================================
# RESUME
# ============================================================

async def resume(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data["paused"] = False
    save_data(data)

    await update.message.reply_text(
        "▶️ Daily love messages are active again. ❤️"
    )

# ============================================================
# CHANGE TIME
# ============================================================

async def set_time(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Use:\n"
            "/time 21:00\n\n"
            "Example:\n"
            "/time 08:30"
        )
        return

    value = context.args[0]

    try:
        hour, minute = map(int, value.split(":"))

        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError

        data["hour"] = hour
        data["minute"] = minute

        save_data(data)

        # Remove old schedule
        jobs = context.job_queue.get_jobs_by_name(
            "daily_love"
        )

        for job in jobs:
            job.schedule_removal()

        # Create new schedule
        context.job_queue.run_daily(
            send_daily_message,
            time=time(
                hour=hour,
                minute=minute,
                tzinfo=TIMEZONE,
            ),
            name="daily_love",
        )

        await update.message.reply_text(
            f"⏰ Daily message time changed to "
            f"{hour:02d}:{minute:02d} Ethiopia time."
        )

    except ValueError:

        await update.message.reply_text(
            "❌ Invalid time.\n\n"
            "Use 24-hour format.\n\n"
            "Example:\n"
            "/time 21:30"
        )

# ============================================================
# STATUS
# ============================================================

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    state = (
        "⏸️ PAUSED"
        if data["paused"]
        else "▶️ ACTIVE"
    )

    await update.message.reply_text(
        "❤️ LOVE BOT STATUS\n\n"
        f"Status: {state}\n"
        f"Daily time: {data['hour']:02d}:{data['minute']:02d} "
        f"Ethiopia time\n"
        f"Messages available: {len(MESSAGES)}\n"
        f"Registered chat: "
        f"{'Yes' if data['girl_chat_id'] else 'No'}"
    )

# ============================================================
# DAILY MESSAGE
# ============================================================

async def send_daily_message(
    context: ContextTypes.DEFAULT_TYPE
):

    if data["paused"]:
        return

    chat_id = data.get("girl_chat_id")

    if not chat_id:
        return

    message = random.choice(MESSAGES)

    # Prevent immediate repetition
    if len(MESSAGES) > 1:

        while message == data.get("last_message"):
            message = random.choice(MESSAGES)

    try:

        await context.bot.send_message(
            chat_id=chat_id,
            text=message,
        )

        data["last_message"] = message
        save_data(data)

        logging.info(
            "Daily love message sent successfully."
        )

    except Exception as e:

        logging.error(
            f"Could not send daily message: {e}"
        )

# ============================================================
# SETUP DAILY JOB
# ============================================================

def setup_daily_job(application):

    application.job_queue.run_daily(
        send_daily_message,
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

    application.add_handler(
        CommandHandler("start", start)
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

    setup_daily_job(application)

    print("❤️ Love Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
