import requests

URL = 'localhost:8888/tasks'

print(requests.get(URL))

# import requests

# url = 'localhost:8888/tasks'
# myobj = {'title': 'sdaflads', 'content': '123132'}

# x = requests.post(url, json = myobj)

# print(x.text)