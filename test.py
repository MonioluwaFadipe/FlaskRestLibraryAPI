from urllib import response
import requests

BASE = "http://127.0.0.1:5000/"

response = requests.patch(BASE + "book/1", {"author":"No"})
print(response.json())
