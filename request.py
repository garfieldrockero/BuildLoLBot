import requests

#test Riot API 
url = "https://ddragon.leagueoflegends.com/cdn/14.9.1/data/en_US/item.json"

response = requests.get(url)
data = response.json()

for id, item in data["data"].items():
    nombre = item["name"]
    print(f"ID: {id}, Nombre: {nombre}")
