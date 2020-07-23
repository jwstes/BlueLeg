class Account():
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
    
    def get_username(self):
        return self.__username
    def get_password(self):
        return self.__password
    
    def set_username(self, value):
        self.__username = value
    def set_password(self, value):
        self.__password = value