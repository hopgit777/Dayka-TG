import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = '7640723426:AAHW_rDRNzIFpez46VcMHyBL6rm5ataBgRg'
bot = telebot.TeleBot(BOT_TOKEN)

CHANNELS = {
    '@DM_Servers': 'https://t.me/DM_Servers',
    '@echobass_707': 'https://t.me/echobass_707',
    '@Lion_Servers': 'https://t.me/Lion_Servers',
    '@DM_404Chat': 'https://t.me/DM_404Chat'
}

@bot.message_handler(commands=['start'])
def start(m):
    markup = InlineKeyboardMarkup(row_width=2)
    for i, (ch, url) in enumerate(CHANNELS.items(), 1):
        markup.add(InlineKeyboardButton(f'KANAL {i}', url=url))
    markup.add(InlineKeyboardButton('✅ Agza boldum', callback_data='check_subs'))
    bot.send_message(m.chat.id, "Salam! Kod almak üçin aşakdaky kanallara agza boluň:", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == 'check_subs')
def check_subs(c):
    user_id = c.from_user.id
    not_joined = []
    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status not in ['member', 'creator', 'administrator']:
                not_joined.append(ch)
        except Exception as e:
            print(f"Hata {ch}: {e}")
            not_joined.append(ch)

    if not_joined:
        text = "🚫 Siz heniz şu kanallara agza bolmadyňyz:\n" + "\n".join(not_joined)
        bot.send_message(c.message.chat.id, text)
        bot.answer_callback_query(c.id, "Kanalara agza boluň!")
    else:
        bot.send_message(c.message.chat.id, "✅ Siz ähli kanallara agza bolduňyz! Ine siziň kodyňyz: ABC123", parse_mode='Markdown')
        bot.answer_callback_query(c.id, "Agzaçylyk barlandy!")

@bot.message_handler(commands=['checkme'])
def checkme(message):
    user_id = message.from_user.id
    results = []
    for ch in CHANNELS:
        try:
            member = bot.get_chat_member(ch, user_id)
            results.append(f"{ch}: {member.status}")
        except Exception as e:
            results.append(f"{ch}: Hata - {e}")

    bot.send_message(message.chat.id, "\n".join(results))

import time

if name == 'main':
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(f"Hata: {e}")
            time.sleep(5)
