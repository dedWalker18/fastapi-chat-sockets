import requests

fodder_users = [
    {
        "id": 1,
        "name": "Peter Griffin",
        "username": "bigpapa",
        "email": "bigpapa@drunkenclam.com",
        "password": "asdf",
        "avatar": 1
    },
    {
        "id": 2,
        "name": "Brian Griffin",
        "username": "writerdog",
        "email": "novel4life@freebeers.com",
        "password": "asdf",
        "avatar": 2
    },
    {
        "id": 3,
        "name": "Stewie Griffin",
        "username": "stewie_g",
        "email": "supreme_overlord@stewieempire.com",
        "password": "asdf",
        "avatar": 3
    },
        {
        "id": 4,
        "name": "Lois Griffin",
        "username": "supermom",
        "email": "supermom@winemoms.com",
        "password": "asdf",
        "avatar": 4
    },
        {
        "id": 5,
        "name": "Glenn Quagmire",
        "username": "gigolo",
        "email": "giggity@mybigplane.com",
        "password": "asdf",
        "avatar": 5
    }
]

for user in fodder_users:
    response = requests.post("http://127.0.0.1:8000/users",json=user)
    print(response.text)