from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, IntegerField

class UserForm(Form):
    firstName = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    userName = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = StringField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])

class LoginForm(Form):
    userName = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = StringField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])

class AddProduct(Form):
    title = StringField('Title', [validators.Length(min=1, max=150), validators.DataRequired()])
    description = TextAreaField('Description', [validators.Length(min=1, max=800), validators.DataRequired()])
    price = StringField('Price', [validators.Length(min=1, max=150), validators.DataRequired()])
    thumbnail = StringField('Thumbnail', [validators.Length(min=1, max=150), validators.DataRequired()])
    slideshow1 = StringField('SlideShow 1', [validators.Length(min=1, max=150), validators.DataRequired()])
    slideshow2 = StringField('SlideShow 2', [validators.Length(min=1, max=150), validators.DataRequired()])
    slideshow3 = StringField('SlideShow 3', [validators.Length(min=1, max=150), validators.DataRequired()])
    category = StringField('Category', [validators.Length(min=1, max=150), validators.DataRequired()])

class PaymentGateway(Form):
    fullName = StringField('Full Name (on the card)', [validators.Length(min=1, max=150), validators.DataRequired()])
    cardnumber = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()])
    exp_month = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()])
    exp_year = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()])
    cvv = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()])

class myAccountForm(Form):
    userName = StringField('Username')
    oldPassword = StringField('Current Password')
    newPassword = StringField('New Password', [validators.Length(min=1, max=150), validators.DataRequired()])

class CreateRewardForm(Form):
 rewardName = StringField('Item Name', [validators.Length(min=1,max=150), validators.DataRequired()])
 incentive = StringField('S$ Off (Dollars)', [validators.Length(min=1,max=150), validators.DataRequired()])
 points = IntegerField('Points Required', [validators.NumberRange(min=1,max=9999), validators.DataRequired()])
 quantity = IntegerField('Quantity', [validators.NumberRange(min=1,max=9999), validators.DataRequired()])

class trackOrderForm(Form):
    transactionID = StringField('Transaction ID', [validators.Length(min=1,max=150), validators.DataRequired()])

class feedbackForm(Form):
    fullName = StringField('Full Name')
    userName = StringField('Username')
    email = StringField('Email')
    message = StringField('Message')
    status = StringField('Status')

class SupplierForm(Form):
    name = StringField('Supplier Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    items = StringField('Supplier Items (Seperate with commar ",")', [validators.Length(min=1, max=150), validators.DataRequired()])