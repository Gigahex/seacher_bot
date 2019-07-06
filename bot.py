import logging
import query
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
folder = os.path.join(os.getcwd(), "доверенности")
query = query.Query(folder)
 
def start(bot, update):
    keyboard = [[InlineKeyboardButton("Искать в папке?", callback_data="1")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text = "Поиск документа по ключевым словам", reply_markup=reply_markup)
 
def button(bot, update):
    query = update.callback_query
 
    bot.editMessageText(text="Введите ключевые слова через пробел",
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
 
 
def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")
 
 
def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))
def echo(bot, update):
    text = (update.message.text)
    response = query.many_text_query(text)
    if len(response) == 0:
        update.message.reply_text("К сожалению документов связанных с этими словами не нашлось")
    else:
        for filename in response:
            bot.send_photo(chat_id = update.message.chat_id, photo=open(os.path.join(folder, filename), 'rb'))
    start(bot, update)
# Create the Updater and pass it your bot's token.
updater = Updater("716346063:AAGcOzhqVcS5HkT_HR7mYpWi8895XaTopS0")
 
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))
updater.dispatcher.add_error_handler(error)
 
# Start the Bot
updater.start_polling()
 
# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT
updater.idle()