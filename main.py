import logging
from telegram.ext.dispatcher import run_async
#from telegram import ext
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from tool import price,balance

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error


def validating_group(data):
  message = data['message']
  chat = message['chat']['username']
  if chat == 'Appics_Bangladesh':
    return True
  else:
    return False



@run_async
def balanc(bot, update, args):
    usr_chat_id = update.message.chat_id
    if validating_group(update):
        if len(args) == 1:
            user_name = args[0]
            response = balance(user_name)
            
            if response is not None:
                usr_name = update.message.from_user.first_name
                if update:
                    usr_command = str(update.effective_message.text) if update.effective_message.text else 'None'
                    if update.message.from_user.last_name:
                        usr_name += ' ' + update.message.from_user.last_name
                    if update.message.from_user.username:
                        usr_name += ' (@' + update.message.from_user.username + ')'
                text_response = "{0}'s Current\n{1}".format(user_name,response)
                bot.send_message(usr_chat_id, text_response, parse_mode="Markdown")
            else:
                bot.send_message(usr_chat_id,'Please Check the Username')

        else:
            bot.send_message(usr_chat_id, 'Please check your username ,remember you should not put "@" at starting your username', parse_mode="Markdown")
    else:
        bot.send_message(usr_chat_id,text='You Must Send Command From @Appics_Bangladesh Group')


def help(bot,update):
    usr_chat_id = update.message.chat_id
    response = 'This bot just help you to view Appics balance\nTo know your balance just send:\n/b yourusername'
    bot.send_message(usr_chat_id,response)

@run_async
def pric(bot, update, args):
    usr_chat_id = update.message.chat_id
    if validating_group(update):
        if len(args) == 2:
            count = args[0]
            symble = args[1]
            response = price(symble)
            total_steemp = None
            if response is not None:
                total_steemp = response*float(count)
            data = "{0} {1}'s Current price {2} Steemp".format(count,symble,total_steemp)
            if response is not None:
                usr_name = update.message.from_user.first_name
                if update:
                    usr_command = str(update.effective_message.text) if update.effective_message.text else 'None'
                    if update.message.from_user.last_name:
                        usr_name += ' ' + update.message.from_user.last_name
                    if update.message.from_user.username:
                        usr_name += ' (@' + update.message.from_user.username + ')'
                text_response = data
                bot.send_message(usr_chat_id, text_response, parse_mode="Markdown")
            else:
                bot.send_message(usr_chat_id,'Please Check the Command')
        else:
            bot.send_message(usr_chat_id, 'Please check format to check price send:/p <numberoftoken> <tokenname> ', parse_mode="Markdown")
    else:
        bot.send_message(usr_chat_id,text='You Must Send Command From @Appics_Bangladesh Group')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("918986642:AAGHCRf82dAxuzKJwqwVdpu9tdcGDKRLC54", use_context=False)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('b',balanc,pass_args=True))
    dp.add_handler(CommandHandler('p',pric,pass_args=True))

    # log all errors
    #dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    print('Bot jsut started')
    main()