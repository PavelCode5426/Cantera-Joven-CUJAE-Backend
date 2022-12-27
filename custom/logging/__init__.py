import logging
from logging import LogRecord

from telegram import Bot

logger = logging.getLogger(__name__)


class TelegramLogFilter(logging.Filter):
    exclude = ['']

    def filter(self, record):
        return False


class TelegramFormater(logging.Formatter):
    def format(self, record: LogRecord):
        if hasattr(record, 'request'):
            text = self._format_request(record)
        else:
            text = self._format_simple(record)

        return text

    def _format_request(self, record: LogRecord):
        text_format = "Nivel: {levelname} \n" \
                      "Fecha: {asctime} \n" \
                      "Usuario: {user} \n" \
                      "Metodo: {method} \n" \
                      "URL: {path_info} \n" \
                      "Mensaje: {message} \n" \
                      "Pila de Traseo: {stacktrace} \n" \
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

    def _format_simple(self, record: LogRecord):
        return f'{record.levelname} {record.message}'


class TelegramLogHandler(logging.Handler):
    channel = None
    token = None

    def __init__(self, channel, token, *args, **kwargs):
        self.channel = channel
        self.token = token
        super(TelegramLogHandler, self).__init__(*args, **kwargs)

    def emit(self, record: LogRecord):
        try:
            if self.channel and self.token:
                bot = Bot(token=self.token)
                message = self.format(record)[:4000]
                bot.send_message(self.channel, message, disable_web_page_preview=True)
        except Exception as e:
            print(e)
