import requests

BASE = "http://127.0.0.1:5000/"

data = {
    3: {"name": 'cool video', 'views': 200, "likes": 10},
    2: {"name": 'what do you want to do', 'views': 23, 'likes': 1},
    9: {"name": 'hello guys!', 'views': 23450, 'likes': 500}
}

patches = {
    3: {'name': 'bad video'},
    2: {'views': 200, 'likes': 32},
    9: {'likes': 32}
}

for k,v in data.items():
    response = requests.put(BASE + f"video/{k}", v)
    print(response.json())
    input()

for k,v in data.items():
    response = requests.put(BASE + f"video/{k}", v)
    print(response.json())
    input()

for k,v in data.items():
    response = requests.get(BASE + f"video/{k}")
    print(response.json())
    input()

for k,v in patches.items():
    response = requests.patch(BASE + f"video/{k}", v)
    print(response.json())
    input()

for k,v in data.items():
    response = requests.delete(BASE + f"video/{k}")
    print(response)
    input()

for k,v in data.items():
    response = requests.delete(BASE + f"video/{k}")
    print(response.json())
    input()