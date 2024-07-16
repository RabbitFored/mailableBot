from bot import web,bot, CONFIG
from quart import request, Response
import mailparser
from bot.core import database as db
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import os

baseURL = CONFIG.baseURL

@web.route('/cust', methods=['POST'])
async def secretmessages():
  mailbytes = await request.get_data()
  mail = mailparser.parse_from_bytes(mailbytes)

  data =  { 
    "from" : mail.from_,
    "to" : mail.to,
    "cc" : mail.cc,
    "bcc" : mail.bcc,
    "subject" : mail.subject,
    "body" : mail.body,
    "text" : mail.text_plain,
    "html" : mail.text_html,
    "reply_to" : mail.reply_to,
    "message_id" : mail.message_id
    }

  content = data['html'][0] if data['html'] else data['text'][0]

 # data = json.loads((await request.form).get("data"))
  userID = db.find_user(data['to'][0][1]).ID

  f = open("inbox.html", "w")
  f.write(str(content))
  f.close()

  text = f"\
**Sender     :** {data['from'][0][1]}\n\
**Recipient  :** {data['to'][0][1]}\n\
**Subject    :** {data['subject']}\n\
**Message    :** \n...\
"

  file = await bot.send_document(chat_id=userID, document="inbox.html")
  await file.reply(
    text=text,
    reply_markup=InlineKeyboardMarkup([[
      InlineKeyboardButton(
        "View mail",
        web_app=WebAppInfo(url=f"{baseURL}/inbox/{userID}/{file.id}")),
    ]]),quote = True)  
  os.remove("inbox.html")
  return Response(status=200)
