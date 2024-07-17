from pyrogram import Client, filters
from bot.core import database as db
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from bot.core import utils


@Client.on_message(filters.command(["adddomain"]))
async def adddomain(client, message):
    user = db.get_user(message.from_user.id)

    if not user.subscription["name"] == "premium":
        await message.reply("You don't have a premium subscription.",
                            reply_markup=(InlineKeyboardMarkup([[
                                InlineKeyboardButton(text="Upgrade",
                                                     callback_data="upgrade")
                            ]])))
        return

    domain = await message.chat.ask('Send me your domain name')
    mail_servers = utils.get_mx_server(domain.text)

    if "mx.bruva.co" in mail_servers:
        status = "▶"
        await message.reply("Domain verified")
        data = {"domains": domain.text}
        user.data.addToSet(message.from_user.id, data)
    else:
        status = "❌"
        text = f'''
Pending verification for {domain.text}

Add MX Record:
`mx.bruva.co`  {status}
'''
        await message.reply(text,
                            reply_markup=(InlineKeyboardMarkup([[
                                InlineKeyboardButton(
                                    text="Check Status",
                                    callback_data=f"chstatus_{domain.text}")
                            ]])))
