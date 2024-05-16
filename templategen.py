from PIL import Image, ImageDraw, ImageFont
import os

def create_template(template_width, template_height, num_columns, num_rows, image_width, image_height, image_names, row_texts):
    template = Image.new('RGB', (template_width, template_height), color='#272727')
    
    horizontal_space = (template_width - num_columns * image_width) // (num_columns + 1)
    vertical_space = (template_height - num_rows * image_height) // (num_rows + 1)
    
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 20)
    
    x_image = horizontal_space
    y_image = vertical_space
    x_text = horizontal_space
    y_text = 10
    directory_path = './imagenes_items_modificadas'  # Directorio donde se encuentran las imágenes

    for i, image_name in enumerate(image_names):
        if i < len(image_names):
            image_path = os.path.join(directory_path, image_name + '.png')
            try:
                with Image.open(image_path) as image:
                    image = image.convert("RGB")  # Convertir la imagen a RGB para asegurar que se pueda guardar como JPEG
                    image = image.resize((image_width, image_height), resample=Image.LANCZOS)  # Redimensionar la imagen al tamaño requerido
            except FileNotFoundError:
                print(f"No se pudo encontrar la imagen {image_name}. Asegúrate de que esté en el directorio correcto.")            
            template.paste(image, (x_image, (y_image + 75)))
        
        x_image += image_width + horizontal_space
        
        if (i + 1) % num_columns == 0 or i == len(image_names) - 1:
            y_image += image_height + vertical_space
            x_image = horizontal_space
    
    draw = ImageDraw.Draw(template)
    for i, row_text in enumerate(row_texts):
        text_width, text_height = textsize(row_text, font=font)
        text_x = (template_width - text_width) // 2
        text_y = vertical_space * (i + 1) + image_height * i + image_height // 2 - text_height // 2
        
        draw.text((text_x, text_y), row_text, fill='white', font=font)
    image_path = "final_imagen"
    template.save(image_path, "PNG")
    print("Plantilla creada exitosamente.")

    return image_path

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

"""template_width = 1080  # Ancho de la imagen final
template_height = 720  # Alto de la imagen final
image_width = 128  # Ancho de cada imagen en la plantilla
image_height = 128  # Alto de cada imagen en la plantilla
num_columns = 6  # Número de columnas de imágenes
num_rows = 4  # Número de filas de imágenes
directory_path = './pruebas'  # Directorio donde se encuentran las imágenes
image_names = ['imagen1.png', 'imagen2.png']  # Lista de nombres de archivos de imágenes
row_texts = ['Fase Inicial', 'Early Game', 'Mid Game', 'Late Game']  # Array de textos por fila"""

#template = create_template(template_width, template_height, num_columns, num_rows, image_width, image_height, image_names, row_texts)

"""if template:
    # Guardar la plantilla resultante
    template.save('image_template_with_text.jpg')
    print("Plantilla creada exitosamente.")"""
