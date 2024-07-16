#from mailable import logger, CONFIG, PROCESSES
from pyrogram import filters, Client
import time
from bot.core import database as db
from bot.core import filters as fltr
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import ProcessManager
import asyncio

async def bcast(client, message):
    while True:
        await client.send_message(chat_id=message.chat.id, text="Test message")
        await asyncio.sleep(2) 

@Client.on_message(filters.command(["broadcast"]) & fltr.group("admin"))
async def broadcast(client, message):
        processes = ProcessManager.list_processes()
        for p in processes:
            if p.name == 'broadcast':
                await message.reply_text("Another broadcast is already in progress. Please try again later.")
                return
        broadcast_msg = message.reply_to_message
        if not broadcast_msg:
            await message.reply(
                "Please reply to a message to broadcast it.", quote=True
            )
            return
            
        users = db.user.fetch_all()

        keyboard = [
            [
                InlineKeyboardButton("Check Progress", callback_data="ps_broadcast"),
            ]
        ]
        await message.reply_text("Broadcasting...",                                                    reply_markup=InlineKeyboardMarkup(keyboard))

        PROCESSES.broadcast["status"] = True
        PROCESSES.broadcast["total"] = len(users)
    
        failed = 0
        x = 0
    
        mode = CONFIG.settings["broadcast"]["mode"]
        if len(message.text.split(" ")) > 1:
            mode = message.text.split(" ")[1]
        for user in users:
            try:
                if mode == "copy":
                    await broadcast_msg.copy(user)
                else:
                    await broadcast_msg.forward(user)

                x += 1
                time.sleep(2)

            except:
                failed += 1
            PROCESSES.broadcast["count"] = failed + x
        text = f"Broadcast complete. {failed} users failed to receive the message, probably due to being kicked."
        await message.reply_text(text)
        logger.info(text)
        PROCESSES.broadcast["status"] = False
