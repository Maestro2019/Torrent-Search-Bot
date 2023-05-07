import api
from bot import telegram_chatbot

def app(*args):

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
    torrent_search_results = []

    while True:
        updates = bot.get_updates(offset=update_id)
        updates = updates.get("result")
        if updates:
            for item in updates:
                try:
                    update_id = item["update_id"]
                    from_ = item["message"]["from"]
                    message = item["message"]["text"]
                    print(update_id, "-->", message)

                except Exception as e:
                    print(e)
                    continue
                
                if message == "/status":
                    bot_send_message("Bot is alive and active !!")
                    
                if message == "/daily":
                    torrent_search_results = api.get_search_result(api.DAILY)
                    reply = ""
                    for row in torrent_search_results:
                        reply += "<b>{no}: {name}</b>\n<i>Size: {size}</i>\n\n".format(no=row['no'], name=row['name'], size=row['size'])
                    bot_send_message(reply)
                
                if message.isnumeric():
                    index = int(message)-1
                    if index >= len(torrent_search_results):
                        bot_send_message("Number not matching with our result")
                        continue
                    url = torrent_search_results[index]['url']
                    magnet = api.get_magnet(url)
                    bot_send_message(magnet)


# run
app()