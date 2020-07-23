from flask import Flask, render_template, url_for, redirect, request, flash, Markup, make_response, Response, jsonify
import os
import json
from Form import UserForm, LoginForm, AddProduct, PaymentGateway, myAccountForm, CreateRewardForm, trackOrderForm, feedbackForm, SupplierForm
import webEngine
import shelve
from Reward import Reward
from Feedback import Feedback
from datetime import datetime
from Supplier import Supplier

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html')

@app.route('/addProduct', methods=['GET', 'POST'])
def addProduct():
    addProductForm = AddProduct(request.form)
    if request.method == 'POST' and addProductForm.validate():
        if addProductForm.category.data not in ["Framesets", "Helmets", "Saddles", "Wheels"]:
            flash("As of now we only accept Framesets, Helmets, Saddles and Wheels!")
        else:
            productID = webEngine.addProduct(addProductForm.title.data, addProductForm.description.data,
            addProductForm.price.data, addProductForm.thumbnail.data,
            addProductForm.slideshow1.data, addProductForm.slideshow2.data,
            addProductForm.slideshow3.data, addProductForm.category.data)
            webEngine.addToMapping(addProductForm.category.data.lower(), productID)
            flash("Product Added Successfully!")
            return redirect(url_for('store'))
    return render_template('addProduct.html', form=addProductForm)

@app.route('/delProduct/<id>', methods=['GET', 'POST'])
def delProduct(id):
    s = shelve.open('db/products.db')
    del s[id]
    s.close()
    webEngine.removeFromMapping(id)
    return redirect(url_for('adminCP'))

@app.route('/store')
def store():
    products = webEngine.get_products()

    framesets = products['framesets']
    lengthFramesets = len(framesets)

    helmets = products['helmets']
    lengthHelmets = len(helmets)

    saddles = products['saddles']
    lengthSaddles = len(saddles)
    
    wheels = products['wheels']
    lengthWheels = len(wheels)

    return render_template('store.html', framesets=framesets, lengthFramesets=lengthFramesets,
                                         helmets=helmets, lengthHelmets=lengthHelmets,
                                         saddles=saddles, lengthSaddles=lengthSaddles,
                                         wheels=wheels, lengthWheels=lengthWheels,
                                         data = products)

