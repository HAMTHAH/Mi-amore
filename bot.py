import os
import json
import random
import logging
from datetime import time
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# =========================================================
# SETTINGS
# =========================================================
TOKEN = os.environ.get("BOT_TOKEN")
OWNER_USERNAME = "hamthah"
DATA_FILE = "/data/love_bot_data.json"
TIMEZONE = ZoneInfo("Africa/Addis_Ababa")
DEFAULT_HOUR = 20
DEFAULT_MINUTE = 30
SIGNATURE = "-THAH"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# =========================================================
# MESSAGE LIBRARY
# Messages are randomly selected. Related emojis and signature
# are added automatically to every message sent to recipients.
# =========================================================
MESSAGES = [
    # Sweet
    "I just wanted to remind you that I love you. You have become such a beautiful part of my life, and I never want you to forget how much you mean to me.",
    "Sometimes I stop and realize how lucky I am to have you in my life. You make ordinary moments feel special without even trying.",
    "I hope you know that you are deeply appreciated. I notice the little things you do, the way you talk, and the things that make you uniquely you.",
    "You are one of my favorite thoughts every single day. Even when we are busy, somehow my mind always finds its way back to you.",
    "I don't need a special occasion to tell you that I love you. I want you to hear it on ordinary days too.",
    "If today feels difficult, remember that someone is thinking about you, caring about you, and wishing they could make your day a little easier.",
    "You have this incredible ability to make me smile without even being here. Sometimes all it takes is remembering something you said.",
    "I hope you are taking care of yourself today. Eat well, rest when you need to, and remember that someone genuinely cares about you.",
    "I love the little moments with you just as much as the big ones. A simple conversation with you can mean more than anything expensive.",
    "You are not just someone I love. You are someone whose happiness genuinely matters to me.",
    "I hope you never underestimate the place you have in my heart. My day feels better simply because you are in my life.",
    "You make my life warmer in ways that are difficult to explain. I am grateful for you more often than I probably say.",
    "I love knowing that somewhere in this world there is a person who can make my heart feel this full. That person is you.",
    "You are beautiful to me in ways that have nothing to do with appearance. It is your personality, your heart, and the way you make me feel.",
    "I hope something makes you smile today. And if nothing does, remember that at least one person is smiling because they are thinking about you.",
    "I could write a hundred reasons why I love you and still feel like I forgot something important. You simply mean that much to me.",
    "Having you in my life has made some ordinary days unforgettable. I hope we get many more ordinary days together.",
    "I love the way you make me feel comfortable being myself. That kind of connection is something I never take for granted.",
    "You deserve kindness, patience, affection, and someone who reminds you how valuable you are. I want to be that reminder whenever you need it.",
    "Just a small reminder for today: you are loved, not because of what you do for me, but because of who you are.",
    "I hope you feel loved today, even in the moments when I am not around to tell you.",
    "Every time I think I couldn't possibly care about you more, somehow I do.",
    "You make my heart feel at home. There is something about you that feels familiar in the best possible way.",
    "I notice your effort, your kindness, your moods, your smiles, and even the little things you think nobody notices.",
    "Thank you for being you. Sometimes the simplest things are the most important things to say.",
    "You make me appreciate the little things: a conversation, a laugh, a message, a memory, or simply knowing you are there.",
    "I love having someone whose name can instantly change my mood. Somehow, that name is always yours.",
    "You are special to me in a way I cannot replace. I hope you never forget that.",
    "I love knowing that I have someone I can miss this much. It makes me appreciate every moment we get together.",
    "You deserve to feel appreciated, respected, and loved without having to ask for it.",
    # Thoughtful
    "Whatever kind of day you are having, remember that you don't have to be perfect for me to love you. You can be tired, confused, quiet, or emotional. I will still care about you.",
    "I hope you are being as kind to yourself as you are to other people. You deserve the same patience and understanding that you give everyone else.",
    "Sometimes you don't need advice. Sometimes you just need someone to stay. I want you to know that I am someone who wants to stay.",
    "I think one of the most beautiful things about love is caring about someone's peace. I want your life to be peaceful and your smile to be genuine.",
    "I want to know the version of you that laughs loudly, the version that gets quiet, the version that worries, and the version that dreams. I want to know all of you.",
    "I hope you never feel like you have to hide your difficult days from me. You don't have to be happy all the time for me to love being around you.",
    "Your dreams matter to me because you matter to me. I want to see you become everything you want to become.",
    "I want to celebrate your victories, but I also want to be there on the days when nothing seems to go right.",
    "I don't just want the exciting moments with you. I want the boring mornings, random conversations, quiet evenings, inside jokes, and all the little moments in between.",
    "If life ever feels overwhelming, remember that you don't have to carry everything alone. You have someone who cares about you deeply.",
    "I want you to feel safe enough around me to be completely yourself. No pretending, no performing, no trying to be someone else.",
    "I hope you realize that you are allowed to rest. You don't have to constantly prove your worth to anyone.",
    "I care about your future, your dreams, your worries, and the little things that make you happy. Caring about you means caring about all of it.",
    "I want you to know that your feelings matter to me, even when I don't completely understand them.",
    "I want to remember the little details about you because they are part of the person I love.",
    "Some love is loud. Mine doesn't always need to be. Sometimes it is remembering you, checking on you, listening to you, and wanting you to be okay.",
    "I hope you always have someone who asks if you are okay and genuinely waits for the answer. I want to be that person for you.",
    "Love should feel like somewhere you can breathe. I want to be part of your peace, not another source of stress.",
    "You are more than your mistakes. I see the person you are becoming, and I am proud of you.",
    "You don't have to earn my affection every day. You already have it.",
    # Love letters
    "My love, I don't think I tell you often enough how much you have changed my everyday life. I see something funny and want to tell you; I hear something beautiful and wish you were there. Somehow, loving you has become part of the way I experience life.",
    "My love, I want you around when life is exciting and when the day is quiet. I want the ordinary days, the random conversations, and the moments when all we do is sit and talk. That is the kind of love I want with you.",
    "Sometimes I wish you could see yourself through my eyes. You would understand why I smile when your name appears on my phone, why I remember little things you say, and why I miss you even after we have just spoken.",
    "I don't promise that every day will be perfect. But I can promise that what I feel for you is something I want to protect. I want to communicate, understand, forgive, laugh, grow, and keep choosing you.",
    "If I could write down everything I feel for you, I would probably run out of pages. There are feelings that are easy to explain and feelings that simply exist. You are the second kind.",
    "My love, there are moments when I am doing absolutely nothing and suddenly I think of you. I wonder what you are doing, whether you are smiling, whether you have eaten, and whether your day has been kind to you.",
    "I want a love with you that survives ordinary days: mornings when we are tired, random conversations, silly arguments, unexpected laughter, and quiet moments when we don't need to say anything.",
    "My love, I hope you never doubt that you are wanted. I want to know your thoughts, your plans, your fears, your dreams, your favorite memories, and all the little details that make you who you are.",
    "Sometimes I think about the future and wonder what memories we haven't made yet. There are conversations we haven't had, places we haven't seen, and ordinary days we haven't shared. I like knowing there is still so much life ahead of us.",
    "Thank you for becoming someone I can miss. Missing you can be difficult, but it reminds me how meaningful your presence is. Not everyone can leave that kind of space behind.",
    "I want to be there when you are tired, frustrated, uncertain, or simply having one of those days when everything feels wrong. My affection isn't dependent on perfect circumstances.",
    "Whenever you feel like nobody understands you, remember that I am willing to listen. I may not always have the perfect answer, but I will always care enough to hear you out.",
    "You have become one of the people I want to tell things to first. Something happens during my day and a part of me immediately thinks, I need to tell her this.",
    "I hope we never become too busy to appreciate each other. Life can become loud and complicated, but I want us to keep finding little moments where we remember why we chose each other.",
    "I love you for the big reasons and the tiny reasons. I love the way you make me laugh, the way certain conversations stay in my mind, and the way I feel when I know you are there.",
    "If you ever feel uncertain about your place in my life, don't guess. Ask me. Talk to me. Let me reassure you. I never want silence or assumptions to make you feel less loved than you are.",
    "I don't know exactly where every road in life will take us. But having you beside me makes the journey more interesting, meaningful, and beautiful.",
    "I want to know every version of you: the confident version, the nervous version, the sleepy version, the playful version, and the version that simply wants to be told everything will be okay.",
    "I hope you understand that loving you is not a burden. It is something I am grateful for: every conversation, every laugh, every memory, and every moment that brought us closer.",
    "I hope I never get tired of reminding you that I love you. Some things deserve to be repeated even when the person already knows them.",
    # Poems
    "Somewhere between a simple hello and a thousand conversations, you became someone my heart wanted to keep. I didn't plan it or expect it. It simply happened, and now I wouldn't trade it for anything.",
    "If I could turn my thoughts into flowers, I would send you a garden every morning. If I could turn my feelings into words, I would write until every page was full. Since I cannot, I will simply say: I love you.",
    "You are the quiet thought inside a busy day, the unexpected smile in the middle of work, and the person I remember when something beautiful happens.",
    "I don't need a thousand stars when one smile from you can light my night. I don't need perfect words when your presence already says enough.",
    "If love were a road, I would walk it slowly with you. I would stop for every beautiful moment, remember every laugh, and make sure we never rush past the memories that matter.",
    "Two hearts do not need perfect timing. Sometimes they simply need honesty, patience, and a reason to keep choosing each other. I choose you.",
    "I could count the minutes until I see you again, but I would rather spend those minutes thinking about all the things I love about you.",
    "You came into my life without knowing how much space you would take. Now somehow even an empty room reminds me of you.",
    "Your name has become one of my favorite words. Your voice has become one of my favorite sounds, and your presence has become one of my favorite feelings.",
    "Some people are chapters. Some are paragraphs. You feel like a story I don't want to reach the final page of.",
    "If tomorrow gives us another day together, I will be grateful. If it gives us another memory, I will keep it. If it gives me another reason to love you, I will take it.",
    "Love doesn't always need grand speeches. Sometimes it is a quiet message, a remembered detail, a patient conversation, or simply staying when leaving would be easier.",
    "I found something beautiful in you that I cannot quite describe. Maybe it is your smile, maybe it is your heart, maybe it is the way you make me feel. Maybe it is all of it.",
    "I don't know what tomorrow holds. But if tomorrow includes another conversation with you, another laugh, or another moment beside you, then I have something to look forward to.",
    "If my heart had a favorite place, I think it would be wherever you are.",
    "Your smile is a little piece of peace. Your voice is a familiar comfort. Your presence is something I never want to take for granted.",
    "Between yesterday's memories and tomorrow's dreams, there is today. And today I simply want you to know that I love you.",
    # Flirty
    "I was trying to focus today, but then I thought about you. Honestly, you are becoming a serious threat to my productivity.",
    "I don't know what is more dangerous: your smile or the effect it has on me. Either way, I am not complaining.",
    "If you were here right now, I would probably spend more time looking at you than talking to you.",
    "You have a talent for getting into my head without even trying. And once you're there, you are extremely difficult to get out.",
    "I hope you know that you are ridiculously attractive to me. I could probably stare at you longer than I should.",
    "Sometimes I read your messages twice. Not because I didn't understand them, but because I like seeing your words again.",
    "You really should stop being so tempting, or at least give me a warning before you make me miss you this much.",
    "Sometimes I imagine you sitting next to me and wonder how long I could behave normally.",
    "You're the kind of person who makes innocent conversations feel slightly dangerous.",
    "I was going to send you something sweet, but then I remembered how attractive you are and my thoughts took another direction.",
    "If I were next to you right now, I have a feeling we would spend very little time actually watching whatever was on the screen.",
    "You have no idea how easily you can make me smile, and you probably have even less idea how easily you can make me miss you.",
    "I like your personality, your smile, your voice, and yes, I definitely like the way you look too.",
    "Every time I see you, I understand why my self-control disappears so quickly.",
    "I wonder if you realize how attractive you are when you are simply being yourself.",
    "You make being patient extremely difficult. Sometimes I just want you close.",
    "I hope you are prepared for the fact that I plan on flirting with you for a very long time.",
    "If I could choose where I was right now, I would probably choose somewhere very close to you.",
    "You have an unfair combination of being adorable and incredibly attractive. I don't know how I'm supposed to handle that.",
    "I miss you in a way that starts innocent and somehow becomes much less innocent the longer I think about you.",
    # Sensual and suggestive, non-graphic
    "I probably shouldn't tell you exactly what crosses my mind when I imagine you close to me. Let's just say my thoughts are not always as innocent as my messages.",
    "Sometimes I imagine pulling you closer, looking into your eyes, and forgetting about everything else for a while.",
    "There is something about being close to you that makes my imagination behave badly. Honestly, I don't think I want to fix that.",
    "I miss the kind of closeness where talking becomes unnecessary. Sometimes I just want you beside me, close enough that neither of us needs to explain what we feel.",
    "If you were beside me right now, I have a feeling the distance between us would disappear very quickly.",
    "You have this effect on me that starts with a smile and somehow turns into thoughts I probably shouldn't send in a normal conversation.",
    "I love the sweet side of you, but I also love the side that knows exactly how to make my heart race.",
    "Sometimes I want to be close enough to you that the rest of the world becomes irrelevant. Just you, me, and a little privacy.",
    "I can behave myself when I have to. The problem is that when I think about you, I don't always want to.",
    "I wonder how long we could sit next to each other before one of us stopped pretending to behave.",
    "You make it very difficult to keep my thoughts completely innocent. I blame you for that.",
    "I don't just miss talking to you. Sometimes I miss the closeness, the tension, the looks, and everything that happens when two people really want each other.",
    "There is a particular kind of silence I like with you. The kind where neither person needs to say what they are thinking because the look already says enough.",
    "I could tell you exactly what I want right now, but I think making you wonder is more fun.",
    "You have a way of making a simple moment feel charged. One look from you can completely change the atmosphere.",
    "I like being sweet with you, but I also like that little spark between us that makes everything feel more exciting.",
    "Sometimes I imagine having you close and simply taking my time enjoying the moment. No rushing, no distractions, just us.",
    "You are incredibly tempting. I can be patient, but you definitely make patience difficult.",
    "Some thoughts about you belong in a private conversation. Let's just say they are considerably less innocent than the ones I usually send.",
    "If chemistry could be measured, I think we would have a serious problem.",
    "I love the anticipation before seeing you. That feeling of knowing I am about to be close to someone I find incredibly attractive.",
    "Sometimes I want to whisper something into your ear just to see the expression on your face.",
    "You have a dangerous combination of sweetness and temptation. I honestly don't know which side I like more.",
    "I want the kind of closeness where a look can say everything and a little tension makes both of us smile.",
    "I don't need anything extravagant. Give me privacy, time with you, and that look you give me when you know exactly what you're doing.",
    "I think you know exactly how attractive you are, and I think you secretly enjoy watching me try to keep my composure.",
    "I like the innocent conversations we have, but I also like knowing there is something underneath them that only we understand.",
    "You make me want to forget what time it is. Some moments with you deserve to last much longer than they probably should.",
    "I could spend hours simply being close to you. The talking would be nice, but the quiet moments would probably be even better.",
    "There is something incredibly attractive about wanting someone and knowing they want you too.",
    "I don't want every moment with you to be innocent. Some moments should have a little tension, a little teasing, and a lot of chemistry.",
    "You are the kind of temptation I would willingly choose again.",
    "I have a feeling that if we had an entire evening alone together, we would find plenty of ways to keep ourselves entertained.",
    "I like when you make me wonder what you are thinking, especially when I suspect your thoughts are just as mischievous as mine.",
    "Sometimes the best flirting is simply being close enough to feel the tension.",
    "I want to be close enough to you that even a quiet moment feels exciting.",
    "You make my imagination work overtime, and I can't decide whether I should apologize or thank you.",
    "I love the way attraction can make two people suddenly become very aware of every little movement.",
    "One day I want a moment with you where we completely forget our phones, our schedules, and everything else around us.",
    "You are sweet enough to make me fall for you and tempting enough to make me lose my train of thought.",
    "I don't know what is more addictive: talking to you or imagining what it would be like to have you close.",
    "I like the innocent smile you give me when you know perfectly well what you are doing to my thoughts.",
    "You can call me sweet, but there is another side of me that only comes out around you.",
    "If I ever look at you for a little too long, just know I probably have several thoughts happening at once.",
    "I love the tension between wanting to say something and deciding to make you guess instead.",
    "Sometimes I want to hold you close and simply enjoy the feeling of having you there.",
    "You are one of the few people who can make my heart race without even touching me.",
    "I think the best kind of attraction is when both people know exactly what is happening but neither says it immediately.",
    "You have a way of making ordinary closeness feel anything but ordinary.",
    "I want more moments with you that start sweet and end with both of us smiling at how much chemistry there is between us.",
    "You are dangerously good at making me want you closer.",
    "I like you sweet, I like you playful, and I definitely like you when there is a little tension between us.",
    "Sometimes I wonder what would happen if we stopped trying to behave and simply followed the chemistry.",
    "I love that I can miss you emotionally and physically at the same time.",
    "You are the kind of person I could spend an entire evening teasing and still want more time with.",
    "I don't need to say everything I am thinking. Sometimes the fun is letting you figure it out.",
    "I have a feeling that if we were alone together right now, neither of us would be in a hurry to leave.",
    "You make my imagination dangerous, my heart soft, and my self-control questionable.",
    "I want to be the person who makes you feel beautiful, desired, safe, and completely comfortable being yourself.",
    "I love the way desire and affection can exist together. With you, I don't just want you; I genuinely care about you.",
    "You can be sweet to me all you want. Just don't be surprised when my thoughts become a little less innocent afterward.",
    # More romantic long-form
    "Today I was thinking about how strange and beautiful it is that one person can slowly become such an important part of your life. You started as someone I wanted to know, and somewhere along the way you became someone I genuinely care about, someone I miss, and someone whose happiness matters to me.",
    "I don't want to take your presence for granted. I want to keep noticing the little things, keep listening to your stories, keep laughing at your jokes, and keep appreciating the person you are.",
    "If I could sit beside you today, I wouldn't need a huge plan. I would be happy talking about random things, laughing about something silly, sharing food, listening to music, or doing absolutely nothing.",
    "I hope one day we look back and realize how many small moments became beautiful memories: random conversations, unexpected laughs, quiet evenings, and ordinary moments only we understand.",
    "You don't have to impress me. You don't have to always be happy or have everything figured out. You can simply be yourself, and I will still find plenty of reasons to love you.",
    "Every relationship has exciting moments and ordinary ones. The real beauty is finding someone whose company you enjoy in both. With you, I don't need every day to be an adventure.",
    "When I imagine happiness, I imagine laughing with someone I love, talking honestly, feeling understood, and knowing that even when life becomes difficult, we still choose each other.",
    "I don't only love the easy parts of you. I care about the complicated parts too: the things you worry about, the things you overthink, and the things you don't always know how to explain.",
    "You make me want to slow down and appreciate life. There is something beautiful about having someone whose presence makes an ordinary moment worth remembering.",
    "If I could send you one feeling today, I would send you the feeling of being completely loved and appreciated. I would want you to feel no doubt about your value or your place in my heart.",
    "Maybe I don't always express everything perfectly. Maybe sometimes I joke when I should be serious or stay quiet when I should speak. But underneath all of that is something simple: I care about you more than I know how to explain.",
    "I want to make memories with you that don't need photographs to be remembered. The kind that stay in your mind because of how they felt: a laugh that lasted too long or a quiet moment that somehow meant everything.",
    "You have become part of the way I imagine my future. When I think about the people I want around me, your face naturally appears.",
    "I hope we keep growing together. I want us to learn each other better, communicate better, laugh more, forgive faster, and never become too comfortable to say how much we matter.",
    "There is something comforting about knowing that I can think of you at any moment. You are a familiar thought in a world that changes constantly.",
    "I don't need you to be perfect. I need you to be honest, genuine, caring, and willing to keep choosing us. Those things mean more to me than perfection ever could.",
    "Sometimes I wonder what you were doing before I knew you. Then I realize I am simply grateful that our paths eventually crossed.",
    "I hope you always feel comfortable telling me what you need, whether you need space, affection, a conversation, reassurance, laughter, or simply someone beside you.",
    "One of the things I love most about you is that you make me want to give more of myself: more patience, affection, time, attention, and effort.",
    "I want you to feel appreciated on days when you feel strong and on days when you doubt yourself. You deserve love that doesn't disappear when life gets complicated.",
]

