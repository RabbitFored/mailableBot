from pyrogram import Client, filters
from mailable.core import utils
from mailable.core import database as db
from mailable.plugins.filters import group

@Client.on_message(filters.command(["whois"]) & group("admin") )
async def whois(client, message):
  args = message.text.split(" ")

  mailID = args[1]
  user = db.find_user(mailID)
  print(user.ID)
  await message.reply_text(f'Mail {mailID} belongs to `{user.ID}`')