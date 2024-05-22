import os
import requests
from PIL import Image 
from PIL import ImageDraw

# Test Riot API
url_version = "https://ddragon.leagueoflegends.com/api/versions.json"
response_version = requests.get(url_version).json()[0]

url = "https://ddragon.leagueoflegends.com/cdn/" + response_version +"/data/en_US/item.json"
response = requests.get(url)
data = response.json()

input_folder = "imagenes_items"
output_folder = "imagenes_items_modificadas"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

image_files = os.listdir(input_folder)

for image_file in image_files:
    try:
        input_image_path = os.path.join(input_folder, image_file)

        #img1 = Image.open(r"background.png")
        img1 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        item_id = os.path.splitext(image_file)[0]

        item_name = data["data"][item_id]["name"]

        img2 = Image.open(input_image_path)

        img1.paste(img2, (32, 32))

        width, height = img1.size

        text_x_percent = 0.20  
        text_y_percent = 0.75  

        text_x = int(text_x_percent * width)
        text_y = int(text_y_percent * height)

        draw = ImageDraw.Draw(img1)

        draw.text((text_x, text_y), item_name, fill=(255, 255, 255))

        file_name_without_extension = os.path.splitext(image_file)[0]

        output_image_path = os.path.join(output_folder, f"{item_name}.png")
        img1.save(output_image_path)

        print(f"Imagen modificada guardada en: {output_image_path} Con el ID: {item_id}")
    except Exception as e:
        print(f"Error al procesar la imagen {image_file}: {e}")

print("Todas las imágenes han sido modificadas exitosamente.")