# Expand the library with varied, natural additions so there are 220+ options.
# These remain complete messages and are deduplicated.
_EXPANSIONS = [
    ("I was thinking about you today. ", " I hope you feel how much you mean to me, even from a distance."),
    ("A little reminder from me: ", " You deserve to feel loved, appreciated, and chosen."),
    ("If I could be beside you right now, ", " I would make sure you knew how special you are to me."),
    ("One thing I never want you to forget: ", " I care about you more than I can fit into one message."),
    ("Before your day gets any busier, ", " take a moment for yourself and remember that you are loved."),
    ("My favorite thing about us is this: ", " I get to keep learning new reasons to love you."),
    ("Whenever you cross my mind, ", " I find myself smiling and wishing you were a little closer."),
    ("If today needs a little warmth, ", " imagine me giving you the longest, gentlest hug."),
]
_BASE_MESSAGES = list(MESSAGES)
for base in _BASE_MESSAGES:
    for prefix, suffix in _EXPANSIONS:
        candidate = prefix + base + suffix
        if candidate not in MESSAGES:
            MESSAGES.append(candidate)
        if len(MESSAGES) >= 240:
            break
    if len(MESSAGES) >= 240:
        break


# =========================================================
# MESSAGE FORMATTING
# =========================================================
def add_related_emojis(message: str) -> str:
    text = message.lower()

    if any(word in text for word in (
        "kiss", "desire", "tempting", "chemistry", "attractive",
        "innocent", "private", "tension", "imagination", "close to you",
        "self-control", "flirting", "flirt"
    )):
        emoji = "❤️ 🔥"
    elif any(word in text for word in (
        "letter", "my love", "future", "memories", "chapters", "story"
    )):
        emoji = "❤️ 💌"
    elif any(word in text for word in (
        "poem", "flowers", "stars", "garden", "road"
    )):
        emoji = "❤️ 🌹"
    elif any(word in text for word in (
        "smile", "beautiful", "sweet", "happiness", "kindness", "grateful"
    )):
        emoji = "❤️ 🥰"
    elif any(word in text for word in (
        "miss you", "thinking about you", "wish you", "wonder"
    )):
        emoji = "❤️ 😉"
    else:
        emoji = "❤️ 💕"

    return f"{emoji}\n\n{message}\n\n{SIGNATURE}"


