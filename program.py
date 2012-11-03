import Image, ImageFont, ImageDraw, ImageEnhance, os

def test():
    batch("./in", "./out/", "./template/default/header.png", "./template/default/footer.png")

def scale((width,height),(max_width,max_height)):
  new_width = max_width
  new_height = int(round(((height * max_width) / width),0))
  if new_height > max_height:
    width = new_width
    height = new_height
    new_height = max_height
    new_width = int(round(((width * max_height) / height),0))

  return ((new_width,new_height))

def draw_canvas(base_image_path, header_path, footer_path, output_dir):
  try:
    DPI = 200
    canvas_size = (11*DPI,int(8.5*DPI)) #8.5x11 letter size with 200 pixels per inch
    header_size = (canvas_size[0],int(0.3*DPI))
    footer_size = (canvas_size[0],int(1.7*DPI))
    content_size = (canvas_size[0],int(6.5*DPI))
    canvas = Image.new('RGBA', canvas_size, (255,255,255,0))
    
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
    
#     font = ImageFont.truetype('/Library/Fonts/Hoefler Text.ttc',100)
#     txt_draw = ImageDraw.Draw(footer)
#     txt_draw.text((10,10),'ccccccccc',fill=(255,0,0,0), font=font)
    


    base_image = Image.open(base_image_path)
    if base_image.mode != 'RGBA':
      base_image = base_image.convert('RGBA')
    base_image = base_image.resize(scale(base_image.size,content_size))
    canvas.paste(base_image,(int((canvas.size[0]-base_image.size[0])/2),header.size[1]+1))
        
#     txtimg = Image.new('RGBA',(150,50),(0,0,0,0))
#     txtimg_drawer = ImageDraw.Draw(txtimg)
#     txtimg_drawer.text((5,20),'aaaaa')
#     canvas.paste(txtimg,(10,10))

#     font = ImageFont.load("arial.pil")
#     image = Image.new("RGBA", (288,432), (255,255,255))
#     usr_font = ImageFont.truetype("resources/HelveticaNeueLight.ttf", 25)
#     d_usr = ImageDraw.Draw(image)
#     d_usr = d_usr.text((105,280), "Travis L.",(0,0,0), font=usr_font)
    
    

    #Image.composite(canvas, base_image, canvas).save(os.path.join(output_dir, os.path.basename(base_image_path)))
    canvas.save(os.path.join(output_dir, os.path.basename(base_image_path)))
  except Exception, (msg):
    print msg

def batch(infolder, outfolder, header_path, footer_path):
    for root, dirs, files in os.walk(infolder):
        for name in files:
          draw_canvas(os.path.join(root, name), header_path, footer_path, outfolder)

if __name__ == '__main__':
    test()