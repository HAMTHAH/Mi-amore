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
# MESSAGE LIBRARY
# 220+ messages
# Only emoji used: ❤️
# =========================================================

MESSAGES = [

# =========================================================
# SWEET
# =========================================================

"I just wanted to remind you that I love you. ❤️ You have become such a beautiful part of my life, and I never want you to forget how much you mean to me.",

"Sometimes I stop and realize how lucky I am to have you in my life. ❤️ You make ordinary moments feel special without even trying.",

"I hope you know that you are deeply appreciated. ❤️ I notice the little things you do, the way you talk, the way you care, and all the little things that make you you.",

"You are one of my favorite thoughts every single day. ❤️ Even when we are busy and doing completely different things, somehow my mind always finds its way back to you.",

"I don't need a special occasion to tell you that I love you. ❤️ I want you to hear it on ordinary days too, because ordinary days are the ones we actually live.",

"If today feels difficult, remember that there is someone thinking about you, caring about you, and wishing they could make your day a little easier. ❤️",

"You have this incredible ability to make me smile without even being here. ❤️ Sometimes all it takes is remembering something you said.",

"I hope you are taking care of yourself today. ❤️ Eat well, rest when you need to, and remember that someone genuinely cares about how you are doing.",

"I love the little moments with you just as much as the big ones. ❤️ Sometimes a simple conversation with you means more to me than anything expensive or complicated.",

"You are not just someone I love. ❤️ You are someone whose happiness genuinely matters to me.",

"I hope you never underestimate the place you have in my heart. ❤️ There is a part of my day that feels better simply because you are in my life.",

"You make my life warmer in ways that are difficult to explain. ❤️ I am grateful for you more often than I probably say.",

"I love knowing that somewhere in this world there is a person who can make my heart feel this full. ❤️ That person is you.",

"You are beautiful to me in ways that have nothing to do with appearance. ❤️ It is your personality, your heart, your little habits, and the way you make me feel.",

"I hope something makes you smile today. ❤️ And if nothing does, remember that at least one person is smiling because they are thinking about you.",

"I could write a hundred reasons why I love you and still feel like I forgot something important. ❤️ You simply mean that much to me.",

"Having you in my life has made some ordinary days unforgettable. ❤️ I hope we get many more ordinary days together.",

"I love the way you make me feel comfortable being myself. ❤️ That kind of connection is something I never take for granted.",

"You deserve kindness, patience, affection, and someone who reminds you how valuable you are. ❤️ I want to be that reminder whenever you need it.",

"Just a small reminder for today: you are loved. ❤️ Not because of what you do for me, but because of who you are.",

"I hope you know that your presence matters. ❤️ You matter to me more than you probably realize.",

"There are people you meet and forget, and then there are people who quietly become part of your heart. ❤️ You became the second kind for me.",

"I love hearing your thoughts, even the random ones that make absolutely no sense. ❤️ I could listen to you talk for hours.",

"You have become one of the easiest people in the world for me to miss. ❤️ One quiet moment is enough for me to start wishing you were closer.",

"I hope today treats you gently. ❤️ You deserve a day where everything feels a little easier.",

"I don't need a perfect relationship. ❤️ I just want something real, honest, warm, and full of moments that belong to us.",

"Thank you for being you. ❤️ I know that sounds simple, but sometimes the simplest things are the most important things to say.",

"You make me appreciate the little things. ❤️ A conversation, a laugh, a message, a memory, or simply knowing you are there.",

"I love having someone whose name can instantly change my mood. ❤️ Somehow, that name is always yours.",

"You are special to me in a way I cannot replace. ❤️ I hope you never forget that.",

"I hope you feel loved today, even in the moments when I am not around to tell you. ❤️",

"Every time I think I couldn't possibly care about you more, somehow I do. ❤️",

"I love knowing that I have someone I can miss this much. ❤️ It makes me appreciate every moment we actually get together.",

"You make my heart feel at home. ❤️ There is something about you that feels familiar in the best possible way.",

"I hope you know that I notice you. ❤️ I notice your effort, your kindness, your moods, your smiles, and even the little things you think nobody notices.",

"You deserve to know how beautiful your presence is in someone's life. ❤️ In mine, it is beautiful.",


# =========================================================
# THOUGHTFUL
# =========================================================

"Whatever kind of day you are having, please remember that you don't have to be perfect for me to love you. ❤️ You can be tired, confused, quiet, emotional, or simply having a bad day. I will still care about you.",

"I hope you are being as kind to yourself as you are to other people. ❤️ You deserve the same patience and understanding that you give everyone else.",

"Sometimes you don't need advice. Sometimes you just need someone to stay. ❤️ I want you to know that I am someone who wants to stay.",

"I think one of the most beautiful things about love is caring about someone's peace. ❤️ I want your life to be peaceful, your heart to be light, and your smile to be genuine.",

"I want to know the version of you that laughs loudly, the version that gets quiet, the version that worries, and the version that dreams. ❤️ I want to know all of you.",

"I hope you never feel like you have to hide your difficult days from me. ❤️ You don't have to be happy all the time for me to love being around you.",

"Your dreams matter to me because you matter to me. ❤️ I want to see you become everything you want to become.",

"I want to celebrate your victories, but I also want to be there on the days when nothing seems to go right. ❤️",

"Sometimes I wonder if you realize how much your small actions affect me. ❤️ A simple message from you can turn an ordinary day around.",

"I don't just want the exciting moments with you. ❤️ I want the boring mornings, random conversations, quiet evenings, inside jokes, and all the little moments in between.",

"If life ever feels overwhelming, remember that you don't have to carry everything alone. ❤️ You have someone who cares about you deeply.",

"I want you to feel safe enough around me to be completely yourself. ❤️ No pretending, no performing, no trying to be someone else.",

"One thing I genuinely admire about you is the person you are when nobody is watching. ❤️ That tells me more about you than anything else could.",

"I hope you realize that you are allowed to rest. ❤️ You don't have to constantly prove your worth to anyone.",

"I care about your future, your dreams, your worries, and the little things that make you happy. ❤️ Caring about you means caring about all of it.",

"If I could give you one thing today, it would be peace of mind. ❤️ I would want you to feel safe knowing that someone has your back.",

"I love learning new things about you. ❤️ Even after knowing you for a while, there are still little details about you that make me smile.",

"I don't want to only know how your day went. ❤️ I want to know how your heart felt during it.",

"Your happiness isn't something I take lightly. ❤️ When you are genuinely happy, it makes me happy too.",

"I hope you remember that you are more than your mistakes. ❤️ I see the person you are becoming, and I am proud of you.",

"I want to be someone you can talk to without worrying about being judged. ❤️ Your thoughts are safe with me.",

"I love the person you are today, but I am also excited about the person you are becoming. ❤️",

"Sometimes I don't know exactly what to say, but I hope my actions always make one thing clear: I care about you deeply. ❤️",

"You don't have to earn my affection every day. ❤️ You already have it.",

"I hope you never confuse a difficult season with a difficult life. ❤️ Better days can still be ahead.",

"I want you to know that your feelings matter to me, even when I don't completely understand them. ❤️",

"The more I know you, the more I understand why my heart chose you. ❤️",

"I want to remember the little details about you because they are part of the person I love. ❤️",

"I hope you always have someone who asks if you are okay and genuinely waits for the answer. ❤️ I want to be that person for you.",

"Some love is loud. Mine doesn't always need to be. ❤️ Sometimes it is simply remembering you, checking on you, listening to you, and wanting you to be okay.",

"I care about the things you don't always say out loud. ❤️ Sometimes your silence tells me you need a little extra affection.",

"I hope you know that you never have to compete for a place in my heart. ❤️ You already have yours.",

"I want to be part of your peaceful moments, not another source of stress. ❤️ Love should feel like somewhere you can breathe.",

"I notice when you are tired. ❤️ I notice when your mood changes. I notice when you need attention. I may not always get it right, but I care enough to notice.",

"I hope life gives you reasons to be proud of yourself. ❤️ And when you forget those reasons, I will remind you.",


# =========================================================
# LOVE LETTERS
# =========================================================

"My love, I don't think I tell you often enough how much you have changed my everyday life. ❤️ Before you, I didn't realize how much one person could become part of another person's thoughts. Now you appear in the smallest moments. I see something funny and want to tell you. I hear something beautiful and wish you were there. I have a good day and want to share it with you. Somehow, loving you has become part of the way I experience life.",

"My love, if you ever wonder what you mean to me, I hope you remember this. ❤️ You are someone I don't simply want around when life is exciting. I want you around when the day is quiet, when nothing interesting happens, when we have nothing planned, and when all we do is sit and talk. That is the kind of love I want with you: something that feels good even when nothing special is happening.",

"Sometimes I wish you could see yourself through my eyes. ❤️ You would understand why I smile when your name appears on my phone. You would understand why I remember little things you say. You would understand why I miss you even after we have just spoken. Maybe then you would finally understand just how much space you have taken up in my heart.",

"My love, I don't promise that every day will be perfect. ❤️ I cannot promise that life will never be difficult or that we will never disagree. But I can promise that what I feel for you is something I want to protect. I want to communicate, understand, forgive, laugh, grow, and keep choosing you.",

"If I could write down everything I feel for you, I would probably run out of pages. ❤️ There are feelings that are easy to explain and feelings that simply exist. You are the second kind. I know what happens inside me when I hear your voice, see your name, or remember your smile. I just don't always have words big enough for it.",

"My love, there are moments when I am doing absolutely nothing and suddenly I think of you. ❤️ I wonder what you are doing, whether you are smiling, whether you have eaten, whether your day has been kind to you. That is how I know you have become important to me. Caring about you happens naturally.",

"I want a love with you that survives ordinary days. ❤️ I want the mornings when neither of us looks perfect, the evenings when we are tired, the random conversations, the silly arguments, the unexpected laughter, and the quiet moments when we don't need to say anything. I want something real enough to live inside everyday life.",

"My love, I hope you never doubt that you are wanted. ❤️ I don't only want your attention when it is convenient. I want to know your thoughts, your plans, your fears, your dreams, your favorite memories, and all those little details that make you who you are.",

"Sometimes I think about the future and I find myself wondering what memories we haven't made yet. ❤️ There are conversations we haven't had, places we haven't seen, jokes we haven't created, and ordinary days we haven't shared. I like knowing that there is still so much life ahead of us.",

"My love, thank you for becoming someone I can miss. ❤️ Missing you can be difficult, but it also reminds me how meaningful your presence is. Not everyone can leave that kind of space behind when they are gone.",

"I don't want to love you only when everything is easy. ❤️ I want to be there when you are tired, frustrated, uncertain, or simply having one of those days when everything feels wrong. I want you to know that my affection isn't dependent on perfect circumstances.",

"Whenever you feel like nobody understands you, remember that I am willing to listen. ❤️ I may not always have the perfect answer, but I will always care enough to hear you out.",

"My love, you have become one of the people I want to tell things to first. ❤️ Something happens during my day and a part of me immediately thinks, I need to tell her this. That little instinct means more to me than I can explain.",

"I hope we never become too busy to appreciate each other. ❤️ Life can become loud and complicated, but I want us to keep finding little moments where we stop and remember why we chose each other.",

"I love you for the big reasons and the tiny reasons. ❤️ I love the way you make me laugh. I love the way certain conversations with you stay in my mind. I love the way I feel when I know you are there. I love the person I become when I am around you.",

"My love, if you ever feel uncertain about your place in my life, don't guess. ❤️ Ask me. Talk to me. Let me reassure you. I never want silence or assumptions to make you feel less loved than you are.",

"I don't know exactly where every road in life will take us. ❤️ But I know that having you beside me makes the journey more interesting, more meaningful, and much more beautiful.",

"Sometimes the best part of my day is not something that happened. ❤️ It is simply remembering that I have you. That thought alone can make an ordinary day feel completely different.",

"My love, I want to know every version of you. ❤️ The confident version, the nervous version, the sleepy version, the playful version, the serious version, and the version that simply wants to be held and told everything will be okay.",

"I hope you understand that loving you is not something I consider a burden. ❤️ It is something I am grateful for. I am grateful for every conversation, every laugh, every memory, every disagreement that taught us something, and every moment that brought us closer.",


# =========================================================
# POEMS
# =========================================================

"Somewhere between a simple hello and a thousand conversations, you became someone my heart wanted to keep. ❤️ I didn't plan it. I didn't expect it. It simply happened, and now I wouldn't trade it for anything.",

"If I could turn my thoughts into flowers, I would send you a garden every morning. ❤️ If I could turn my feelings into words, I would write until every page was full. Since I cannot, I will simply say: I love you.",

"You are the thought that stays when the noise disappears. ❤️ You are the name my heart remembers when the day becomes quiet. You are the person I look for in memories and the person I hope to find in my future.",

"I don't need a thousand stars when one smile from you can light my night. ❤️ I don't need perfect words when your presence already says enough. I don't need a perfect life when I have someone I genuinely love.",

"If love were a road, I would walk it slowly with you. ❤️ I would stop for every beautiful moment, remember every laugh, and make sure we never rush past the memories that matter.",

"You are the quiet thought inside a busy day. ❤️ The unexpected smile in the middle of work. The person I remember when something beautiful happens. Somehow, you have become part of everything good.",

"Two hearts do not need perfect timing. ❤️ Sometimes they simply need honesty, patience, and a reason to keep choosing each other. I choose you.",

"I could count the minutes until I see you again, but I would rather spend those minutes thinking about all the things I love about you. ❤️",

"You came into my life without knowing how much space you would take. ❤️ Now somehow even an empty room reminds me of you.",

"Your name has become one of my favorite words. ❤️ Your voice has become one of my favorite sounds. And your presence has become one of my favorite feelings.",

"If tomorrow gives us another day together, I will be grateful. ❤️ If it gives us another memory, I will keep it. If it gives me another reason to love you, I will take it.",

"Love doesn't always need grand speeches. ❤️ Sometimes it is a quiet message, a remembered detail, a patient conversation, or simply staying when leaving would be easier.",

"I found something beautiful in you that I cannot quite describe. ❤️ Maybe it is your smile. Maybe it is your heart. Maybe it is the way you make me feel. Maybe it is all of it.",

"Some people are chapters. Some are paragraphs. ❤️ You feel like a story I don't want to reach the final page of.",

"I don't know what tomorrow holds. ❤️ But if tomorrow includes another conversation with you, another laugh, or another moment beside you, then I already have something to look forward to.",

"If my heart had a favorite place, I think it would be wherever you are. ❤️",

"Your smile is a little piece of peace. ❤️ Your voice is a familiar comfort. Your presence is something I never want to take for granted.",

"I could write your name across every page and still not explain what you mean to me. ❤️ So instead, I will keep showing you in every way I can.",

"Between yesterday's memories and tomorrow's dreams, there is today. ❤️ And today I simply want you to know that I love you.",

"You are not just someone I think about. ❤️ You are someone I feel connected to, someone whose happiness matters to me, someone I want beside me through more chapters of life.",


# =========================================================
# FLIRTY
# =========================================================

"I was trying to focus today, but then I thought about you. ❤️ Honestly, you are becoming a serious threat to my productivity.",

"I don't know what is more dangerous: your smile or the effect it has on me. ❤️ Either way, I am not complaining.",

"If you were here right now, I would probably spend more time looking at you than talking to you. ❤️",

"You have a talent for getting into my head without even trying. ❤️ And once you're there, you are extremely difficult to get out.",

"I hope you know that you are ridiculously attractive to me. ❤️ I could probably stare at you longer than I should.",

"Sometimes I read your messages twice. ❤️ Not because I didn't understand them, but because I like seeing your words again.",

"You really should stop being so tempting. ❤️ Or at least give me a warning before you make me miss you this much.",

"I have a confession. ❤️ Sometimes I imagine you sitting next to me and wonder how long I could behave normally.",

"You're the kind of person who makes innocent conversations feel slightly dangerous. ❤️",

"I was going to send you something sweet, but then I remembered how attractive you are and my thoughts took another direction. ❤️",

"If I were next to you right now, I have a feeling we would spend very little time actually watching whatever was on the screen. ❤️",

"You have no idea how easily you can make me smile. ❤️ And you probably have even less idea how easily you can make me miss you.",

"I like your personality. I like your smile. I like your voice. ❤️ And yes, I definitely like the way you look too.",

"Every time I see you, I understand why my self-control disappears so quickly. ❤️",

"I wonder if you realize how attractive you are when you are simply being yourself. ❤️",

"You make being patient extremely difficult. ❤️ Sometimes I just want you close.",

"I hope you are prepared for the fact that I plan on flirting with you for a very long time. ❤️",

"If I could choose where I was right now, I would probably choose somewhere very close to you. ❤️",

"You have a very unfair combination of being adorable and incredibly attractive. ❤️ I don't know how I'm supposed to handle that.",

"I miss you in a way that starts innocent and somehow becomes much less innocent the longer I think about you. ❤️",


# =========================================================
# NASTY / SENSUAL
# =========================================================

"I probably shouldn't tell you exactly what crosses my mind when I imagine you close to me. ❤️ Let's just say my thoughts are not always as innocent as my messages.",

"Sometimes I imagine pulling you closer, looking into your eyes, and forgetting about everything else for a while. ❤️",

"There is something about being close to you that makes my imagination behave badly. ❤️ And honestly, I don't think I want to fix that.",

"I miss the kind of closeness where talking becomes unnecessary. ❤️ Sometimes I just want you beside me, close enough that neither of us needs to explain what we are feeling.",

"If you were beside me right now, I have a feeling the distance between us would disappear very quickly. ❤️",

"You have this effect on me that starts with a smile and somehow turns into thoughts I probably shouldn't send in a normal conversation. ❤️",

"I love the sweet side of you, but I also love the side that knows exactly how to make my heart race. ❤️",

"Sometimes I want to be close enough to you that the rest of the world becomes irrelevant. ❤️ Just you, me, and a little privacy.",

"I can behave myself when I have to. ❤️ The problem is that when I think about you, I don't always want to.",

"I wonder how long we could sit next to each other before one of us stopped pretending to behave. ❤️",

"You make it very difficult to keep my thoughts completely innocent. ❤️ I blame you for that.",

"I don't just miss talking to you. ❤️ Sometimes I miss the closeness, the tension, the looks, and everything that happens when two people really want each other.",

"There is a particular kind of silence I like with you. ❤️ The kind where neither person needs to say what they are thinking because the look already says enough.",

"I could tell you exactly what I want right now, but I think making you wonder is more fun. ❤️",

"You have a way of making a simple moment feel charged. ❤️ One look from you can completely change the atmosphere.",

"I like being sweet with you. ❤️ But I also like that little spark between us that makes everything feel more exciting.",

"I sometimes imagine having you close and simply taking my time enjoying the moment. ❤️ No rushing, no distractions, just us.",

"You are incredibly tempting. ❤️ I can be patient, but you definitely make patience difficult.",

"Some thoughts about you belong in a private conversation. ❤️ Let's just say they are considerably less innocent than the ones I usually send.",

"If chemistry could be measured, I think we would have a serious problem. ❤️",

"I love the anticipation before seeing you. ❤️ That feeling of knowing I am about to be close to someone I find incredibly attractive.",

"Sometimes I want to whisper something into your ear just to see the expression on your face. ❤️",

"You have a dangerous combination of sweetness and temptation. ❤️ I honestly don't know which side I like more.",

"I want the kind of closeness where a look can say everything. ❤️ Where a little tension makes both of us smile.",

"I don't need anything extravagant. ❤️ Give me privacy, time with you, and that look you give me when you know exactly what you're doing.",

"I think you know exactly how attractive you are. ❤️ And I think you secretly enjoy watching me try to keep my composure.",

"I like the innocent conversations we have. ❤️ But I also like knowing there is something underneath them that only we understand.",

"You make me want to forget what time it is. ❤️ Some moments with you deserve to last much longer than they probably should.",

"I could spend hours simply being close to you. ❤️ The talking would be nice, but the quiet moments would probably be even better.",

"There is something incredibly attractive about wanting someone and knowing they want you too. ❤️",

"I don't want every moment with you to be innocent. ❤️ Some moments should have a little tension, a little teasing, and a lot of chemistry.",

"You are the kind of temptation I would willingly choose again. ❤️",

"I have a feeling that if we had an entire evening alone together, we would find plenty of ways to keep ourselves entertained. ❤️",

"I like when you make me wonder what you are thinking. ❤️ Especially when I suspect your thoughts are just as mischievous as mine.",

"Sometimes the best flirting is simply being close enough to feel the tension. ❤️",

"I want to be close enough to you that even a quiet moment feels exciting. ❤️",

"You make my imagination work overtime. ❤️ And I can't decide whether I should apologize or thank you.",

"I love the way attraction can make two people suddenly become very aware of every little movement. ❤️",

"One day I want a moment with you where we completely forget our phones, our schedules, and everything else around us. ❤️",

"You are sweet enough to make me fall for you and tempting enough to make me lose my train of thought. ❤️",

"I don't know what is more addictive: talking to you or imagining what it would be like to have you close. ❤️",

"I like the innocent smile you give me when you know perfectly well what you are doing to my thoughts. ❤️",

"You can call me sweet, but you should know there is another side of me that only comes out around you. ❤️",

"If I ever look at you for a little too long, just know I probably have several thoughts happening at once. ❤️",

"I love the tension between wanting to say something and deciding to make you guess instead. ❤️",

"Sometimes I want to hold you close and simply enjoy the feeling of having you there. ❤️",

"You are one of the few people who can make my heart race without even touching me. ❤️",

"I think the best kind of attraction is the kind where both people know exactly what is happening but neither one says it immediately. ❤️",

"You have a way of making ordinary closeness feel anything but ordinary. ❤️",

"I want more moments with you that start sweet and end with both of us smiling at how much chemistry there is between us. ❤️",

"You are dangerously good at making me want you closer. ❤️",

"I like you sweet. I like you playful. And I definitely like you when there is a little tension between us. ❤️",

"Sometimes I wonder what would happen if we stopped trying to behave and simply followed the chemistry. ❤️",

"I love that I can miss you emotionally and physically at the same time. ❤️",

"You are the kind of person I could spend an entire evening teasing and still want more time with. ❤️",

"I don't need to say everything I am thinking. ❤️ Sometimes the fun is letting you figure it out.",

"I have a feeling that if we were alone together right now, neither of us would be in a hurry to leave. ❤️",

"You make my imagination dangerous, my heart soft, and my self-control questionable. ❤️",

"I want to be the person who makes you feel beautiful, desired, safe, and completely comfortable being yourself. ❤️",

"I love the way desire and affection can exist together. ❤️ With you, I don't just want you; I genuinely care about you.",

"You can be sweet to me all you want. ❤️ Just don't be surprised when my thoughts become a little less innocent afterward.",


# =========================================================
# MORE ROMANTIC / LONG-FORM
# =========================================================

"Today I was thinking about how strange and beautiful it is that one person can slowly become such an important part of your life. ❤️ You started as someone I wanted to know, and somewhere along the way you became someone I genuinely care about, someone I miss, someone I think about, and someone whose happiness matters to me.",

"I don't want to take your presence for granted. ❤️ People sometimes become so familiar that they forget to appreciate them. I never want that to happen with you. I want to keep noticing the little things, keep listening to your stories, keep laughing at your jokes, and keep appreciating the person you are.",

"If I could sit beside you today, I wouldn't necessarily need some huge plan. ❤️ I would be happy simply sitting there, talking about random things, laughing about something stupid, sharing food, listening to music, or doing absolutely nothing. Sometimes being with the right person is the whole plan.",

"I hope there comes a time when you look back at the life we have shared and realize how many small moments became beautiful memories. ❤️ The random conversations, unexpected laughs, little disagreements, quiet evenings, and all the ordinary moments that nobody else would understand but us.",

"I want you to know something simple today. ❤️ You don't have to impress me. You don't have to always be happy. You don't have to have everything figured out. You can simply be yourself, and I will still find plenty of reasons to love you.",

"Every relationship has moments that are exciting and moments that are ordinary. ❤️ I think the real beauty is finding someone whose company you enjoy in both. With you, I don't need every day to be an adventure. Sometimes I just want another day with you.",

"When I imagine happiness, I don't imagine perfection. ❤️ I imagine laughing with someone I love, being able to talk honestly, feeling understood, having someone to come home to, and knowing that even when life becomes difficult, we still choose each other.",

"I hope you know that I don't only love the easy parts of you. ❤️ I care about the complicated parts too. The things you worry about, the things you overthink, the things you don't always know how to explain. I want to understand them rather than run away from them.",

"You are one of those people who makes me want to slow down and appreciate life. ❤️ There is something beautiful about having someone whose presence makes an ordinary moment feel worth remembering.",

"If I could send you one feeling today, I would send you the feeling of being completely loved and appreciated. ❤️ I would want you to feel no doubt about your value, no doubt about your place in my heart, and no doubt that there is someone who genuinely cares about you.",

"I don't know how many messages I will send you over the years, but I hope I never get tired of reminding you that I love you. ❤️ Some things deserve to be repeated even when the person already knows them.",

"Maybe I don't always express everything perfectly. ❤️ Maybe sometimes I joke when I should be serious or stay quiet when I should speak. But underneath all of that is something very simple: I care about you more than I know how to explain.",

"I want to make memories with you that don't need photographs to be remembered. ❤️ The kind that stay in your mind because of how they felt. A laugh that lasted too long. A conversation that changed something. A quiet moment that somehow meant everything.",

"You have become part of the way I imagine my future. ❤️ Not because I know exactly what the future will look like, but because when I think about the people I want around me, your face naturally appears.",

"I hope we keep growing together. ❤️ I want us to learn each other better, communicate better, laugh more, forgive faster, appreciate more, and never become too comfortable to stop telling each other how much we matter.",

"There is something comforting about knowing that I can think of you at any moment. ❤️ You are a familiar thought in a world that changes constantly, and somehow that makes everything feel a little more stable.",

"I don't need you to be perfect. ❤️ I need you to be honest, genuine, caring, and willing to keep choosing us. Those things mean more to me than perfection ever could.",

"Sometimes I wonder what you were doing before I knew you. ❤️ Then I realize I am simply grateful that our paths eventually crossed. Whatever happened before, I am happy that you are part of my life now.",

"I hope you always feel comfortable telling me what you need. ❤️ Whether you need space, affection, a conversation, reassurance, laughter, or simply someone beside you, I want you to know that you can tell me.",

"One of the things I love most about you is that you make me want to give more of myself. ❤️ More patience, more affection, more time, more attention, and more effort. You make love feel worth investing in.",

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
            "❤️ Love Reminder Bot is online.\n\n"
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
            "❤️ Hey.\n\n"
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
            "Only the owner can create a connection code."
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
        "❤️ CONNECTION CODE\n\n"
        f"Your code is:\n\n"
        f"{code}\n\n"
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
            "There is no active connection code right now."
        )

        return

    if entered_code != saved_code:

        await update.message.reply_text(
            "The connection code is invalid."
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

    data["connect_code"] = None

    save_data(data)

    await update.message.reply_text(
        "❤️ You're connected.\n\n"
        "You'll now receive a daily love reminder.\n\n"
        "No action is needed from you."
    )

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
            "Owner only."
        )

        return

    data = load_data()

    recipients = data.get("recipients", {})

    if not recipients:

        await update.message.reply_text(
            "No recipients connected yet."
        )

        return

    lines = ["❤️ RECIPIENTS", ""]

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