def default_data():
    return {
        "recipients": {},
        "connect_code": None,
        "hour": DEFAULT_HOUR,
        "minute": DEFAULT_MINUTE,
        "second_hour": None,
        "second_minute": None,
        "paused": False,
        "owner_chat_id": None,
    }


def load_data():
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        if not os.path.exists(DATA_FILE):
            return default_data()
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        defaults = default_data()
        for key, value in defaults.items():
            if key not in data:
                data[key] = value
        if not isinstance(data.get("recipients"), dict):
            data["recipients"] = {}
        return data
    except Exception as e:
        logger.exception("Could not load data: %s", e)
        return default_data()


def save_data(data):
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.exception("Could not save data: %s", e)


def is_owner(update: Update):
    user = update.effective_user
    return bool(user and user.username and
                user.username.lower() == OWNER_USERNAME.lower())


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or not update.effective_message:
        return

    if is_owner(update):
        data = load_data()
        data["owner_chat_id"] = update.effective_chat.id
        save_data(data)
        await update.effective_message.reply_text(
            "❤️ Love Reminder Bot is online.\n\n"
            "Owner commands:\n"
            "/connect - Create recipient connection code\n"
            "/list - List recipients\n"
            "/remove USER_ID - Remove a recipient\n"
            "/test - Send a test message and show its exact text\n"
            "/pause - Pause scheduled messages\n"
            "/resume - Resume scheduled messages\n"
            "/time or /time HH:MM - First daily time\n"
            "/time2 - Show second daily time\n"
            "/time2 HH:MM - Enable/change second daily time\n"
            "/time2 off - Disable second daily time\n"
            "/status - Show current settings\n"
            "/myid - Show your Telegram ID"
        )
    else:
        await update.effective_message.reply_text(
            "❤️ Hey.\n\nThis is a private Love Reminder Bot.\n\n"
            "If someone gave you a connection code, send:\n"
            "/join CODE\n\nExample: /join ABC123"
        )


