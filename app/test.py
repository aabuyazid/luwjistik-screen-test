import requests
from requests.auth import HTTPBasicAuth
from random import randint

BASE = "https://luwjistik-screen-test.herokuapp.com/"

orders = {
    'john': [
        {
            'weight': 5,
            'contact': 'john@gmail.com',
            'sender_addr': 'Paris, France',
            'receiv_addr': 'Nice, France'
        },
        {
            'weight': 1,
            'contact': 'john@gmail.com',
            'sender_addr': 'Paris, France',
            'receiv_addr': 'Lyon, France'
        }
    ],
    'helloworld': [
        {
            'weight': 2,
            'contact': 'hello.world@gmail.com',
            'sender_addr': 'Jakarta, Indonesia',
            'receiv_addr': 'Suryabaya, Indonesia'
        },
        {
            'weight': 3,
            'contact': 'hello.world@gmail.com',
            'sender_addr': 'Jakarta, Indonesia',
            'receiv_addr': 'Palembang, Indonesia'
        }
    ],
    'monty': [
        {
            'weight': 7,
            'contact': 'monty@gmail.com',
            'sender_addr': 'Penang, Malaysia',
            'receiv_addr': 'Bangkok, Thailand'
        },
        {
            'weight': 3,
            'contact': 'monty@gmail.com',
            'sender_addr': 'Penang, Malaysia',
            'receiv_addr': 'Kuala Lumpur, Malaysia'
        }
    ],
    'python': [
        {
            'weight': 4,
            'contact': 'python@gmail.com',
            'sender_addr': 'Tokyo, Japan',
            'receiv_addr': 'Osaka, Japan'
        },
        {
            'weight': 6,
            'contact': 'python@gmail.com',
            'sender_addr': 'Tokyo, Japan',
            'receiv_addr': 'Seoul, Korea'
        }
    ]
}

passwords = {
    'john': 'smithy123',    'helloworld': 'thefirst',
    'monty':'python',       'python': 'monty'
}

ids = {
    'john': [],             'helloworld': [],
    'monty': [],            'python': []
}

for user in orders:
    for order in orders[user]:
        response = requests.post(BASE + 'order', order,
            auth = HTTPBasicAuth(user, passwords[user]))
        resjson = response.json()
        ids[user].append(resjson['id'])
        print(response.json())
        input()

print(ids)

for user in orders:
    for order, id in zip(orders[user], ids[user]):
        response = requests.get(BASE + f'order/{id}',
            auth = HTTPBasicAuth(user, passwords[user]))
        print(response.json())
        input()

for user in orders:
    for order, id in zip(orders[user], ids[user]):
        response = requests.get(BASE + f'order/{randint(0,127)}',
            auth = HTTPBasicAuth(user, passwords[user]))
        print(response.json())
        input()

for user in orders:
    for order, id in zip(orders[user], ids[user]):
        response = requests.get(BASE + f'order/{id}',
            auth = HTTPBasicAuth('john', 'smithy123'))
        print(response.json())
        input()