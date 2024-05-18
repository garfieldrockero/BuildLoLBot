from PIL import Image, ImageDraw, ImageFont
import os

def create_template(template_width, template_height, num_columns, num_rows, image_width, image_height, image_names_row1, image_names_row2, image_names_row3,image_names_row4, row_texts):
    
    template = Image.new('RGB', (template_width, template_height), color='#272727')
    horizontal_space = (template_width - num_columns * image_width) // (num_columns + 1)
    vertical_space = (template_height - num_rows * image_height) // (num_rows + 1)
    # Constant to adjust the image
    const_image = 65
    const_vertical_space = 15 
    
    #Font
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 20)
    
    x_image = horizontal_space
    y_image = vertical_space
    directory_path = './imagenes_items_modificadas'  # Directorio donde se encuentran las imágenes

    # Función interna para pegar imágenes de una fila
    def paste_images(image_names, y_start):
        x_image = horizontal_space
        for image_name in image_names:
            image_path = os.path.join(directory_path, image_name + '.png')
            try:
                with Image.open(image_path) as image:
                    image = image.convert("RGB")  # Convertir la imagen a RGB para asegurar que se pueda guardar como JPEG
                    image = image.resize((image_width, image_height), resample=Image.LANCZOS)  # Redimensionar la imagen al tamaño requerido
            except FileNotFoundError:
                print(f"No se pudo encontrar la imagen {image_name}. Asegúrate de que esté en el directorio correcto.")
                continue
            template.paste(image, (x_image, y_start))
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
        text_x = (template_width - text_width) // 2
        text_y = (vertical_space - const_vertical_space) * (i + 1) + image_height * i + image_height // 2 - text_height // 2
        draw.text((text_x, text_y), row_text, fill='white', font=font)
    
    image_path = "final_imagen.png"
    template.save(image_path, "PNG")
    print("Plantilla creada exitosamente.")
    return image_path

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

# Example for test
"""template_width = 1080  # Ancho de la imagen final
template_height = 720  # Alto de la imagen final
image_width = 128  # Ancho de cada imagen en la plantilla
image_height = 128  # Alto de cada imagen en la plantilla
num_columns = 6  # Número de columnas de imágenes
num_rows = 4  # Número de filas de imágenes"""

"""mage_names_row1 = ['image1']
image_names_row2 = ['image2']
image_names_row3 = ['image3']
image_names_row4 = ['image3']

row_texts = ['Starter Phase','Early Phase' ,'Core Phase', 'Late Phase']  # Array de textos por fila """

#create_template(template_width, template_height, num_columns, num_rows, image_width, image_height, image_names_row1, image_names_row2, image_names_row3, row_texts)
