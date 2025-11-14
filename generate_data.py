# generate_data.py
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

N_USERS = 120
N_PRODUCTS = 80
N_ORDERS = 300

# Users (with behavioral fields)
users = []
channels = ['organic','paid_search','referral','social','email']
devices = ['mobile','desktop','tablet']
for i in range(1, N_USERS+1):
    first = fake.first_name()
    last = fake.last_name()
    email = f"{first.lower()}.{last.lower()}{i}@example.com"
    signup = fake.date_between(start_date='-18M', end_date='-6M')
    last_login = signup + timedelta(days=random.randint(1, 540))
    users.append({
        "user_id": i,
        "name": f"{first} {last}",
        "email": email,
        "city": fake.city(),
        "signup_channel": random.choices(channels, weights=[40,20,10,20,10])[0],
        "device_type": random.choice(devices),
        "first_order_date": None,
        "last_login": last_login.isoformat()
    })

# Products (with sustainability and cost)
categories = ['electronics','home','apparel','books','health']
brands = ['Aster','Bellamy','Cores','Dovetail','Eon']
products = []
for i in range(1, N_PRODUCTS+1):
    price = round(random.uniform(5, 500), 2)
    cost = round(price * random.uniform(0.4,0.85), 2)
    products.append({
        "product_id": i,
        "product_name": f"{fake.word().capitalize()} {random.choice(['Pro','X','Lite','Plus',''])}".strip(),
        "brand": random.choice(brands),
        "category": random.choice(categories),
        "price": price,
        "cost_price": cost,
        "rating": round(random.uniform(2.5,5.0),1),
        "is_limited_edition": random.random() < 0.06,
        "sustainability_score": round(random.uniform(0,1),2)
    })

# Orders + order_items + payments
orders = []
order_items = []
payments = []
order_id = 1
oi_id = 1
for _ in range(N_ORDERS):
    user = random.choice(users)
    user_id = user['user_id']
    order_date = fake.date_between(start_date='-12M', end_date='today')
    num_items = random.choices([1,2,3,4], weights=[60,25,10,5])[0]
    order_total = 0
    discount = 0
    discount_code = None
    for _ in range(num_items):
        p = random.choice(products)
        qty = random.choices([1,1,1,2,3], weights=[60,20,10,5,5])[0]
        subtotal = p['price'] * qty
        order_total += subtotal
        order_items.append({
            "order_item_id": oi_id,
            "order_id": order_id,
            "product_id": p['product_id'],
            "quantity": qty,
            "unit_price": p['price'],
            "is_returned": random.random() < 0.03
        })
        oi_id += 1

    # random discount
    if random.random() < 0.12:
        discount = round(order_total * random.uniform(0.05, 0.25),2)
        discount_code = random.choice(['SUMMER','WELCOME','FLASH10','LOYALTY20'])

    shipping_type = random.choices(['standard','express','pickup'], weights=[70,25,5])[0]
    status = random.choices(['paid','pending','failed','refunded'], weights=[85,7,3,5])[0]

    payment_amount = round(order_total - discount, 2)
    orders.append({
        "order_id": order_id,
        "user_id": user_id,
        "order_date": order_date.isoformat(),
        "discount_code": discount_code,
        "discount_amount": discount,
        "shipping_type": shipping_type,
        "order_value": round(order_total,2)
    })
    payments.append({
        "payment_id": order_id,
        "order_id": order_id,
        "amount": payment_amount,
        "payment_method": random.choice(['card','netbank','wallet']),
        "status": status
    })
    order_id += 1

# events.csv for funnel
events = []
event_id = 1
event_types = ['page_view','add_to_cart','checkout','purchase']
for _ in range(900):
    u = random.choice(users)
    events.append({
        "event_id": event_id,
        "user_id": u['user_id'],
        "event_type": random.choices(event_types, weights=[70,15,10,5])[0],
        "event_time": fake.date_time_between(start_date='-12M', end_date='now').isoformat(),
        "page_url": fake.uri_path()
    })
    event_id += 1

# Update first_order_date in users
user_first = {}
for o in orders:
    uid = o['user_id']
    od = datetime.fromisoformat(o['order_date'])
    if uid not in user_first or od < user_first[uid]:
        user_first[uid] = od
for u in users:
    if u['user_id'] in user_first:
        u['first_order_date'] = user_first[u['user_id']].date().isoformat()

# Save CSVs
pd.DataFrame(users).to_csv('data/users.csv', index=False)
pd.DataFrame(products).to_csv('data/products.csv', index=False)
pd.DataFrame(orders).to_csv('data/orders.csv', index=False)
pd.DataFrame(order_items).to_csv('data/order_items.csv', index=False)
pd.DataFrame(payments).to_csv('data/payments.csv', index=False)
pd.DataFrame(events).to_csv('data/events.csv', index=False)

print("Generated CSVs in /data")
