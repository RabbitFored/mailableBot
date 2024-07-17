from bot import bot, web
import os
from bot.core.utils import strip_script_tags
from quart import render_template

@web.route('/inbox/<user>/<id>')
async def inbox(user, id):
  print(user, id)
  m = await bot.get_messages(int(user), int(id))
  file = await m.download()
  f = open(file, "r")
  content = f.read()
  nojs = strip_script_tags(content)
  os.remove(file)
  return await render_template("inbox.html" , content = nojs)
  