from pyrogram import Client, filters

from bot import CONFIG, strings
from bot.core import filters as fltr
from bot.core.utils import generate_keyboard
from bot.core import database as db

@Client.on_message(filters.private & ~ filters.me , group=-100)
async def user_load(client, message):
    userID = message.from_user.id
    user = await db.get_user(userID, fetch_info=True)
    if not user:
        await db.add_user(message)
    else:
        await user.refresh(message)
    message.continue_propagation()
    
@Client.on_message(fltr.cmd(["start"]))
async def start(client, message):
    text = strings.get("start_txt", user=message.from_user.mention)
    keyboard = generate_keyboard(strings.get("start_btn"))

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        reply_markup=keyboard,
        quote=True,
    )


@Client.on_message(filters.command(["help"]))
async def get_help(client, message):
    group_url = CONFIG.settings["links"]["group_url"]

    text = strings.get("help_txt")
    keyboard = generate_keyboard(strings.get("help_btn", group_url=group_url))

    # extended help message for bot administrator
    chatID = message.chat.id
    admins = CONFIG.get_group("admin")

    if chatID in admins:
        text += "\n\n" + strings.get("admin_help_txt")
    if message.from_user.is_self:
        await message.edit(text,
                           reply_markup=keyboard,
                           disable_web_page_preview=True)
    else:
        await message.reply_text(text,
                                 reply_markup=keyboard,
                                 quote=True,
                                 disable_web_page_preview=True)


@Client.on_message(filters.command(["about"]))
async def aboutTheBot(client, message):
    channel_url = CONFIG.settings["links"]["channel_url"]
    group_url = CONFIG.settings["links"]["group_url"]

    text = strings.get("about_txt", name = client.me.first_name)
    keyboard = generate_keyboard(
        strings.get("about_btn", channel_url=channel_url, group_url=group_url))

    await message.reply_text(text,
                             reply_markup=keyboard,
                             quote=True,
                             disable_web_page_preview=True)


@Client.on_message(filters.command(["donate"]))
async def donate(client, message):
    repo_url = CONFIG.settings["links"]["repo_url"]
    donation_url = CONFIG.settings["links"]["donation_url"]
   
    text = strings.get("donate_txt")
    keyboard = generate_keyboard(strings.get("donate_btn",repo_url=repo_url, donation_url=donation_url))

    await message.reply_text(text,
                             reply_markup=keyboard,
                             quote=True,
                             disable_web_page_preview=True)
