import requests
from bs4 import BeautifulSoup
import telebot
import json
from PIL import Image
import os

 
with open('token.json', 'r') as file:
    config = json.load(file)

# Telegram Token
TOKEN = config['telegram_token']

# Init bot
bot = telebot.TeleBot(TOKEN)
build_summoners = []
build_runes = []
build = []
titulos = ['Runas', 'Hechizos', 'Objetos']
url = ''
def scrape_build(champion_name, mode):
    # check the mode
    if mode.lower() == 'aram':
        url = 'https://mobalytics.gg/lol/champions/' + champion_name + '/aram-builds'
    else:
        url = 'https://mobalytics.gg/lol/champions/' + champion_name + '/build'
    print(url)


    response = requests.get(url)
    
    # Check 200 Status
    if response.status_code == 200:
        build =  []
        build_img = []
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # first Container
        build_container = soup.find_all('div', class_='m-owe8v3')
        print ('BUILD CONTAINER  '+ str(build_container))
        contador = 0
        for container in build_container:
            print('CONTADOR ' + str(contador))
            # limit 3 for no errors
            if contador < 3:
                # runes
                if contador == 0:
                    build_runes = container.find_all('img',class_= 'm-1nx2cdb')
                    build.append('\n' +titulos[contador])
                    for rune in build_runes:
                        build.append(rune['alt'])
                # summoners
                elif contador == 1:
                    build_summoners = container.find_all('img')
                    build.append('\n' +titulos[contador])
                    for summoners in build_summoners:
                            print(summoners['alt'])
                            build.append(summoners['alt'].replace("Summoner", ""))  
                # build
                else:
                    if container:
                        # Extraer los elementos de la build
                        build_items = container.find_all('img')
                        
                        # Imprimir los elementos de la build
                        print("Build de " + champion_name + ":")
                        build.append('\n' +titulos[contador])
                        for item in build_items:
                            print(item['alt'])
                            build.append(item['alt'])
                            build_img.append(item['alt'])
                    else:
                        print("No se encontró la información de la build.")
                contador += 1
        return build, build_img
    else:
        print("No se pudo obtener la página." + str(response))

def generate_Imagen(build_img):
    img_list = []
    for img_path in build_img:
        img_list.append(Image.open("imagenes_items_modificadas/" + img_path + ".png"))

    img_size = img_list[0].size

    total_width = max([img.size[0] for img in img_list]) * 4
    total_height = max([img.size[1] for img in img_list]) * 4
    new_im = Image.new('RGB', (total_width, total_height), (39, 39, 39))

    current_x = 0
    current_y = 0
    for img in img_list:
        new_im.paste(img, (current_x, current_y))
        current_x += img_size[0]
        if current_x >= total_width:
            current_x = 0
            current_y += img_size[1]

    image_path = "merged_images.png"
    new_im.save(image_path, "PNG")
    new_im.show()
    return image_path

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Envía /build seguido del nombre del campeón para obtener una build, si quieres que la build sea de ARAM añade al final del comando aram")

@bot.message_handler(commands=['build'])
def send_builds(message):

    msg = message.text.split(' ')  # split the message
    champion_name = msg[1]
    mode = ''
    if len(msg) == 3:
        mode = msg[2]
    builds, build_img = scrape_build(champion_name, mode)
    imagen = generate_Imagen(build_img)
    print('build!!!! ' + str(builds))
    builds = '\n'.join(builds)
    if builds:
        bot.reply_to(message, builds)
        with open(imagen, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.reply_to(message, f"No se pudieron encontrar builds para " +  champion_name + " en este momento.")

bot.polling()