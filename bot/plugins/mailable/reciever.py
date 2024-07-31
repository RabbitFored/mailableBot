from bot import web, bot, CONFIG, logger
from quart import request, Response
import mailparser
from bot.core import database as db
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import os
import tempfile
import aiofiles

baseURL = CONFIG.baseURL


@web.route('/cust', methods=['POST'])
async def secretmessages():
  logger.info("new mail")
  mailbytes = await request.get_data()
  logger.info("mailbytes")
  logger.info(str(mailbytes))
  logger.info(mailbytes)
  mail = mailparser.parse_from_bytes(mailbytes)
  logger.info("mail")
  logger.info(mail)
  logger.info("data")
  data = {
      "from": mail.from_,
      "to": mail.to,
      "cc": mail.cc,
      "bcc": mail.bcc,
      "subject": mail.subject,
      "body": mail.body,
      "text": mail.text_plain,
      "html": mail.text_html,
      "reply_to": mail.reply_to,
      "message_id": mail.message_id
  }
  logger.info(data)
  content = data['html'][0] if data['html'] else data['text'][0]

  # data = json.loads((await request.form).get("data"))

  user = db.find_user({"mails": data['to'][0][1]})
  if user:
    userID = user.ID
  else:
    return "user not found"
  text = f"\
  **Sender     :** {data['from'][0][1]}\n\
  **Recipient  :** {data['to'][0][1]}\n\
  **Subject    :** {data['subject']}\n\
  **Message    :** \n...\
  "

  with tempfile.TemporaryDirectory(prefix=f"{userID}_") as temp_dir:
    temp_file_path = os.path.join(temp_dir, 'inbox.html')
    async with aiofiles.open(temp_file_path, 'w') as temp_file:
      await temp_file.write(content)
      file = await bot.send_document(chat_id=userID, document=temp_file_path)
      await file.reply(text=text,
                       reply_markup=InlineKeyboardMarkup([[
                           InlineKeyboardButton(
                               "View mail",
                               web_app=WebAppInfo(
                                   url=f"{baseURL}/inbox/{userID}/{file.id}")),
                       ]]),
                       quote=True)
  db.statial("recieved", 1)
  return Response(status=200)
