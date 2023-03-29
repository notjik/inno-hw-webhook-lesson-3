"""
Добавить в бота реализацию работы с SQLite.
"""
# *You need to download: "aiogram", "python-dotenv"*
# *You need to add a token, host, path to the environment variable*

# Imports for working with a bot
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions
from dotenv import load_dotenv
from text_utils import ansi_color, ansi_effect, logging
from db import Database

# Loading environment variables
load_dotenv()

# Unloading local variables and initializing the bot
try:
    WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
    WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
    WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH
    WEBAPP_HOST = os.getenv('WEBAPP_HOST')
    WEBAPP_PORT = os.getenv('WEBAPP_PORT')
    bot = Bot(token=os.getenv('TOKEN'))
except TypeError:
    exit('Create local variables')
dispatcher = Dispatcher(bot)


async def startup(callback):
    """
    Logging the launch of the bot

    :param callback: dispatcher object
    :return: None
    """
    global db
    table_template = {
        'users': [
            {
                'name': 'id',
                'desc': 'integer primary key autoincrement not null',
            },
            {
                'name': 'userid',
                'desc': 'integer unique',
            },
            {
                'name': 'username',
                'desc': 'text',
            },
            {
                'name': 'firstname',
                'desc': 'text',
            },
            {
                'name': 'lastname',
                'desc': 'text',
            }
        ]
    }
    db = Database('webhook-3.db', table_template)
    me = await callback.bot.get_me()  # Request information about the bot
    print('{}The {}{}[{}]{} has been successfully launched.{}\n'.format(
        ansi_color['green']['text'],
        ansi_effect['bold'],
        me.username, me.id,
        ansi_effect['break'] + ansi_color['green']['text'],
        ansi_effect['break']))  # Logging message
    await bot.set_webhook(WEBHOOK_URL)


async def shutdown(callback):
    """
    Logging off the bot

    :param callback: dispatcher object
    :return: None
    """
    global db
    me = await callback.bot.get_me()  # Request information about the bot
    del db
    print('\n{}The {}{}[{}]{} is disabled.{}'.format(
        ansi_color['green']['text'],
        ansi_effect['bold'],
        me.username, me.id,
        ansi_effect['break'] + ansi_color['green']['text'],
        ansi_effect['break']))  # Logging message
    await bot.delete_webhook()


@dispatcher.message_handler(commands=['start'])
async def start_message(msg: types.Message):
    """
    The starting message of the bot

    :param msg: message object
    :return: answer
    """
    global db
    elems = {
        'userid': msg.from_user.id,
        'username': msg.from_user.username,
        'firstname': msg.from_user.first_name,
        'lastname': msg.from_user.last_name,
    }
    db.add('users', elems)
    logging(msg, '/start', '{}'.format(msg))
    await msg.answer('Hi! Welcome to the bot from the webhooks homework №2 of Innopolis University. \n'
                     'This is an echo bot.')  # Request with a message to the user


@dispatcher.message_handler(commands=['help'])
async def help_message(msg: types.Message):
    """
    The help message of the bot

    :param msg: message object
    :return: answer
    """
    logging(msg, '/help', '{}'.format(msg))
    await msg.answer("Just send me a message and I'll repeat it!")  # Request with a message to the user


@dispatcher.message_handler(content_types=['any'])
async def echo(msg: types.Message):
    """
    Echo function.

    :param msg: message object
    :return: send message
    """
    logging(msg, msg.content_type, '{}'.format(msg))  # Calling the logger
    await bot.copy_message(chat_id=msg.chat.id,
                           from_chat_id=msg.chat.id,
                           message_id=msg.message_id)  # Request to copy a message


@dispatcher.errors_handler(exception=exceptions.BotBlocked)
async def except_bot_blocked(update: types.Update, exception: exceptions.BotBlocked):
    global db
    db.delete('users', conjunction={'userid': update.message.from_user.id})
    logging(update.message, 'the bot to the ban', '{}'.format(exception))
    return True


# Entry point
if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dispatcher,
        webhook_path=WEBHOOK_PATH,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
        on_startup=startup,
        on_shutdown=shutdown,
        skip_updates=True,
    )  # Launching webhook
