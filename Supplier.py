import hashlib

class Supplier():
    def __init__(self, supplierName):
        self.__supplierName = supplierName
        self.__supplierID = self.generateSupplierID()
        self.__supplierItems = {}

    def generateSupplierID(self):
        prefix = f"supplier-{hashlib.sha384(self.__supplierName.encode()).hexdigest()[0:6]}"
        return prefix

    def get_supplierName(self):
        return self.__supplierName
    def get_supplierID(self):
        return self.__supplierID
    def get_supplierItems(self):
        return self.__supplierItems

    def set_supplierName(self, name):
        self.__supplierName = name
    def set_supplierID(self, ID):
        self.__supplierID = ID
    def add_supplerItems(self, productID, quantity):
        currentItems = self.__supplierItems

        try:
            c_quantity = currentItems[productID]
            c_quantity = c_quantity + quantity
            currentItems[productID] = c_quantity
        except KeyError:
            currentItems[productID] = quantity
        
        self.__supplierItems = currentItems
    def remove_supplierItemStock(self, productID, quantity):
        currentItems = self.__supplierItems

        try:
            c_quantity = currentItems[productID]
            c_quantity = c_quantity - quantity
            currentItems[productID] = c_quantity
        except KeyError:
            pass

        self.__supplierItems = currentItems