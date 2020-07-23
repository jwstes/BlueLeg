import shelve
import json
from Product import Product
from Member import Member
from Admin import Admin
from Receipt import Receipt
from Transaction import Transaction
import hashlib
from datetime import datetime
from Supplier import Supplier


def addProduct(title, description, price, thumbnail, slideshow1, slideshow2, slideshow3, category):
    x = Product(title, description, price, category)
    x.set_images(thumbnail, slideshow1, slideshow2, slideshow3)
    
    s = shelve.open('db/products.db')
    s[x.get_productID()] = x
    s.close()

    return x.get_productID()

def addToMapping(category, id):
    categoryMap = json.loads(open('categoryMap.txt', 'r').read())
    categoryMap[category.lower()].append(id)

    file = open('categoryMap.txt', 'w')
    file.write(json.dumps(categoryMap))
    file.close()

def removeFromMapping(id):
    categoryMap = json.loads(open('categoryMap.txt', 'r').read())
    for key in categoryMap:
        if id in categoryMap[key]:
            categoryMap[key].remove(id)

    file = open('categoryMap.txt', 'w')
    file.write(json.dumps(categoryMap))
    file.close()

def get_products():
    products = shelve.open('db/products.db')
    categoryMap = json.loads( open('categoryMap.txt', 'r').read() )

    framesets = []
    helmets = []
    saddles = []
    wheels = []

    data = {'framesets' : [],
            'helmets' : [],
            'saddles' : [],
            'wheels' : []}
    
    for frameset in categoryMap['framesets']:
        x = products[frameset]
        framesets.append([ x.get_title(), x.get_description(), x.get_price(), x.get_stock(), x.get_images(), x.get_productID()])
    for helmet in categoryMap['helmets']:
        x = products[helmet]
        helmets.append([ x.get_title(), x.get_description(), x.get_price(), x.get_stock(), x.get_images(), x.get_productID()])
    for saddle in categoryMap['saddles']:
        x = products[saddle]
        saddles.append([ x.get_title(), x.get_description(), x.get_price(), x.get_stock(), x.get_images(), x.get_productID()])
    for wheel in categoryMap['wheels']:
        x = products[wheel]
        wheels.append([ x.get_title(), x.get_description(), x.get_price(), x.get_stock(), x.get_images(), x.get_productID()])

    data['framesets'] = framesets
    data['helmets'] = helmets
    data['saddles'] = saddles
    data['wheels'] = wheels

    products.close()

    return data

def SHA384(data):
    return hashlib.sha384(data.encode()).hexdigest()[0:6]

def createUser(userName, password, name, email):
    userID = f"member-{SHA384(userName)}"
    s = shelve.open('db/users.db')

    try:
        s[userID]
        s.close()
        return False
    except KeyError:
        x = Member(userName, password)
        x.set_name(name)
        x.set_email(email)
        
        s[userID] = x
        s.close()
        return True

def validateUser(userName, password, method):
    m_userID = f"member-{SHA384(userName)}"
    a_userID = f"admin-{SHA384(userName)}"
    
    s = shelve.open('db/users.db')

    if method == "login":
        try:
            if password == s[m_userID].get_password():
                s.close()
                return True
            else:
                s.close()
                return False
        except KeyError:
            try:
                if password == s[a_userID].get_password():
                    s.close()
                    return True
                else:
                    s.close()
                    return False
            except KeyError:
                s.close()
                return False
    elif method == "rights":
        m_userID = f"member-{SHA384(userName)}"
        a_userID = f"admin-{SHA384(userName)}"

        try:
            return s[m_userID].get_rights()
        except KeyError:
            try:
                return s[a_userID].get_rights()
            except KeyError:
                print("Not Exist")

def username2id(userName):
    s = shelve.open('db/users.db')
    keys = list(s.keys())
    for key in keys:
        if s[key].get_username() == userName:
            s.close()
            return key
    s.close()

