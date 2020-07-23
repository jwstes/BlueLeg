import hashlib
from datetime import datetime

class Transaction():
    def __init__(self, receipt, userID, username):
        self.__userID = userID
        self.__username = username
        self.__receipt = receipt
        self.__date = self.get_date()
        self.__totalPrice = self.__receipt.get_totalPrice()
        self.__transactionID = self.generate_transactionID()
        self.__pointsEarned = self.generate_pointsEarned()

        #KEY = DATE
        #VALUE = WAITING TO BE SHIPPED ,SHIPPED, IN TRANSIT, DELIVERED
        self.__status = self.generate_status()
    

    def generate_transactionID(self):
        date = self.__date
        userID = self.__userID
        items = self.__receipt.get_items()
        model = f"{date.year}{date.month}{date.day}{self.__userID}{len(items)}{self.__totalPrice}"
        transactionID = f"transaction-{hashlib.sha384(model.encode()).hexdigest()[0:6]}"
        return transactionID
    
    def generate_pointsEarned(self):
        ptsEarned = int(round(float(self.__totalPrice) * 0.005))
        return ptsEarned

    def generate_status(self):
        date = f"{self.__date.year}-{self.__date.month}-{self.__date.day} {self.__date.hour}:{self.__date.minute}"
        status = {date : 'WAITING TO BE SHIPPED'}
        return status

    def get_date(self):
        return self.__receipt.get_date()
    def get_userID(self):
        return self.__userID
    def get_username(self):
        return self.__username
    def get_receipt(self):
        return self.__receipt
    def get_totalPrice(self):
        return self.__totalPrice
    def get_transactionID(self):
        return self.__transactionID
    def get_pointsEarned(self):
        return self.__pointsEarned
    def get_status(self):
        return self.__status
    
    def set_status(self, value):
        x = datetime.now()
        date = f"{x.year}-{x.month}-{x.day} {x.hour}:{x.minute}"
        self.__status[date] = value
    
    def __str__(self):
        return f"Transaction: {self.__date.day}-{self.__date.month}-{self.__date.year} User ID: {self.__userID} \n--{self.__receipt}\n----Total Price: {self.__totalPrice}"

