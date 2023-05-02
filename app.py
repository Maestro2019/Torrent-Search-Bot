import api
from bot import telegram_chatbot

bot = telegram_chatbot("config.cfg")

def bot_send_message(*args, sender = None):
    '''send the message to telegram'''
    user = sender if sender else from_      # user is from_ if sender not mentioned
    message = " ".join(args)
    message = message.replace("&","%26")        # else gives wrong ans
    bot.send_message(message, user["id"])
    return

update_id = None
while True:
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    if updates:
        for item in updates:
            update_id = item["update_id"]
            from_ = item["message"]["from"]
            try:
                message = item["message"]["text"]

            except Exception as e:
                print(e)
                continue
    
            if message == "/daily":
                res = api.get_search_result(api.DAILY)
                reply = ""
                for row in res:
                    reply += "{} - {} (size:{})\n\n".format(row['no'], row['name'], row['size'])
                bot_send_message(reply)
