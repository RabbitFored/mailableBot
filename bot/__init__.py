import sys
from quart import Quart
from pyrogram import Client

from .core import ProcessManager, logger
from .core.shared import CONFIG
from .core import Translator
#if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    logger.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

# setting up processes
ProcessManager = ProcessManager()

# Initialize bot
bot = Client("bot", api_id=CONFIG.apiID, api_hash=CONFIG.apiHASH, bot_token=CONFIG.botTOKEN, plugins= dict(root="bot/plugins"), alt_port=True)
web = Quart(__name__)
# Initialize strings
strings = Translator()

