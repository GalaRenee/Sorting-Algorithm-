import pygame

def draw_panel(surf, rect, fill, stroke, radius=20, border=2):
    pygame.draw.rect(surf, fill, rect, border_radius=radius)
    pygame.draw.rect(surf, stroke, rect, width=border, border_radius=radius)