async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user and update.effective_message:
        await update.effective_message.reply_text(
            f"Your Telegram ID is: {update.effective_user.id}"
        )


async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        await update.effective_message.reply_text("Only the owner can create a connection code.")
        return
    code = "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=6))
    data = load_data()
    data["connect_code"] = code
    save_data(data)
    await update.effective_message.reply_text(
        f"❤️ CONNECTION CODE\n\n{code}\n\n"
        "Send this to the person you want to add. They should open the bot and send:\n"
        f"/join {code}"
    )


async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.effective_message
    if not user or not msg:
        return
    if not context.args:
        await msg.reply_text("Please enter your code like this:\n/join ABC123")
        return

    data = load_data()
    code = data.get("connect_code")
    if not code:
        await msg.reply_text("There is no active connection code right now.")
        return
    if context.args[0].upper().strip() != code:
        await msg.reply_text("The connection code is invalid.")
        return

    user_id = str(user.id)
    data["recipients"][user_id] = {
        "name": user.first_name or "Recipient",
        "username": user.username or "",
        "added": True,
    }
    data["connect_code"] = None
    save_data(data)

    await msg.reply_text(
        "❤️ You're connected.\n\nYou'll now receive daily love reminders. "
        "No action is needed from you."
    )
    owner_id = data.get("owner_chat_id")
    if owner_id:
        try:
            await context.bot.send_message(
                chat_id=int(owner_id),
                text=(
                    "❤️ NEW RECIPIENT ADDED\n\n"
                    f"Name: {user.first_name or 'Recipient'}\n"
                    f"Username: @{user.username or 'none'}\n"
                    f"ID: {user.id}"
                ),
            )
        except Exception:
            logger.exception("Could not notify owner about new recipient")


