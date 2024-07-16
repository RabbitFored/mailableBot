from pyrogram import Client, filters
from bot.core import database as db
from bot import strings, CONFIG
from bot.core.utils import generate_keyboard, gen_rand_string
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from pyrogram.enums import MessageEntityType

async def no_mails(message):
    text = strings.get("no_mails_txt")
    await message.reply_text(text, quote=True)


@Client.on_message(filters.command(["mails", "transfer", "delete"]))
async def mail_action(client, message):
    user = db.get_user(message.from_user.id)
    mailIDs = user.data.get("mails", [])

    command = message.text.split(" ")[0][1:]
    actions = {"mails": "info", "transfer": "tr", "delete": "dl"}

    if len(mailIDs) == 0:
        await no_mails(message)
        return
    text = strings.get("select_mail_txt")
    btns = ""

    for mailID in mailIDs:
        btn = strings.get("select_mail_btn",
                          mailID=mailID,
                          action=actions[command])
        btns += f"{btn}\n"
    keyboard = generate_keyboard(btns)
    await message.reply_text(text, reply_markup=keyboard, quote=True)


@Client.on_message(filters.command(["generate"]))
async def generate(client, message): 
    user = db.get_user(message.from_user.id)

    mailIDs = user.data['mails']
    limits = user.get_limits()

    if len(mailIDs) >= limits["max_mails"]:
        await message.reply(
            f"**Your plan includes reserving {limits['max_mails']} mails only.\nSwitch to premium plan to make more mails.**"
        )
        return

    domains = CONFIG.settings["extras"]["domains"]

    if user.subscription["name"] == "premium":
        user_domains = user.data.get("domains", [])
        domains = domains + user_domains

    buttons = []
    for domain in domains:
        buttons.append([InlineKeyboardButton(domain, f"{domain}")])

    k = await message.chat.ask(text="**Select a domain:**",
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(buttons))
    
    callback_query = await client.wait_for_callback_query(message.from_user.id)
    await callback_query.answer()

    domain = callback_query.data
    mailID = gen_rand_string(8).lower() + "@" + domain

    user.data.addToSet({"mails": mailID})

    await callback_query.message.reply_text(
        f"Mail Created successfully.\nYour mail id : {mailID}\nNow You can access your mails here.")
    await callback_query.message.delete()


@Client.on_message(filters.command(["set"]))
async def set_mail(client, message):
  user = db.get_user(message.from_user.id)
  mailIDs = user.data['mails']
  limits = user.get_limits()

  if len(mailIDs) >= limits["max_mails"]:
        await message.reply(
            f"**Your plan includes reserving {limits['max_mails']} mails only.\nSwitch to premium plan to make more mails.**"
        )
        return
      
  mailID = None
  for entity in message.entities:
    if entity.type == MessageEntityType.EMAIL:
      o = entity.offset
      l = entity.length
      mailID = message.text[o:o + l]
  if mailID == None:
    await message.reply_text(text="**Provide a valid mail ID.**")
    return
      
  domains = CONFIG.settings["extras"]["domains"]
  if user.subscription["name"] == "premium":
    user_domains = user.data.get("domains", [])
    domains = domains + user_domains
  
  reserved_keyword = CONFIG.settings["extras"]["reserved_keyword"]
    
  id, domain = mailID.split("@")

  if id in reserved_keyword:
    await client.send_message(message.chat.id,
                               f"**Sorry this mail ID is unavailable**")
    return


  
  if domain not in domains:
    await client.send_message(
      message.chat.id,
      f"**The domain {domain} is not maintained by us.\nUse /domains to check list of available domains.\n\nIf you are the owner of {domain} and interested to use it in this bot, contact us at @ostrichdiscussion.**"
    )
    return
  
  dataExists = db.data_exists({'mails':mailID})
  if dataExists:
        await client.send_message(message.chat.id,
                                   "Sorry this mail ID is unavailable")
        return
  user.data.addToSet({'mails':mailID})    
  await message.reply_text(
          f"Mail Created successfully.\nYour mail id : {mailID}\nNow You can access your mails here."
        )
  