from Account import Account
import hashlib

class Admin(Account):
    def __init__(self, username, password):
        Account.__init__(self, username, password)
        self.__userID = self.generateUserID()
        self.__name = ""
        self.__email = ""
        self._rights = True
    
    def generateUserID(self):
        prefix = f"admin-{hashlib.sha384(self.get_username().encode()).hexdigest()[0:6]}"
        return prefix

    def get_userID(self):
        return self.__userID
    def get_name(self):
        return self.__name
    def get_email(self):
        return self.__email
    def get_rights(self):
        return self._rights
    def get_points(self):
        return 0

    def set_name(self, value):
        self.__name = value
    def set_email(self, value):
        self.__email = value
    
    def __str__(self):
        return f"Object({self.__userID}): {self.__name}"