async def remove(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not is_owner(update):

        await update.message.reply_text(
            "Owner only."
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
            "Recipient not found."
        )

        return

    removed = data["recipients"].pop(user_id)

    save_data(data)

    await update.message.reply_text(
        f"Removed {removed.get('name', 'recipient')}."
    )


# =========================================================
# TEST
# =========================================================

async def test(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not is_owner(update):

        await update.message.reply_text(
            "Owner only."
        )

        return

    data = load_data()

    recipients = data.get("recipients", {})

    if not recipients:

        await update.message.reply_text(
            "No recipients connected."
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
        f"❤️ Test message sent to {sent} recipient(s)."
    )


# =========================================================
# DAILY MESSAGE
# =========================================================

async def send_daily_messages(
    context: ContextTypes.DEFAULT_TYPE
):

    data = load_data()

    if data.get("paused"):

        logger.info(
            "Daily messages are paused."
        )

        return

    recipients = data.get(
        "recipients",
        {}
    )

    if not recipients:

        logger.info(
            "No recipients."
        )

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

async def pause(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not is_owner(update):

        await update.message.reply_text(
            "Owner only."
        )

        return

    data = load_data()

    data["paused"] = True

    save_data(data)

    await update.message.reply_text(
        "Daily messages are paused."
    )


# =========================================================
# RESUME
# =========================================================

async def resume(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not is_owner(update):

        await update.message.reply_text(
            "Owner only."
        )

        return

    data = load_data()

    data["paused"] = False

    save_data(data)

    await update.message.reply_text(
        "Daily messages are active again."
    )


# =========================================================
# TIME
# =========================================================

async def set_time(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not is_owner(update):

        await update.message.reply_text(
            "Owner only."
        )

        return

    if not context.args:

        data = load_data()

        await update.message.reply_text(
            "Current time: "
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
            "Invalid time.\n\n"
            "Use:\n"
            "/time 21:00"
        )

        return

    data = load_data()

    data["hour"] = hour

    data["minute"] = minute

    save_data(data)

    schedule_daily_job(
        context.application
    )

    await update.message.reply_text(
        f"❤️ Daily message time changed to "
        f"{hour:02d}:{minute:02d} Ethiopia time."
    )


# =========================================================
# STATUS
# =========================================================

async def status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not is_owner(update):

        await update.message.reply_text(
            "Owner only."
        )

        return

    data = load_data()

    recipients = data.get(
        "recipients",
        {}
    )

    paused = data.get(
        "paused",
        False
    )

    hour = data.get(
        "hour",
        DEFAULT_HOUR
    )

    minute = data.get(
        "minute",
        DEFAULT_MINUTE
    )

    await update.message.reply_text(
        "❤️ LOVE BOT STATUS\n\n"
        f"Recipients: {len(recipients)}\n"
        f"Daily time: {hour:02d}:{minute:02d}\n"
        f"Timezone: Ethiopia\n"
        f"Status: {'Paused' if paused else 'Active'}"
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

    logger.info(
        "Starting Love Reminder Bot..."
    )

    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CommandHandler(
            "connect",
            connect
        )
    )

    application.add_handler(
        CommandHandler(
            "join",
            join
        )
    )

    application.add_handler(
        CommandHandler(
            "list",
            list_recipients
        )
    )

    application.add_handler(
        CommandHandler(
            "remove",
            remove
        )
    )

    application.add_handler(
        CommandHandler(
            "test",
            test
        )
    )

    application.add_handler(
        CommandHandler(
            "pause",
            pause
        )
    )

    application.add_handler(
        CommandHandler(
            "resume",
            resume
        )
    )

    application.add_handler(
        CommandHandler(
            "time",
            set_time
        )
    )

    application.add_handler(
        CommandHandler(
            "status",
            status
        )
    )

    application.add_error_handler(
        error_handler
    )

    schedule_daily_job(
        application
    )

    logger.info(
        "Bot is running."
    )

    application.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
