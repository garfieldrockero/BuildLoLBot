from PIL import Image 
from PIL import ImageDraw

img1 = Image.open(r"background.png") 

img2 = Image.open(r"imagen1.png") 


img1.paste(img2, (32,32)) 

width, height = img1.size
text_x_percent = 0.20  
text_y_percent = 0.75  


text_x = int(text_x_percent * width)
text_y = int(text_y_percent * height)

draw = ImageDraw.Draw(img1)

draw.text((text_x, text_y), "Nombre del objeto", fill=(255, 255,255))


img1.save('result.png')
