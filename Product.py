import random, string

class Product():
    def __init__(self, title, description, price, category):
        self.__productID = self.generateProductID()
        self.__title = title
        self.__description = description
        self.__price = price
        self.__category = category
        self.__stock = 100
        self.__images = [] #thumbnail, slideshow1, slideshow2, slideshow3
    
    def generateProductID(self):
        pool = string.ascii_letters
        prefix = "sku-"
        for i in range(6):
            prefix += pool[random.randint(0, 51)]
        return prefix

    def get_productID(self):
        return self.__productID
    def get_title(self):
        return self.__title
    def get_description(self):
        return self.__description
    def get_price(self):
        return self.__price
    def get_stock(self):
        return self.__stock
    def get_images(self):
        return self.__images
    def get_category(self):
        return self.__category
    
    def set_title(self, value):
        self.__title = value
    def set_description(self, value):
        self.__description = value
    def set_price(self, value):
        self.__price = value
    def set_stock(self, value):
        if int(value) > 0:
            self.__stock = value
        else:
            print("Error")
    def set_images(self, thumbnail, slideshow1, slideshow2, slideshow3):
        self.__images = [thumbnail, slideshow1, slideshow2, slideshow3]
    

    def __str__(self):
        return f'Object({self.__productID}): {self.__title}'