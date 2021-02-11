from telegram.ext.dispatcher import run_async
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,ConversationHandler,CallbackQueryHandler,InlineQueryHandler
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,InputTextMessageContent,InlineQueryResultArticle
import logging
import os
import unshortenit
from unshortenit import UnshortenIt
import pyshorteners
import re
from uuid import uuid4


Api_key=os.environ.get("api_key","df873189c1a48c8faf7a0dac0849040c84c0fa1a")
s=pyshorteners.Shortener(api_key=Api_key)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

@run_async
def start(update,context):
    first=update.message.chat.first_name
    update.message.reply_text('Hi! '+str(first)+' \n\nWelcome to Url Shortener Bot\n\n 🔌This Bot Was Made By: @levi_dev \n\n 💡Send Any Url Below Make Sure The Url Starts With http:// or https://.')



@run_async
def convert(update,context):
    global link
    link=update.message.text
    pattern1="https://*"
    pattern2="http://*"
    if(re.search(pattern1,link)) or (re.search(pattern2,link)):
        keyboard = [[InlineKeyboardButton("Short", callback_data='short'),InlineKeyboardButton("Unshort", callback_data='unshort')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('You Want Short The Url Or Unshort?', reply_markup=reply_markup)
    else:
        update.message.reply_text("<i>⚠💡 Url must start with http:// or https://.</i>",parse_mode=telegram.ParseMode.HTML)

@run_async
def button(update,context):
    query=update.callback_query
    query.answer()
    a=query.data
    if a=="unshort":
        unshortener=UnshortenIt()
        uri=unshortener.unshorten(link)
        query.edit_message_text(text="Unshorted url 👇🏼 : \n"+str(uri))
    if a=="short":
        response=s.bitly.short(link)
        query.edit_message_text("Shorted url 👇🏼:\n"+str(response))


def inlinequery(update,context):
	query = update.inline_query.query
	###for short links#######
	shortlink=s.bitly.short(query)
	#####for unshort link####$#$
	unshortener=UnshortenIt()
	unshortlink=unshortener.unshorten(query)
	
	results=[InlineQueryResultArticle(id=uuid4(),title="short",input_message_content=InputTextMessageContent(shortlink), description="Click to shorten the link"),
                     InlineQueryResultArticle(id=uuid4(),title="unshort",input_message_content=InputTextMessageContent(unshortlink), description="Click to unshort the link")]
	update.inline_query.answer(results)
		
def donate(update,context):
    update.message.reply_text("You can support me by donating any amount you with crypto: TRX: TCkjMWYRihFDEZnLeiCZYAXXJPRWUHzA9J)\n\n",parse_mode=telegram.ParseMode.MARKDOWN_V2)
	
def buy(update,context):
    update.message.reply_text("🔌Contact: @levi_dev 💡For Buying)\n\n",parse_mode=telegram.ParseMode.MARKDOWN_V2)	


def main():
    token=os.environ.get("bot_token","1679153860:AAGSr7XSeGUm4894zm6pMzMjGIk3CYDo3iU")
    updater = Updater(token,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('buy',buy))
    dp.add_handler(CommandHandler('donate',donate))
    dp.add_handler(MessageHandler(Filters.text,convert))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(InlineQueryHandler(inlinequery))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
