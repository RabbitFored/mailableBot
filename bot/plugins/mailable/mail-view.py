import os
import tempfile

import aiofiles
from quart import render_template

from bot import bot, web, logger
from bot.core.utils import strip_script_tags


@web.route("/inbox/<user>/<id>")
async def inbox(user, id):
    try:
        with tempfile.TemporaryDirectory(prefix=f"{int(user)}_") as temp_dir:
            media = await bot.get_messages(int(user), int(id))
            temp_file_path = os.path.join(temp_dir, f"mail_{id}")
            await media.download(temp_file_path)
            async with aiofiles.open(temp_file_path, "r") as temp_file:
                content = await temp_file.read()
                nojs = strip_script_tags(content)
                await temp_file.close()
                return await render_template("inbox.html", content=nojs)
    except Exception as e:
        try:
           await bot.send_message(int(user), "File not found")
        except:
            pass
        logger.error(f"Something went wrong while viewing mails, {e}")
        return "File not found"