import configparser
from os import stat

config = configparser.RawConfigParser()
config.read(".\\testingBDD\\Configuration\\config.ini")

class ReadConfig:
    @staticmethod
    def getURL():
        url = config.get('info', 'baseURL')
        return url

    @staticmethod
    def fetchUsername():
        username = config.get('info', 'userName')
        return username

    @staticmethod
    def fetchPassword():
        password = config.get('info', 'passWord')
        return password