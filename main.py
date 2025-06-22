from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    CallbackQueryHandler,
)
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from dotenv import load_dotenv
import os

import json

load_dotenv()
token = os.getenv("token")

updater = Updater(token=token)
dispatcher = updater.dispatcher

with open("count.json", "r") as f:

    try:
        count = json.loads(f.read())
    except:
        count = {"like": 0, "dislike": 0}

g_dislike = count["dislike"]
d_like = count["like"]

with open("text.json", "r") as f:
    try:
        dct = json.loads(f.read())
    except:
        dct = {}


def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    bot = context.bot
    user_named=update.message.chat.username
    user_chat=str(update.message.from_user.id)
    use=update.message.from_user.first_name
    try :
        with open('user_name.json','r') as me:
            user_json=json.load(me)
    except:
        user_json={}
        if user_chat not in user_json:
            user_json[user_chat]=user_named
            with open('user_name.json','w') as write: 
                e=json.dumps(user_json)
                write.write(e)
    try:
        with open('first_name.json','r') as usage:
            used_json=json.load(usage)
    except:
            used_json={}
            if user_chat not in  used_json:
                used_json[user_chat]=use
                with open('first_name.json','w') as ser:
                    rer=json.dumps(used_json) 
                    ser.write(rer)

    
    

    keyboard1 = InlineKeyboardButton(
        f"dislike 👎 {g_dislike}", callback_data="1dislike"
    )
    keyboard2 = InlineKeyboardButton(f"like 👍 {d_like}", callback_data="1like")
    reply_markup = InlineKeyboardMarkup([[keyboard1, keyboard2]])

    bot.send_message(
        chat_id=chat_id,
        text="Hello @" + update.message.chat.username,
        reply_markup=reply_markup,
    )


def query(update: Update, context: CallbackContext):
    global g_dislike, d_like

    if update.callback_query:
        chat_id = update.callback_query.message.chat_id
        button = update.callback_query.data

        if button == "1like":
            current_choice = "like"
        elif button == "1dislike":
            current_choice = "dislike"
        else:
            return

        previous_choice = dct.get(str(chat_id), None)

        if previous_choice == current_choice:
            return

        if previous_choice == "like":
            d_like -= 1
        elif previous_choice == "dislike":
            g_dislike -= 1

        if current_choice == "like":
            d_like += 1
        else:
            g_dislike += 1

        with open("count.json", "w") as f:
            json_string = json.dumps({"like": d_like, "dislike": g_dislike})
            f.write(json_string)

        dct[str(chat_id)] = current_choice


        with open("text.json", "w") as f:
            json_string = json.dumps(dct)
            f.write(json_string)
        with open("text.json", "w") as j:
            user_json=json.dumps(dct)
            j.write(user_json)

        keyboard1 = InlineKeyboardButton(
            f"dislike 👎 {g_dislike}", callback_data="1dislike"
        )
        keyboard2 = InlineKeyboardButton(f"like 👍 {d_like}", callback_data="1like")
        reply_markup = InlineKeyboardMarkup([[keyboard1, keyboard2]])

        update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)


dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(callback=query, pattern="1"))

updater.start_polling()
updater.idle()
