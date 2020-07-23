import shelve
import os
import json
from Member import Member
import webEngine
from Receipt import Receipt
from Transaction import Transaction
from Admin import Admin
from datetime import datetime
import shelve
from Reward import Reward
from Form import UserForm, LoginForm, AddProduct, PaymentGateway, myAccountForm, CreateRewardForm, trackOrderForm


# s = shelve.open('db/products.db')
# keys = list(s.keys())

# for key in keys:
#     print(s[key])

# s.close()

# data = {'framesets' : ['sku-GrzZTn', 'sku-IQHKIe', 'sku-MVTMyB', 'sku-GTvULx', 'sku-rOpDMG', 'sku-HsTpMk'],
#         'helmets' : ['sku-dxqnIz', 'sku-LzRnzf', 'sku-jkqxCC', 'sku-AnxwRF', 'sku-iNlJkM', 'sku-nvZtwq'],
#         'saddles' : ['sku-FmxSEv', 'sku-ZpQXSr', 'sku-jiVFHy', 'sku-tjLtMQ', 'sku-IfxwkK', 'sku-jtYxJM'],
#         'wheels' : ['sku-nFPKJk', 'sku-lidgVC', 'sku-mTqmtj', 'sku-jXGpVM', 'sku-KeiQjq', 'sku-okYaQt']}

# file = open('categoryMap.txt', 'w')
# file.write(json.dumps(data))
# # file = file.read()
# # file = json.loads(file)
# file.close()



s = shelve.open('db/feedback.db')

for key in s:
    if key != 'member-9251a3':
        del s[key]

s.close()