# gradient background

import pygame
from ui.theme import HOT_PINK, SUN_YELLOW, CANDY_PINK, LILAC, TANGERINE, BG_BASE

def draw_gradient_background(surf):
    """Draw a subtle gradient background"""
    w, h = surf.get_size()
    
    # Simple vertical gradient
    for y in range(h):
        ratio = y / h
        # Blend from light pink to light cream
        r = int(255 * (1 - ratio * 0.1))
        g = int(249 * (1 - ratio * 0.05))
        b = int(243 * (1 - ratio * 0.02))
        color = (r, g, b)
        pygame.draw.line(surf, color, (0, y), (w, y))