def id2username(id):
    s = shelve.open('db/users.db')
    username = s[id].get_username()
    s.close()
    return username

def getPassword(username, id):
    if id == "": #MEANS GOT ONLY USERNAME
        id = username2id(username)
        s = shelve.open('db/users.db')
        password = s[id].get_password()
        s.close()
        return password
    else:
        s = shelve.open('db/users.db')
        password = s[id].get_password()
        s.close()
        return password

def changePassword(newPassword, username, id):
    if id == "":
        id = username2id(username)
        s = shelve.open('db/users.db')
        x = s[id]
        x.set_password(newPassword)
        s[id] = x
        s.close()

def addToCart(userName, productID, quantity):
    userID = f"member-{SHA384(userName)}"

    s = shelve.open('db/users.db')
    x = s[userID]
    x.set_cart(productID, quantity)
    s[userID] = x
    s.close()

def getCart(userName):
    userID = f"member-{SHA384(userName)}"
    
    s = shelve.open('db/users.db')
    x = s[userID]

    s.close()
    return x.get_cart()

def removeFromCart(userName, productID):
    userID = f"member-{SHA384(userName)}"
    s = shelve.open('db/users.db')
    x = s[userID]
    cart = x.get_cart()
    new_cart = []

    for item in cart:
        if item[0] == productID:
            pass
        else:
            new_cart.append(item)
    x.empty_cart()
    for item in new_cart:
        x.set_cart(item[0], item[1])

    s[userID] = x

    s.close()

def checkout(userID, cart, option, receiptClass, paymentGatewayInformation, totalPrice):
    if option == "processCheckout":
        items = {}
        for item in cart:
            items[item[1]] = [item[5], item[3], item[2]]
        receipt = Receipt(items, userID) #MAKE RECEIPT OBJECT
        
        s = shelve.open('db/temporaryReceipt.db')
        s[userID] = receipt
        s.close()
    elif option == "confirmPayment":
        receipt = receiptClass
        username = userID
        user_id = username2id(userID)

        transaction = Transaction(receipt, user_id, username) #MAKE TRANSACTION OBJECT
        points = transaction.get_pointsEarned()
        
        s = shelve.open('db/transactionHistory.db')
        
        try:
            x = s[user_id]
            keys = list(x.keys())
            newCount = int(len(keys)) + 1

            x = s[user_id]
            x[newCount] = transaction
            s[user_id] = x
        except KeyError:
            s[user_id] = {1 : transaction}

        s.close()

        ####
        #UPDATING STOCKS
        ####
        keys = list(cart.keys())
        for key in keys:
            item_id = cart[key][0]
            quantityPurchased = cart[key][2]

            oldStock = stock(item_id, 0, "getStock")

            newStock = int(oldStock) - int(quantityPurchased)
            
            stock(item_id, newStock, "updateStock")

        clear_cart(user_id)

        ####
        #ADDING POINTS TO USER
        ####
        s = shelve.open('db/users.db')
        x = s[user_id]
        oldPts = int(x.get_points())
        newPts = oldPts + int(points)
        x.set_points(newPts)
        s[user_id] = x
        s.close()

def clear_cart(userID):
    s = shelve.open('db/users.db')
    x = s[userID]
    x.empty_cart()
    s[userID] = x
    s.close()

def stock(itemID, new_stock, option):
    if option == "updateStock":
        s = shelve.open('db/products.db')
        
        x = s[itemID]
        x.set_stock(int(new_stock))
        
        s[itemID] = x

        s.close()
    elif option == "getStock":
        s = shelve.open('db/products.db')

        x = s[itemID].get_stock()
        s.close()
        return x

def addStock(productID, supplierID, quantity):
    s = shelve.open('db/products.db')
    x = s[productID]
    oldStock = x.get_stock()
    x.set_stock(int(oldStock) + int(quantity))
    s[productID] = x
    s.close()

    s = shelve.open('db/supplier.db')
    x = s[supplierID]
    x.remove_supplierItemStock(productID, int(quantity))
    s[supplierID] = x
    s.close()

