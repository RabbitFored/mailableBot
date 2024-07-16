from pyrogram import filters, Client

@Client.on_message(filters.command(["sponsors"]))
async def sponsors(client, message):
    text = strings.get("sponsor_txt")
    await message.reply_text(text, 
                             quote=True, 
                             disable_web_page_preview=True)