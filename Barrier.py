from pygame import *


class Barrier(sprite.Sprite):
    def __init__(self, size, color, row, column):
        sprite.Sprite.__init__(self)
        self.height = size
        self.width = size
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.row = row
        self.column = column

    def blitme(self):
        self.screen.blit(self.image, self.rect)