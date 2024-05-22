from PIL import Image, ImageDraw, ImageFont
import os

def create_template_build(template_width, template_height, num_columns, num_rows, image_width, image_height, image_names_row1, image_names_row2, image_names_row3,image_names_row4, row_texts,image_path):
    
    #template = Image.new('RGBA', (template_width, template_height), color=(0,0,0,0)) #272727'
    template = Image.open('new_background.png', 'r')

    horizontal_space = (template_width - num_columns * image_width) // (num_columns + 15)
    vertical_space = (template_height - num_rows * image_height) // (num_rows + 4)
    # Constant to adjust the image
    const_image = 65 #65
    const_vertical_space = 50 #15
    const_x_text = 798
    const_horizontal_space = 50
    
    #Font
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 20)
    
    #x_image = horizontal_space
    y_image = vertical_space - const_vertical_space
    directory_path = './imagenes_items_modificadas'  # Directorio donde se encuentran las imágenes

    # Función interna para pegar imágenes de una fila
    def paste_images(image_names, y_start):
        x_image = horizontal_space - const_horizontal_space
        for image_name in image_names:
            image_path = os.path.join(directory_path, image_name + '.png')
            try:
                with Image.open(image_path) as image:
                    image = image.convert("RGBA") 
                    image = image.resize((image_width, image_height), resample=Image.LANCZOS)  # Redimensionar la imagen al tamaño requerido
            except FileNotFoundError:
                print(f"No se pudo encontrar la imagen {image_name}. Asegúrate de que esté en el directorio correcto.")
                continue
            template.paste(image, (x_image, y_start), image)
            
            x_image += image_width + horizontal_space

    paste_images(image_names_row1, y_image + const_image)
    y_image += image_height + vertical_space - const_vertical_space
    paste_images(image_names_row2, y_image + const_image)
    y_image += image_height + vertical_space - const_vertical_space
    paste_images(image_names_row3, y_image + const_image)
    y_image += image_height + vertical_space - const_vertical_space 
    paste_images(image_names_row4, y_image + const_image)
    
    draw = ImageDraw.Draw(template)
    for i, row_text in enumerate(row_texts):
        text_width, text_height = textsize(row_text, font=font)
        text_x = (template_width - text_width - const_x_text) // 2
        text_y = (vertical_space - const_vertical_space) * (i + 1) + image_height * i + image_height // 2 - text_height // 2
        draw.text((text_x, text_y), row_text, fill='white', font=font)
    
    image_path = image_path + ".WebP"
    template.save(image_path, "WebP", lossless = True)
    print("Plantilla creada exitosamente.")
    return image_path

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

def create_template_runes():
    hola = ''
