from telegram import Bot

import logging
logger = logging.getLogger(__name__)

class TelegramLogHandler(logging.Handler):
    channel = None
    token = None

    def __init__(self,channel,token,*args,**kwargs):
        self.channel = channel
        self.token = token
        super().__init__(*args,**kwargs)

    def emit(self, record):
        try:
            bot = Bot(token=self.token)
            message = self.format(record)[:4000]
            bot.send_message(self.channel,message,disable_web_page_preview=True)
        except Exception as e:
            print(e)