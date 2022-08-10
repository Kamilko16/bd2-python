import os
import pygame

images = {}

files = os.listdir('images')


def loadresources():
    for file in files:
        curr = images
        name = str.split(file, '.')
        name_parts = str.split(name[0], '_')
        for part in name_parts:
            if name_parts.index(part) < (len(name_parts) - 1):
                if curr.get(part) is None:
                    curr[part] = {}
                curr = curr[part]

            else:
                curr[part] = pygame.image.load(os.path.join('images', file))
                if name[1] == 'bmp':
                    curr[part].set_colorkey((255, 0, 255))
                if part == 'normal':

                    curr['normal'] = curr['normal'].convert_alpha()

                    img = pygame.surfarray.pixels_alpha(curr['normal'])

                    alpha = pygame.surfarray.pixels3d(curr['alpha'])

                    for x in range(0, img.shape[0]):
                        for y in range(0, img.shape[1]):
                            img[x, y] = alpha[x, y, 0]