@app.route('/viewProduct')
def viewProduct():
    return render_template('viewProduct.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    userForm = UserForm(request.form)
    if request.method == 'POST' and userForm.validate():
        if webEngine.createUser(userForm.userName.data, userForm.password.data, userForm.firstName.data, userForm.email.data) != False:
            print("User Created Successfully!")
            return render_template('home.html')
        else:
            flash("User Already Exists!")

    return render_template('register.html', form=userForm)

@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm(request.form)
    if request.method == 'POST' and loginForm.validate():
        if webEngine.validateUser(loginForm.userName.data, loginForm.password.data, 'login') != False:
            resp = make_response(render_template('home.html'))
            rights = webEngine.validateUser(loginForm.userName.data, loginForm.password.data, 'rights')
            cookiePayload = [loginForm.userName.data, rights]
            resp.set_cookie('loginKey', json.dumps(cookiePayload))

            return resp
        else:
            flash("User doesn't exist or password is incorrect!")

    return render_template('login.html', form=loginForm)

@app.route('/myAccount', methods=['GET', 'POST'])
def myAccount():
    myaccountform = myAccountForm(request.form)
    if request.method == 'POST' and myaccountform.validate():
        username = json.loads(request.cookies.get('loginKey'))[0]
        webEngine.changePassword(myaccountform.newPassword.data, username, "")
        resp = make_response(render_template('home.html'))
        resp.set_cookie('loginKey', json.dumps(["nothing", "False"]))
        return resp
    else:
        rewardsList = []
        s = shelve.open('db/rewards.db')
        for key in s:
            reward = s[key]
            rewardsList.append(reward)
        s.close()
        username = json.loads(request.cookies.get('loginKey'))[0]
        userID = webEngine.username2id(username)
        s=shelve.open('db/users.db')
        gainlist=[]
        for i in s[userID].get_myRewards():
            gainlist.append(i)
        points=s[userID].get_points()
        return render_template('myAccount.html', form=myaccountform, rewardsList=rewardsList, gainlist=gainlist, userID=userID,points=points)

@app.route('/myAccountSettings', methods=['GET'])
def myAccountSettings():
    option = request.args.get('option')
    if option == "getPassword":
        username = request.args.get('username')
        password = webEngine.getPassword(username, "")

        return jsonify({ 'current_password': password })
        
    elif option == "getMyOrders":
        username = request.args.get('username')
        orders = webEngine.myAccount_myOrders(username)

        if orders != False:
            return jsonify({ 'orders': orders })
        else:
            return jsonify({ 'orders': "nothing" })

    return jsonify({ 'response': 200 })

@app.route('/trackOrder', methods=['GET'])
def trackOrder():
    transactionID = request.args.get('transactionID')
    username = request.args.get('username')
    userID = webEngine.username2id(username)
    
    trackingDetails = webEngine.global_trackOrder(userID, transactionID)

    return jsonify({ 'orderStatus': trackingDetails })

@app.route('/checkUser', methods=['GET'])
def checkUser():
    option = request.args.get('option')
    loginKey = ['nothing', "False"]

    if option == "logout":
        resp = make_response(render_template('home.html'))
        resp.set_cookie('loginKey', json.dumps(["nothing", "False"]))

        return resp
    elif option == "get_user_info":
        try:
            loginKey = json.loads(request.cookies.get('loginKey'))
        except:
            pass

        username = loginKey[0]
        rights = str(loginKey[1])

        return jsonify({ 'username': username, 'rights': rights })

@app.route('/editUser/<id>', methods=['GET', 'POST'])
def editUser(id):
    editUserForm = myAccountForm(request.form)
    if request.method == 'POST':
        s = shelve.open('db/users.db')
        user = s[id]
        user.set_username(editUserForm.userName.data)
        user.set_password(editUserForm.oldPassword.data)
        s[id] = user
        s.close()
        return redirect(url_for('adminCP')) 
    else:
        s = shelve.open('db/users.db')
        user = s[id]
        s.close()

        editUserForm.userName.data = user.get_username()
        editUserForm.oldPassword.data = user.get_password()

        return render_template('editUser.html', form=editUserForm)

@app.route('/delUser', methods=['GET'])
def delUser():
    userID = request.args.get('userID')
    webEngine.adminCP_delUser(userID)
    return jsonify({'response' : 200})

@app.route('/addToCart', methods=['GET'])
def addToCart():
    option = request.args.get('option')
    userName = request.args.get('username')
    productID = request.args.get('product_id')
    quantity = request.args.get('quantity')

    if option == "add_to_cart":
        webEngine.addToCart(userName, productID, quantity)
        return jsonify({ 'response': f"Added {quantity} To Cart!" })

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/getCart', methods=['GET'])
def getCart():
    username = request.args.get('username')
    cart = webEngine.getCart(username)
    s = shelve.open('db/products.db')

    cart_items = []

    for item in cart:
        price = float(s[item[0]].get_price()) * float(item[1])
        cart_items.append([s[item[0]].get_images()[0],
                           s[item[0]].get_title(),
                           item[1], price,
                           s[item[0]].get_price(),
                           s[item[0]].get_productID()])

    return jsonify({ 'cart_items': cart_items })

@app.route('/removeFromCart', methods=['GET'])
def removeFromCart():
    username = request.args.get('username')
    productID = request.args.get('product_id')
    
    webEngine.removeFromCart(username, productID)

    return jsonify({ 'response': "Removed" })

@app.route('/processCheckout', methods=['GET'])
def processCheckout():
    username = request.args.get('username')
    cart = json.loads(request.args.get('cart'))

    webEngine.checkout(username, cart, "processCheckout", "" , "", 0)

    return jsonify({ 'response': [username, 200] })

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    paymentGateway = PaymentGateway(request.form)

    username = request.args.get('username')
    userID = webEngine.username2id(username)
    s = shelve.open('db/users.db')
    name = s[userID].get_name()
    s.close()

    receiptClass = ""
    totalPrice = 0
    date = ""
    items = []
    lengthOfItems = len(items)

    s = shelve.open('db/temporaryReceipt.db')
    totalPrice = s[username].get_totalPrice()
    date = s[username].get_date()
    items = s[username].get_items()
    receiptClass = s[username]
    s.close()

    if request.method == 'POST' and paymentGateway.validate():
        paymentGatewayInformation = [paymentGateway.fullName.data,
        paymentGateway.cardnumber.data,
        paymentGateway.exp_month.data,
        paymentGateway.exp_year.data,
        paymentGateway.cvv.data]
        webEngine.checkout(username, items, "confirmPayment", receiptClass, paymentGatewayInformation, totalPrice)

        return render_template('thankyou.html')

    return render_template('checkout.html', totalPrice=totalPrice, items=items, date=date
                           ,name=name, userID=userID, lengthOfItems=lengthOfItems, form=paymentGateway)

@app.route('/adminCP')
def adminCP():
    users = webEngine.adminCP_Users()
    products = webEngine.adminCP_Products()

    transactions = webEngine.adminCP_Transactions()
    userIDs = list(transactions.keys())
    userNames = []
    
    for userID in userIDs:
        userNames.append(webEngine.id2username(userID))
    

    revenue=webEngine.calculateRevenue()
    average=webEngine.calculateAverage()
    pastYearly=webEngine.pastYearly()
    yearly=webEngine.Yearly()
    monthly=webEngine.Monthly()
    daily=webEngine.Daily()
    compareYears=webEngine.compareYears(yearly,pastYearly)
    topUser=webEngine.top_user_exchanges()
    averageExchange=webEngine.average_exchanges()
    topReward=webEngine.top_rewards()

    rewardsList = []
    s = shelve.open('db/rewards.db')
    for key in s:
        reward = s[key]
        rewardsList.append(reward)
    s.close()
    
    feedbacks = {}
    feedback_usernames = {}
    s = shelve.open('db/feedback.db')
    for key in s:
        feedbacks[key] = s[key]
        feedback_usernames[key] = webEngine.id2username(key)
    s.close()

    return render_template('adminCP.html', users=users, lenOfUsers=len(users),
                                           products=products, lenOfProducts=len(products),
                                           be_transactions=transactions, be_userIDs=userIDs,
                                           be_userNames=userNames

                                            ,revenue=revenue,average=average
                                            ,pastYearly=pastYearly,yearly=yearly,monthly=monthly,daily=daily,
                                            reward=reward,rewardsList=rewardsList, compareYears=compareYears,
                                            topUser=topUser,averageExchange=averageExchange,topReward=topReward

                                            ,feedbacks=feedbacks, feedback_usernames=feedback_usernames)

@app.route('/manageTransactions')
def manageTransactions():
    transactions = webEngine.manageTransactions()
    lengthOfTransactions = len(transactions)

    return render_template('manageTransactions.html', transactions=transactions, lengthOfTransactions=lengthOfTransactions)

@app.route('/changeStatus', methods=['GET'])
def changeStatus():
    transactionIDs = json.loads(request.args.get('transactionIDs'))
    status = request.args.get('status')
    webEngine.changeTransactionStatus(transactionIDs, status)

    return jsonify({'response' : "Status Changed!"})

@app.route('/change_stock', methods=['GET'])
def change_stock():
    productID = request.args.get('productID')
    newStock = request.args.get('newStock')

    webEngine.stock(productID, newStock, 'updateStock')

    return jsonify({ 'response': 200 })

@app.route('/createReward', methods=['GET', 'POST'])
def createReward():
    createRewardForm = CreateRewardForm(request.form)
    if request.method == 'POST' and createRewardForm.validate():
        s = shelve.open('db/rewards.db')

        reward = Reward(createRewardForm.rewardName.data, createRewardForm.points.data,createRewardForm.quantity.data, createRewardForm.incentive.data)
        s[reward.get_rewardID()] = reward

        s.close()

        return redirect(url_for('adminCP'))
    return render_template('createReward.html', form=createRewardForm)

@app.route('/updateReward/<id>/', methods=['GET', 'POST'])
def updateReward(id):
    updateRewardForm = CreateRewardForm(request.form)
    if request.method == 'POST' and updateRewardForm.validate():
        s = shelve.open('db/rewards.db')

        reward = s[id]
        reward.set_rewardName(updateRewardForm.rewardName.data)
        reward.set_incentive(updateRewardForm.incentive.data)
        reward.set_points(updateRewardForm.points.data)
        reward.set_quantity(updateRewardForm.quantity.data)
        s[id] = reward

        s.close()
        return redirect(url_for('adminCP'))
    else:

        s = shelve.open('db/rewards.db')
        reward = s[id]
        s.close()


        updateRewardForm.rewardName.data = reward.get_rewardName()
        updateRewardForm.incentive.data = reward.get_incentive()
        updateRewardForm.points.data = reward.get_points()
        updateRewardForm.quantity.data = reward.get_quantity()
        return render_template('updateReward.html',form=updateRewardForm)

@app.route('/deleteReward/<id>', methods=['POST'])
def deleteReward(id):
    s = shelve.open('db/rewards.db')
    del s[id]
    s.close()
    return redirect(url_for('adminCP'))

@app.route('/trackOrderPage/<userID>', methods=['GET','POST'])
def trackOrderPage(userID):
    userID = webEngine.username2id(userID)
    trackorderform = trackOrderForm(request.form)

    if request.method == 'POST' and trackorderform.validate():
        trackingDetails = webEngine.global_trackOrder(userID, trackorderform.transactionID.data)
        orderStatus = []
        for key in trackingDetails:
            orderStatus.append([key, trackingDetails[key]])
        return render_template('trackOrder.html', form=trackorderform, orderStatus=orderStatus)

    return render_template('trackOrder.html', form=trackorderform)

@app.route('/feedback/<username>', methods=['GET','POST'])
def feedback(username):
    userID = webEngine.username2id(username)

    feedbackform = feedbackForm(request.form)

    fullName = ""
    userName = ""
    email = ""
    message = ""

    user = []
    s = shelve.open('db/users.db')
    user = s[userID]
    s.close()

    if request.method == 'POST' and feedbackform.validate():
        fullName = feedbackform.fullName.data
        userName = feedbackform.userName.data
        email = feedbackform.email.data
        message = feedbackform.message.data
        
        feedbackObject = Feedback(fullName, user.get_username(), user.get_password(), email, message)

        feedbackShelve = {}
        s = shelve.open('db/feedback.db')

        try:
            feedbackShelve = s[userID]
            feedbackShelve[feedbackObject.get_feedbackID()] = feedbackObject
            s[userID] = feedbackShelve
        except KeyError:
            feedbackShelve[feedbackObject.get_feedbackID()] = feedbackObject
            s[userID] = feedbackShelve

        s.close()
        
        return render_template('home.html')
    else:

        feedbackform.userName.data = user.get_username()
        feedbackform.fullName.data = user.get_name()
        feedbackform.email.data = user.get_email()

        return render_template('feedback.html', form=feedbackform)

@app.route('/updateFeedbackStatus/<id>', methods=['GET','POST'])
def updateFeedbackStatus(id):
    id = id.split('&')

    feedbackform = feedbackForm(request.form)

    s = shelve.open('db/feedback.db')
    feedbackObj = s[id[1]][id[0]]
    s.close()

    if request.method == 'POST':
        memWrapper = {}

        s = shelve.open('db/feedback.db')
        memWrapper = s[id[1]]
        feedbackObj.set_status(feedbackform.status.data)
        memWrapper[id[0]] = feedbackObj
        s[id[1]] = memWrapper
        s.close()
        return redirect(url_for('adminCP'))
    else:
        feedbackform.fullName.data = feedbackObj.get_fullName()
        feedbackform.userName.data = feedbackObj.get_userName()
        feedbackform.email.data = feedbackObj.get_email()
        feedbackform.message.data = feedbackObj.get_message()
        feedbackform.status.data = feedbackObj.get_status()
        return render_template('updateFeedbackStatus.html', form=feedbackform)

@app.route('/deleteFeedback/<id>', methods=['GET','POST'])
def deleteFeedback(id):
    id = id.split('&')

    memWrapper = {}
    s = shelve.open('db/feedback.db')
    memWrapper = s[id[1]]
    del memWrapper[id[0]]
    s[id[1]] = memWrapper
    s.close()
    return redirect(url_for('adminCP'))

@app.route('/redeemReward/<payload>', methods=["POST"])
def redeemReward(payload):
    payload = payload.split('&')
    rewardID = payload[0]
    userID = payload[1]

    s=shelve.open('db/users.db')
    points=s[userID].get_points()
    s.close()

    s = shelve.open('db/rewards.db')
    pointsReq=s[rewardID].get_points()
    if int(points)>=int(pointsReq):
        reward=s[rewardID]
        newquantity=int(reward.get_quantity())-1
        reward.set_quantity(newquantity)
        s[rewardID] = reward
        temp=Reward(reward.get_rewardName(),reward.get_points(),1,reward.get_incentive())
        s.close()

        s=shelve.open('db/users.db')
        userdetails=s[userID]
        newpoints=int(points)-int(pointsReq)
        userdetails.set_points(newpoints)
        userdetails.set_myRewards(temp)
        s[userID] = userdetails
        s.close()

        rewardsList = []
        s = shelve.open('db/rewards.db')
        for key in s:
            reward = s[key]
            rewardsList.append(reward)
        s.close()

    else:
        print("failed")
    return redirect(url_for('myAccount',rewardsList=rewardsList,points=points))

@app.route('/addSupplier', methods=["POST", "GET"])
def addSupplier():
    supplierForm = SupplierForm(request.form)
    if request.method == 'POST' and supplierForm.validate():
        supplierID = webEngine.addSupplier(supplierForm.name.data, supplierForm.items.data)
        return redirect(url_for('adminCP'))

    return render_template('addSupplier.html', form=supplierForm)

@app.route('/getSupplier', methods=['GET'])
def getSupplier():
    suppliers = webEngine.adminCP_Suppliers()

    return jsonify({ 'response': 200, 'suppliers' : suppliers })

@app.route('/addSupplierStocks/<id>', methods=["POST", "GET"])
def addSupplierStocks(id):
    s = shelve.open('db/supplier.db')
    supplier = s[id]
    s.close()

    supplierItems = supplier.get_supplierItems()
    supplierName = supplier.get_supplierName()

    return render_template('addSupplierStocks.html', supplierItems = supplierItems, supplierName = supplierName, supplierID = id)

@app.route('/updateSupplierStocks', methods=['GET'])
def updateSupplierStocks():
    supplierID = request.args.get('supplierID')
    items = json.loads(request.args.get('items'))

    webEngine.updateSupplier(items, supplierID)

    return jsonify({ 'response': 200 })

@app.route('/deleteSupplier/<id>', methods=['POST','GET'])
def deleteSupplier(id):
    s = shelve.open('db/supplier.db')
    del s[id]
    s.close()
    return redirect(url_for('adminCP'))

@app.route('/addStockP1/<id>', methods=['POST','GET'])
def addStockP1(id):
    s = shelve.open('db/products.db')
    productDetails = [s[id].get_title(), s[id].get_stock()]
    s.close()

    suppliers = webEngine.findSupplier(id)

    return render_template('addStockP1.html', productID=id, productDetails=productDetails, suppliers=suppliers)

@app.route('/addStockP2', methods=['GET'])
def addStockP2():
    supplierID = request.args.get('supplierID')
    productID = request.args.get('productID')
    quantity = request.args.get('quantity')
    
    webEngine.addStock(productID, supplierID, quantity)
    return jsonify({ 'response': 200, 'payload': "OK" })

@app.route('/line')
def line():
    z = datetime.now()
    values=[]
    for i in range(12):
        month=i+1
        y=datetime(z.year,month,z.day)
        a=y.month
        monthly=0
        s = shelve.open('db/transactionHistory.db')
        for x in s:
            for y in s[x]:
                if a==s[x][y].get_date().month:
                    monthly+= float(s[x][y].get_totalPrice())/1000
        values.append(round(monthly,2))
        s.close()

    labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
    ]

    line_labels=labels
    line_values=values
    return render_template('line_chart.html', title='Monthly Earnings(in thousands)', max=5000, labels=line_labels, values=line_values)

@app.route('/pie')
def pie():
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

    colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

    pie_labels = nameList
    pie_values = countList
    return render_template('pie_chart.html', title='Number of Exchanges By Users', max=17000, set=zip(pie_values, pie_labels, colors))



if __name__ == '__main__':
    app.run()
