# colors, fonts, stroke widths, etc.
import pygame

def hexrgb(h: str) -> tuple[int, int, int]:
    h = h.strip().lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# Pastel palette
HOT_PINK    = hexrgb("#E800B5")
SUN_YELLOW  = hexrgb("#FFB700")
CANDY_PINK  = hexrgb("#FF9DE2")
LILAC       = hexrgb("#D77DF6")
TANGERINE   = hexrgb("#FF6D18")
BG_BASE     = hexrgb("#FFF7FC")

# Base colors
BG = hexrgb("#FFF9F3")
PANEL = hexrgb("#FFF5FB")
STROKE_PINK   = hexrgb("#FF9DE2")
STROKE_LILAC  = hexrgb("#D77DF6")
STROKE_ORANGE = hexrgb("#FF6D18")
STROKE_YEL    = hexrgb("#FFB700")

TEXT_DARK = (45, 20, 60)

# FIXED: Flower mapping with both emoji and name (this was the main issue!)
FLOWERS = {
    0: ("🌹", "Rose"),
    1: ("🌷", "Tulip"), 
    2: ("🌼", "Daisy"),
    3: ("🌸", "Cherry Blossom")
}