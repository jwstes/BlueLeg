from datetime import datetime

class Receipt():
    def __init__(self, items, customerID):
        self.__items = items
        self.__customerID = customerID
        self.__date = self.generate_date()
        self.__totalPrice = self.generate_totalPrice()
        
    def generate_date(self):
        y = datetime.now()
        x = datetime(y.year, y.month, y.day, y.hour, y.minute, y.second)
        return x

    def generate_totalPrice(self):
        keys = list(self.__items.keys())
        totalPrice = 0
        for key in keys:
            totalPrice = totalPrice + float(self.__items[key][1])
        return totalPrice
    
    def get_date(self):
        return self.__date
    def get_items(self):
        return self.__items
    def get_totalPrice(self):
        return self.__totalPrice
    # def get_fullReceipt(self):
    #     keys = list(self.__items.keys())
    #     fullReceipt = "FULL RECEIPT:\n"

    #     for key in keys:
    #         fullReceipt += f"{key} - S${self.__items[key]}\n"
    #     fullReceipt += "-END OF RECEIPT-"
    #     return fullReceipt
    
    def __str__(self):
        return f"Receipt: {self.__date.day}-{self.__date.month}-{self.__date.year} Customer ID: ({self.__customerID}): {len(self.__items)} items bought."