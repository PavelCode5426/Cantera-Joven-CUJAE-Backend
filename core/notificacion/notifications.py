class AbstractNotification(object):
    function_prefix = '_send'
    def send(self,*args,**kwargs):
        for func in dir(self):
            if func.startswith(self.function_prefix):
                func=self.__getattribute__(func)
                func(*args,**kwargs)
    def __new__(cls, *args, **kwargs):
        is_in = False
        it = iter(dir(cls))
        try:
            item = next(it)
            while item and not is_in:
                if item.startswith(cls.function_prefix):
                    is_in = True
                item = next(it)
        except StopIteration:
            pass
        if not is_in:
            raise NotImplementedError('Es necesario implementar un metodo {prefix}*'.format(prefix=cls.function_prefix))
        return super().__new__(cls,*args,**kwargs)

class EmailNotification(AbstractNotification):
    def _send_email(self,*args,**kwargs):
        raise NotImplementedError('Es necesario implementar este metodo')

class TelegramNotification(AbstractNotification):
    def _send_telegram(self,*args,**kwargs):
        raise NotImplementedError('Es necesario implementar este metodo')

class DataBaseNotification(AbstractNotification):
    def _send_database(self,*args,**kwargs):
        raise NotImplementedError('Es necesario implementar este metodo')

