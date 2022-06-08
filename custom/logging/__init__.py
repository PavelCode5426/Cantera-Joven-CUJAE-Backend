from telegram import Bot

import logging
logger = logging.getLogger(__name__)

class TelegramFormater(logging.Formatter):
    def format(self, record):

        text_format = "Nivel: {levelname} \n" \
                      "Fecha: {asctime} \n" \
                      "Usuario: {user} \n" \
                      "Metodo: {method} \n" \
                      "URL: {path_info} \n" \
                      "Mensaje: {message} \n"\
                      "Pila de Traseo: {stacktrace} \n"\
            .format(
            levelname=record.levelname,
            asctime=record.asctime,
            user=record.request.user if record.request.user else 'N/A',
            method=record.request.method if record.request.method else 'N/A',
            path_info=record.request.path_info if record.request.path_info else 'N/A',
            message=record.message,
            stacktrace=record.exc_text[:500]
        )

        return text_format

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