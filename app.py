import api
from bot import telegram_chatbot

def app():

    def bot_send_message(*args, sender = None):
        '''send the message to telegram'''
        user = sender if sender else from_      # user is from_ if sender not mentioned
        message = " ".join(args)
        message = message.replace("&","%26")        # else gives wrong ans
        bot.send_message(message, user["id"])
        return
    
    bot = telegram_chatbot("config.cfg")
    update_id = None
    from_ = None

    while True:
        updates = bot.get_updates(offset=update_id)
        updates = updates["result"]
        if updates:
            for item in updates:
                update_id = item["update_id"]
                from_ = item["message"]["from"]
                try:
                    message = item["message"]["text"]
                    print(update_id, message)

                except Exception as e:
                    print(e)
                    continue
                
                if message == "/status":
                    bot_send_message("Bot is alive and active !!")
                    
                if message == "/daily":
                    res = api.get_search_result(api.DAILY)
                    for row in res:
                        reply = "<b>{no}: {name}</b>\n\n<i>Size: {size}\nURL: {url}</i>".format(no=row['no'], name=row['name'], size=row['size'], url=row['url'])
                        bot_send_message(reply)
