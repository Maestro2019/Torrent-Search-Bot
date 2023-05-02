import requests
import json
import configparser as cfg
import urllib


class telegram_chatbot():

    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)
        self.file_base = "https://api.telegram.org/file/bot{}/".format(self.token)

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')

    def get_file_contents(self, file_id):
        # url = https://api.telegram.org/bot<bot_token>/getFile?file_id=the_file_id
        url = self.base + "getFile?file_id={}".format(file_id)
        r = requests.get(url)
        file_details = json.loads(r.content)
        
        # getting the file content
        # url = https://api.telegram.org/file/bot<token>/<file_path>
        file_path = file_details["result"]["file_path"]
        url = self.file_base + file_path
        r = urllib.request.urlopen(url).read()
        return r