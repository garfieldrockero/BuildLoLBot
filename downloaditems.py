import os
import requests

# Test Riot API
url = "https://ddragon.leagueoflegends.com/cdn/14.9.1/data/en_US/item.json"

response = requests.get(url)
data = response.json()

# Carpeta donde se guardarán las imágenes
folder_path = "imagenes_items"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Iterar sobre los ítems y descargar las imágenes
for id, item in data["data"].items():
    nombre = item["name"]
    image_url = f"https://ddragon.leagueoflegends.com/cdn/14.9.1/img/item/{id}.png"
    
    # Descargar la imagen
    image_response = requests.get(image_url)
    
    # Guardar la imagen en la carpeta
    with open(os.path.join(folder_path, f"{id}.png"), 'wb') as f:
        f.write(image_response.content)
    
    print(f"Descargada imagen para el ítem ID: {id}, Nombre: {nombre}")

print("Todas las imágenes han sido descargadas exitosamente.")
