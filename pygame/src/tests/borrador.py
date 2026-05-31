# Source - https://stackoverflow.com/a/46390412
# Posted by skrx, modified by community. See post 'Timeline' for change history
# Retrieved 2026-05-31, License - CC BY-SA 4.0
#
#mport pygame as pg
#
#
#g.init()
#creen = pg.display.set_mode((640, 480))
#OLOR_INACTIVE = pg.Color('lightskyblue3')
#OLOR_ACTIVE = pg.Color('dodgerblue2')
#ONT = pg.font.Font(None, 32)
#
#
#lass InputBox:
#
#   def __init__(self, x, y, w, h, text=''):
#       self.rect = pg.Rect(x, y, w, h)
#       self.color = COLOR_INACTIVE
#       self.text = text
#       self.txt_surface = FONT.render(text, True, self.color)
#       self.active = False
#
#   def handle_event(self, event):
#       if event.type == pg.MOUSEBUTTONDOWN:
#           # If the user clicked on the input_box rect.
#           if self.rect.collidepoint(event.pos):
#               # Toggle the active variable.
#               self.active = not self.active
#           else:
#               self.active = False
#           # Change the current color of the input box.
#           self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
#       if event.type == pg.KEYDOWN:
#           if self.active:
#               if event.key == pg.K_RETURN:
#                   print(self.text)
#                   self.text = ''
#               elif event.key == pg.K_BACKSPACE:
#                   self.text = self.text[:-1]
#               else:
#                   self.text += event.unicode
#               # Re-render the text.
#               self.txt_surface = FONT.render(self.text, True, self.color)
#
#   def update(self):
#       # Resize the box if the text is too long.
#       width = max(200, self.txt_surface.get_width()+10)
#       self.rect.w = width
#
#   def draw(self, screen):
#       # Blit the text.
#       screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y))
#       # Blit the rect.
#       pg.draw.rect(screen, self.color, self.rect, 2)
#
#
#
#ef main():
#   clock = pg.time.Clock()
#   input_box1 = InputBox(100, 100, 150, 50)
#   input_box2 = InputBox(100, 300, 140, 32, text="Hola")
#   input_boxes = [input_box1, input_box2]
#   done = False
#
#   while not done:
#       for event in pg.event.get():
#           if event.type == pg.QUIT:
#               done = True
#           for box in input_boxes:
#               box.handle_event(event)
#
#       for box in input_boxes:
#           box.update()
#
#       screen.fill((30, 30, 30))
#       for box in input_boxes:
#           box.draw(screen)
#
#       pg.display.flip()
#       clock.tick(30)
#
#
#f __name__ == '__main__':
#   main()
#   pg.quit()
#


abc = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
    'x', 'y', 'z'
]

text = "d234923d"

list_text = text.strip()


for character in list_text:
    for letter in abc:
        if character.lower() == letter:
            print("Hola")
