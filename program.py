import Image, ImageFont, ImageDraw, os
font = ImageFont.truetype('/Library/Fonts/Hoefler Text.ttc',100)
DPI = 200
canvas_size = (11*DPI,int(8.5*DPI)) #8.5x11 letter size with 200 pixels per inch
header_size = (canvas_size[0],int(0.3*DPI))
footer_size = (canvas_size[0],int(1.7*DPI))
content_size = (canvas_size[0],int(6.5*DPI))

def test():
    batch("./in", "./out/", "./templates/default/header.png", "./templates/default/footer.png", "./templates/default/text.txt")

def scale_image((max_width,max_height), image):
  width = image.size[0]
  height = image.size[1]
  new_width = max_width
  new_height = int(round(((height * max_width) / width),0))
  if new_height > max_height:
    width = new_width
    height = new_height
    new_height = max_height
    new_width = int(round(((width * max_height) / height),0))
  image = image.resize((new_width,new_height))
  return image

def open_image(image_path):
  image = Image.open(image_path)
  if image.mode != 'RGBA':
    image = image.convert('RGBA')
  return image

def draw_canvas(base_image_path, header_path, footer_path, canvas):
  header = open_image(header_path)
  header = scale_image(header_size,header)
  canvas.paste(header,(int((canvas.size[0]-header.size[0])/2),0))
      
  footer = open_image(footer_path)
  footer = scale_image(footer_size,footer)
  canvas.paste(footer,(int((canvas.size[0]-footer.size[0])/2),canvas.size[1]-footer.size[1]))

  base_image = open_image(base_image_path)
  base_image = scale_image(content_size,base_image)    
  canvas.paste(base_image,(int((canvas.size[0]-base_image.size[0])/2),header.size[1]+1))

def draw_text(text_path,canvas):
  txt_draw = ImageDraw.Draw(canvas)
  file = open(text_path, 'rb')
  for line in file.readlines():
    fields = line.rstrip().split('|||')
    txt_draw.text((int(fields[1]),int(fields[2])),fields[0],fill=(0,0,0), font=font)  
  file.close()

def batch(input_dir, output_dir, header_path, footer_path, text_path):
  for root, dirs, files in os.walk(input_dir):
    for name in files:
      if name != '.DS_Store':
        canvas = Image.new('RGBA', canvas_size, (255,255,255))
        draw_canvas(os.path.join(root, name), header_path, footer_path, canvas)
        draw_text(text_path,canvas)
        canvas.save(os.path.join(output_dir, name))

if __name__ == '__main__':
    test()

#     Image.composite(canvas, base_image, canvas).save(os.path.join(output_dir, os.path.basename(base_image_path)))