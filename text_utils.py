import re
from aiogram import types

# ANSI EFFECT CODE
ansi_effect = {
    'break': '\033[0m',
    'bold': '\033[1m',
    'fade': '\033[2m',
    'italic': '\033[3m',
    'underline': '\033[4m',
    'rflash': '\033[5m',
    'fflash': '\033[6m',
    'cbgtx': '\033[7m',
    'crossout': '\033[8m',
    'dunderline': '\033[21m',
    'framed': '\033[51m',
    'circled': '\033[52m',
    'overlined': '\033[53m',
}

# ANSI COLOR CODE
ansi_color = {
    'black': {
        'text': '\033[30m',
        'background': '\033[40m',
    },
    'red': {
        'text': '\033[31m',
        'background': '\033[41m',
    },
    'green': {
        'text': '\033[32m',
        'background': '\033[42m',
    },
    'yellow': {
        'text': '\033[33m',
        'background': '\033[43m',
    },
    'blue': {
        'text': '\033[34m',
        'background': '\033[44m',
    },
    'purple': {
        'text': '\033[35m',
        'background': '\033[45m',
    },
    'turquoise': {
        'text': '\033[36m',
        'background': '\033[46m',
    },
    'white': {
        'text': '\033[37m',
        'background': '\033[47m',
    },
}


def logging(message: types.Message,
            type_content: str,
            content: str) -> None:
    """
    Procedure for logging actions with the bot to the console.
    :param message: message object
    :param type_content: str name type content
    :param content: str content
    :return: None
    """
    log = '{}{}[{}]{} in {}{}{} send {}{}{}: \n{}{}{}\n'.format(ansi_color['blue']['text'] + ansi_effect['bold'],
                                                                message.from_user.username,
                                                                message.from_user.id,
                                                                ansi_effect['break'] + ansi_color['blue']['text'],
                                                                ansi_color['yellow']['text'],
                                                                message.date,
                                                                ansi_effect['break'] + ansi_color['blue']['text'],
                                                                ansi_color['yellow']['text'],
                                                                type_content,
                                                                ansi_effect['break'] + ansi_color['blue']['text'],
                                                                ansi_color['turquoise']['text'] + ansi_effect['italic'],
                                                                content,
                                                                ansi_effect['break'])
    with open('logging.log', 'a', encoding="utf-8") as logfile:
        logfile.writelines(re.sub(r'\033\[\d+m', r'', log))  # Logging message in logfile
    print(log)  # Logging message in console