def findSupplier(productID):
    s = shelve.open('db/supplier.db')
    returnValue = []

    for key in s:
        for productKey in s[key].get_supplierItems():
            if productKey == productID:
                print(f"{key} has {s[key].get_supplierItems()[productKey]} of them.")

                returnValue.append([key, s[key].get_supplierName(), s[key].get_supplierItems()[productKey]])
    s.close()
    return returnValue

def addSupplier(SupplierName, SupplierItems):
    supplier = Supplier(SupplierName)
    SupplierItems = SupplierItems.split(',')
    for item in SupplierItems:
        supplier.add_supplerItems(item, 0)
    
    s = shelve.open('db/supplier.db')
    s[supplier.get_supplierID()] = supplier
    s.close()
    return supplier.get_supplierID()

def updateSupplier(supplierItems, supplierID):
    s = shelve.open('db/supplier.db')
    oldSupplier = s[supplierID]

    for item in supplierItems:
        oldSupplier.add_supplerItems(item[0], item[1])

    s[supplierID] = oldSupplier

    s.close()

def global_trackOrder(userID, transactionID):
    s = shelve.open('db/transactionHistory.db')
    for key in s[userID]:
        if s[userID][key].get_transactionID() == transactionID:
            orderStatus = s[userID][key].get_status()
            s.close()
            return orderStatus

    s.close()

def myAccount_myOrders(username):
    id = username2id(username)
    s = shelve.open('db/transactionHistory.db')
    try:
        orders = {}   
        for key in s[id]:
            x = s[id][key].get_receipt().get_items()
            transactionID = s[id][key].get_transactionID()
            date = s[id][key].get_date()
            date = f"{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}"

            subOrder = []
            for i in x:
                subOrder.append([ i, x[i][0], x[i][2], x[i][1], transactionID  ])
            orders[date] = subOrder

        s.close()
        return orders
    except KeyError:
        s.close()
        return False

    s.close()

def adminCP_Users():
    s = shelve.open('db/users.db')
    keys = list(s.keys())

    users = []
    for key in keys:
        users.append([s[key].get_userID(), s[key].get_username(), s[key].get_points()])

    s.close()

    return users

def adminCP_delUser(userID):
    s = shelve.open('db/users.db')
    del s[userID]
    s.close()

    s = shelve.open('db/transactionHistory.db')
    try:
        del s[userID]
    except KeyError:
        pass
    s.close()

def adminCP_Products():
    s = shelve.open('db/products.db')
    keys = list(s.keys())

    items = []
    for key in keys:
        items.append( [ s[key].get_productID(), s[key].get_images()[0], s[key].get_title(), s[key].get_price(), s[key].get_stock() ] )
    s.close()

    return items

def adminCP_Suppliers():
    suppliers = {}
    s = shelve.open('db/supplier.db')
    for key in s:
        items = s[key].get_supplierItems()
        suppliers[key] = [s[key].get_supplierName(),items]
    s.close()

    return suppliers

def adminCP_Transactions():
    transactions = {}
    s = shelve.open('db/transactionHistory.db')
    keys = list(s.keys())
    
    for key in keys:
        subKeys = list(s[key].keys())
        cart = []
        count = 0
        for subKey in subKeys:
            itemKeys = list(s[key][subKey].get_receipt().get_items().keys())
            item = s[key][subKey].get_receipt().get_items()

            subCart = []
            for itemKey in itemKeys:
                subCart.append([ itemKey, item[itemKey][2] ])
            cart.append([ [s[key][subKey].get_date().year, s[key][subKey].get_date().month, s[key][subKey].get_date().day], subCart, s[key][subKey].get_transactionID(), s[key][subKey].get_pointsEarned(), s[key][subKey].get_totalPrice()])
            count = count + 1
        transactions[key] = cart
    s.close()
    return transactions


