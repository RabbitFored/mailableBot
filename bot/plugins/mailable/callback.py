from pyrogram import Client
from bot.core import filters as fltr
import importlib
from bot import strings
from bot.core.utils import generate_keyboard
from bot.core import database as db
from .actions import transfer_mail

@Client.on_callback_query(fltr.on_marker("info"))
async def mail_info(client, query):
    mailID = query.data.split("_")[1]
    text = strings.get("mail_info_txt",
                            mailID=mailID,
                            owner=query.message.reply_to_message.from_user.mention() )
    btn = strings.get("mail_info_action_btn", mailID=mailID)
    print(btn)
    keyboard = generate_keyboard(btn)
    await query.message.edit(text, reply_markup=keyboard)


@Client.on_callback_query(fltr.on_marker("dl"))
async def dl_mail(client, query):
        await query.answer()
        mailID = query.data.split("_")[1]
        user = db.get_user(query.message.reply_to_message.from_user.id)
        user.data.rm({"mails": mailID})
        await query.message.edit_text("**Mail deleted successfully**")

@Client.on_callback_query(fltr.on_marker("tr"))
async def tr_mail(client, query):
        mailID = query.data.split("_")[1]
        await transfer_mail(client, query.message, mailID)