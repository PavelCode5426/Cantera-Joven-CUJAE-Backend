import glob
import importlib

class AutoImporter:
    def cleanPath(self,file):
        file = file.replace('\\', '.')
        file = file.replace('.py', '')
        return file
    def loadApps(self,exclude:list=['AppConfig']):
        self.apps = set()
        prefix = '**/apps.py'
        for file in glob.glob(prefix,recursive=True):
            file = self.cleanPath(file.__str__())
            appsInported = importlib.import_module(file)
            for app in dir(appsInported):
                if not app.startswith('__') and not app in exclude:
                    self.apps.add(file+'.'+app)
        return self.apps
    def loadUrls(self,exclude:list=[]):
        self.urls = dict()
        prefix = '**/urls.py'
        for file in glob.glob(prefix, recursive=True):
            file = self.cleanPath(file.__str__())
            if not file in exclude:
                appsInported = __import__(file,globals(),locals(),['app_name','app_prefix'],0)
                app_prefix = appsInported.app_prefix if hasattr(appsInported,'app_prefix') else ''
                if hasattr(appsInported,'app_name'):
                    self.urls[appsInported.app_name] = (app_prefix,file)

        returnList = list()
        from django.urls import path,include
        for index in self.urls:
            returnList.append(path(self.urls[index][0],include(self.urls[index][1],namespace=index)))


        return returnList