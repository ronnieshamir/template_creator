import Image, ImageFont, ImageDraw, ImageEnhance, os
font = ImageFont.truetype('/Library/Fonts/Hoefler Text.ttc',100)
DPI = 200
canvas_size = (11*DPI,int(8.5*DPI)) #8.5x11 letter size with 200 pixels per inch
header_size = (canvas_size[0],int(0.3*DPI))
footer_size = (canvas_size[0],int(1.7*DPI))
content_size = (canvas_size[0],int(6.5*DPI))

def test():
    batch("./in", "./out/", "./templates/default/header.png", "./templates/default/footer.png")

def scale((width,height),(max_width,max_height)):
  new_width = max_width
  new_height = int(round(((height * max_width) / width),0))
  if new_height > max_height:
    width = new_width
    height = new_height
    new_height = max_height
    new_width = int(round(((width * max_height) / height),0))

  return ((new_width,new_height))

def draw_canvas(base_image_path, header_path, footer_path, output_dir, canvas):
  header = Image.open(header_path)
  if header.mode != 'RGBA':
    header = header.convert('RGBA')
  header = header.resize(scale(header.size,header_size))
  canvas.paste(header,(int((canvas.size[0]-header.size[0])/2),0))
      
  footer = Image.open(footer_path)
  if footer.mode != 'RGBA':
    footer = footer.convert('RGBA')
  footer = footer.resize(scale(footer.size,footer_size))
  canvas.paste(footer,(int((canvas.size[0]-footer.size[0])/2),canvas.size[1]-footer.size[1]))

  base_image = Image.open(base_image_path)
  if base_image.mode != 'RGBA':
    base_image = base_image.convert('RGBA')
  base_image = base_image.resize(scale(base_image.size,content_size))    
  canvas.paste(base_image,(int((canvas.size[0]-base_image.size[0])/2),header.size[1]+1))

def batch(input_dir, output_dir, header_path, footer_path):
  for root, dirs, files in os.walk(input_dir):
    for name in files:
      if name != '.DS_Store':
        canvas = Image.new('RGBA', canvas_size, (255,255,255))
        draw_canvas(os.path.join(root, name), header_path, footer_path, output_dir, canvas)

        txt_draw = ImageDraw.Draw(canvas)
        file = open('test.txt', 'rb')
        while(1):
          line = file.readline()
          if not line:
            break
          fields = line.rstrip().split('|||')
          txt_draw.text((int(fields[1]),int(fields[2])),fields[0],fill=(0,0,0), font=font)        

        canvas.save(os.path.join(output_dir, name))



if __name__ == '__main__':
    test()

#     Image.composite(canvas, base_image, canvas).save(os.path.join(output_dir, os.path.basename(base_image_path)))