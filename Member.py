from Account import Account
import hashlib

class Member(Account):
    def __init__(self, username, password):
        Account.__init__(self, username, password)
        self.__userID = self.generateUserID()
        self.__name = ""
        self.__email = ""
        self._rights = False
        self.__cart = []
        self.__points = 0
        self.__myRewards = []

    def generateUserID(self):
        prefix = f"member-{hashlib.sha384(self.get_username().encode()).hexdigest()[0:6]}"
        return prefix

    def get_userID(self):
        return self.__userID
    def get_name(self):
        return self.__name
    def get_email(self):
        return self.__email
    def get_rights(self):
        return self._rights
    def get_cart(self):
        return self.__cart
    def get_points(self):
        return self.__points
    def get_myRewards(self):
        return self.__myRewards

    def set_name(self, value):
        self.__name = value
    def set_email(self, value):
        self.__email = value
    def set_cart(self, productID, quantity):
        self.__cart.append([productID, quantity])
    def empty_cart(self):
        self.__cart = []
    def set_points(self, value):
        self.__points = value
    def set_myRewards(self, object):
        self.__myRewards.append(object)
    
    def __str__(self):
        return f"Object({self.__userID}): {self.__name}"