import requests

BASE = "http://127.0.0.1:5000/"

response = requests.delete(BASE + "deleteDestination/1/'Abu Simbel Temple'")
print(response.json())
print("Maii")