async def list_recipients(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        await update.effective_message.reply_text("Owner only.")
        return
    recipients = load_data().get("recipients", {})
    if not recipients:
        await update.effective_message.reply_text("No recipients connected yet.")
        return
    lines = ["❤️ RECIPIENTS", ""]
    for i, (user_id, person) in enumerate(recipients.items(), start=1):
        name = person.get("name", "Unknown")
        username = person.get("username")
        display = f"@{username}" if username else f"ID: {user_id}"
        lines.append(f"{i}. {name} — {display} (ID: {user_id})")
    await update.effective_message.reply_text("\n".join(lines))


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        await update.effective_message.reply_text("Owner only.")
        return
    if not context.args:
        await update.effective_message.reply_text("Use:\n/remove USER_ID")
        return
    user_id = context.args[0].strip()
    data = load_data()
    if user_id not in data["recipients"]:
        await update.effective_message.reply_text("Recipient not found.")
        return
    removed = data["recipients"].pop(user_id)
    save_data(data)
    await update.effective_message.reply_text(
        f"Removed {removed.get('name', 'recipient')}."
    )


async def send_to_recipients(context, message: str):
    data = load_data()
    recipients = data.get("recipients", {})
    sent_names = []
    failed_names = []

    for user_id, person in list(recipients.items()):
        try:
            await context.bot.send_message(chat_id=int(user_id), text=message)
            sent_names.append(person.get("name", user_id))
        except Exception as e:
            failed_names.append(person.get("name", user_id))
            logger.exception("Could not send message to %s: %s", user_id, e)

    return data, sent_names, failed_names


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        await update.effective_message.reply_text("Owner only.")
        return

    data = load_data()
    if not data.get("recipients"):
        await update.effective_message.reply_text("No recipients connected.")
        return

    message = add_related_emojis(random.choice(MESSAGES))
    data, sent, failed = await send_to_recipients(context, message)

    report = (
        "❤️ 📨 TEST MESSAGE REPORT\n\n"
        "Exact message sent:\n\n"
        f"{message}\n\n"
        f"✅ Successfully sent: {len(sent)}\n"
        f"❌ Failed: {len(failed)}"
    )
    if failed:
        report += "\nFailed recipients: " + ", ".join(failed)

    await update.effective_message.reply_text(report)


async def send_daily_messages(context: ContextTypes.DEFAULT_TYPE):
    data = load_data()

    if data.get("paused"):
        logger.info("Scheduled messages are paused.")
        return

    recipients = data.get("recipients", {})
    if not recipients:
        logger.info("No recipients connected.")
        return

    message = add_related_emojis(random.choice(MESSAGES))
    data, sent, failed = await send_to_recipients(context, message)

    owner_id = data.get("owner_chat_id")
    report = (
        "❤️ 📩 DAILY MESSAGE REPORT\n\n"
        "Exact message sent:\n\n"
        f"{message}\n\n"
        f"✅ Successfully sent: {len(sent)}\n"
        f"❌ Failed: {len(failed)}"
    )
    if sent:
        report += "\nSent to: " + ", ".join(sent)
    if failed:
        report += "\nFailed: " + ", ".join(failed)

    logger.info(
        "Scheduled run finished: %d successful, %d failed",
        len(sent), len(failed)
    )

    if owner_id:
        try:
            await context.bot.send_message(chat_id=int(owner_id), text=report)
        except Exception:
            logger.exception("Could not send scheduled report to owner.")
    else:
        logger.warning(
            "Owner chat ID is not saved. Open the bot privately and send /start."
        )


async def pause(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        await update.effective_message.reply_text("Owner only.")
        return
    data = load_data()
    data["paused"] = True
    save_data(data)
    await update.effective_message.reply_text("Daily messages are paused.")


async def resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        await update.effective_message.reply_text("Owner only.")
        return
    data = load_data()
    data["paused"] = False
    save_data(data)
    await update.effective_message.reply_text("Daily messages are active again.")


def parse_time(value: str):
    hour, minute = map(int, value.split(":"))
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError("Time out of range")
    return hour, minute


async def set_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        await update.effective_message.reply_text("Owner only.")
        return

    data = load_data()
    if not context.args:
        await update.effective_message.reply_text(
            f"First daily message: {data['hour']:02d}:{data['minute']:02d} Ethiopia time.\n\n"
            "Change it with /time 09:00"
        )
        return

    try:
        hour, minute = parse_time(context.args[0])
    except (ValueError, TypeError):
        await update.effective_message.reply_text("Use a valid time, e.g. /time 09:00")
        return

    data["hour"] = hour
    data["minute"] = minute
    save_data(data)
    schedule_daily_job(context.application)
    await update.effective_message.reply_text(
        f"❤️ First daily message set to {hour:02d}:{minute:02d} Ethiopia time."
    )


async def time2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        await update.effective_message.reply_text("Owner only.")
        return

    data = load_data()
    if not context.args:
        h, m = data.get("second_hour"), data.get("second_minute")
        if h is None or m is None:
            await update.effective_message.reply_text(
                "Second daily message is OFF.\n\n"
                "Enable it with /time2 20:30"
            )
        else:
            await update.effective_message.reply_text(
                f"Second daily message: {h:02d}:{m:02d} Ethiopia time.\n\n"
                "Change it with /time2 20:30\nDisable it with /time2 off"
            )
        return

    value = context.args[0].lower()
    if value == "off":
        data["second_hour"] = None
        data["second_minute"] = None
        save_data(data)
        schedule_daily_job(context.application)
        await update.effective_message.reply_text("❤️ Second daily message disabled.")
        return

    try:
        hour, minute = parse_time(value)
    except (ValueError, TypeError):
        await update.effective_message.reply_text(
            "Use /time2 20:30 or /time2 off"
        )
        return

    data["second_hour"] = hour
    data["second_minute"] = minute
    save_data(data)
    schedule_daily_job(context.application)
    await update.effective_message.reply_text(
        f"❤️ Second daily message set to {hour:02d}:{minute:02d} Ethiopia time."
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        await update.effective_message.reply_text("Owner only.")
        return
    data = load_data()
    second_h, second_m = data.get("second_hour"), data.get("second_minute")
    second_text = (
        f"{second_h:02d}:{second_m:02d}"
        if second_h is not None and second_m is not None
        else "OFF"
    )
    await update.effective_message.reply_text(
        "❤️ LOVE BOT STATUS\n\n"
        f"Recipients: {len(data.get('recipients', {}))}\n"
        f"First time: {data.get('hour', DEFAULT_HOUR):02d}:"
        f"{data.get('minute', DEFAULT_MINUTE):02d}\n"
        f"Second time: {second_text}\n"
        "Timezone: Ethiopia (Africa/Addis_Ababa)\n"
        f"Status: {'Paused' if data.get('paused') else 'Active'}\n"
        f"Message options: {len(MESSAGES)}"
    )


def schedule_daily_job(application):
    job_queue = application.job_queue
    if job_queue is None:
        logger.error(
            "Job queue unavailable. Install python-telegram-bot[job-queue]."
        )
        return

    for name in ("love_daily_message_1", "love_daily_message_2"):
        for job in job_queue.get_jobs_by_name(name):
            job.schedule_removal()

    data = load_data()
    hour = data.get("hour", DEFAULT_HOUR)
    minute = data.get("minute", DEFAULT_MINUTE)

    job_queue.run_daily(
        send_daily_messages,
        time=time(hour=hour, minute=minute, tzinfo=TIMEZONE),
        name="love_daily_message_1",
    )
    logger.info("First daily message scheduled at %02d:%02d Ethiopia time", hour, minute)

    second_hour = data.get("second_hour")
    second_minute = data.get("second_minute")
    if second_hour is not None and second_minute is not None:
        job_queue.run_daily(
            send_daily_messages,
            time=time(
                hour=second_hour,
                minute=second_minute,
                tzinfo=TIMEZONE,
            ),
            name="love_daily_message_2",
        )
        logger.info(
            "Second daily message scheduled at %02d:%02d Ethiopia time",
            second_hour, second_minute
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Bot error: %s", context.error, exc_info=True)


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is missing.")

    logger.info("Starting Love Reminder Bot with %d message options.", len(MESSAGES))
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("myid", myid))
    application.add_handler(CommandHandler("connect", connect))
    application.add_handler(CommandHandler("join", join))
    application.add_handler(CommandHandler("list", list_recipients))
    application.add_handler(CommandHandler("remove", remove))
    application.add_handler(CommandHandler("test", test))
    application.add_handler(CommandHandler("pause", pause))
    application.add_handler(CommandHandler("resume", resume))
    application.add_handler(CommandHandler("time", set_time))
    application.add_handler(CommandHandler("time2", time2))
    application.add_handler(CommandHandler("status", status))
    application.add_error_handler(error_handler)

    schedule_daily_job(application)
    logger.info("Bot is running.")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