def manageTransactions():
    s = shelve.open('db/transactionHistory.db')
    transactions = []

    for x in s:
        for y in s[x]:
            a = ""
            for u in s[x][y].get_status():
                a = s[x][y].get_status()[u]
            transactionsSet = [ s[x][y].get_userID(),s[x][y].get_transactionID(), a]
            transactions.append(transactionsSet)

    s.close()
    return transactions

def changeTransactionStatus(transactionIDs, status):
    s = shelve.open('db/transactionHistory.db')

    userTransactions = {}

    for transactionID in transactionIDs:
        for key in s:
            userTransactions = s[key]
            for subKey in userTransactions:
                if userTransactions[subKey].get_transactionID() == transactionID:
                    userTransactions[subKey].set_status(status)

            s[key] = userTransactions

    s.close()



def calculateRevenue():
    s = shelve.open('db/transactionHistory.db')
    total=0
    for x in s:
        for y in s[x]:
            total+= int(s[x][y].get_totalPrice())
    s.close()
    return total

def calculateAverage():
    s = shelve.open('db/transactionHistory.db')
    total=0
    count=0
    for x in s:
        for y in s[x]:
            count+=1
            total+= int(s[x][y].get_totalPrice())
    s.close()
    average=total/count
    return average

def pastYearly():
    y = datetime.now()
    last=y.year-1
    pastYearly=0
    s = shelve.open('db/transactionHistory.db')
    for x in s:
        for y in s[x]:
            if last==s[x][y].get_date().year:
                pastYearly+= int(s[x][y].get_totalPrice())
    s.close()
    return pastYearly

def Yearly():
    y = datetime.now()
    a=y.year
    yearly=0
    s = shelve.open('db/transactionHistory.db')
    for x in s:
        for y in s[x]:
            if a==s[x][y].get_date().year:
                yearly+= int(s[x][y].get_totalPrice())
    s.close()
    return yearly

def Monthly():
    y = datetime.now()
    a=y.month
    monthly=0
    s = shelve.open('db/transactionHistory.db')
    for x in s:
        for y in s[x]:
            if a==s[x][y].get_date().month:
                monthly+= int(s[x][y].get_totalPrice())
    s.close()
    return monthly

def Daily():
    y = datetime.now()
    day=str(y).split(" ")
    daily=0
    s = shelve.open('db/transactionHistory.db')
    for x in s:
        for y in s[x]:
            data=str(s[x][y].get_date()).split(" ")
            if day[0]==data[0]:
                daily+= int(s[x][y].get_totalPrice())
    s.close()
    return daily

def compareYears(this,last):
    new=float(this-last)
    return new

def top_user_exchanges():
    s=shelve.open('db/users.db')
    topUser=""
    topcount=0
    for key in s:
        details=key.split("-")
        count=0
        if details[0]=="member":
            for i in s[key].get_myRewards():
                count+=1
            if count>topcount:
                topUser=s[key].get_name()
                topcount=count
            count=0
    return topUser,topcount

def average_exchanges():
    s=shelve.open('db/users.db')
    countList=[]
    nameList=[]
    for key in s:
        details=key.split("-")
        count=0

        if details[0]=="member":
            for i in s[key].get_myRewards():
                count+=1
        name=s[key].get_name()
        nameList.append(name)
        countList.append(count)
    return(len(nameList)/sum(countList))

def top_rewards():
    s=shelve.open('db/users.db')
    gainlist=[]
    for key in s:
        details=key.split("-")
        if details[0]=="member":
            for i in s[key].get_myRewards():
                gainlist.append(i)
    s.close()
    s=shelve.open('db/rewards.db')
    list=[]
    newlist=[]
    for i in gainlist:
        if i.get_rewardName() not in list:
            list.append(i.get_rewardName())
    for i in gainlist:
        newlist.append(i.get_rewardName())
    top=''
    topcount=0
    for i in list:
        count=0
        for a in newlist:
            if a in i:
                count+=1
        if count > topcount:
            top=i
            topcount=count

    return top,topcount
