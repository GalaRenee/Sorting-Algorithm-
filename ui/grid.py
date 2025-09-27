import pygame
from ui.theme import FLOWERS, TEXT_DARK, STROKE_PINK

def build_grid(area, rows, cols, gap):
    cells = []
    x, y, w, h = area
    
    # Leave space for title and algorithm text
    title_space = 80  # Space for both title and algorithm text
    usable_area = pygame.Rect(x, y + title_space, w, h - title_space)
    
    # Add small padding around the grid
    padding = 15
    grid_area = usable_area.inflate(-padding * 2, -padding * 2)
    
    # Calculate cell dimensions - RECTANGULAR not square
    available_w = grid_area.w - gap * (cols - 1)  # Space minus gaps
    available_h = grid_area.h - gap * (rows - 1)  # Space minus gaps
    
    cell_w = available_w // cols
    cell_h = available_h // rows
    
    # Ensure minimum readable size but stay within bounds
    cell_w = max(cell_w, 70)  # Minimum width
    cell_h = max(cell_h, 65)  # Minimum height
    
    # Recalculate if cells are too big for the area
    total_grid_w = cols * cell_w + (cols - 1) * gap
    total_grid_h = rows * cell_h + (rows - 1) * gap
    
    if total_grid_w > grid_area.w:
        cell_w = (grid_area.w - gap * (cols - 1)) // cols
    if total_grid_h > grid_area.h:
        cell_h = (grid_area.h - gap * (rows - 1)) // rows
    
    # Center the grid within the available area
    total_grid_w = cols * cell_w + (cols - 1) * gap
    total_grid_h = rows * cell_h + (rows - 1) * gap
    start_x = grid_area.x + (grid_area.w - total_grid_w) // 2
    start_y = grid_area.y + (grid_area.h - total_grid_h) // 2
    
    # Create all 16 cells (4x4 grid)
    for row in range(rows):
        for col in range(cols):
            cell_x = start_x + col * (cell_w + gap)
            cell_y = start_y + row * (cell_h + gap)
            cells.append(pygame.Rect(cell_x, cell_y, cell_w, cell_h))
    
    return cells

def draw_flower_cell(screen, rect, flower_type, font, highlighted=False):
    color = (255, 230, 245) if highlighted else (255, 255, 255)
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, STROKE_PINK, rect, width=2, border_radius=12)
    
    _, name = FLOWERS[flower_type]
    
    # Scale font sizes based on cell size - make text bigger since no emoji anymore 
    text_size = max(14, min(rect.width // 6, rect.height // 4))
    
    text_font = pygame.font.Font(None, text_size)
    name_surface = text_font.render(name, True, TEXT_DARK)
    name_rect = name_surface.get_rect(center=rect.center)
    
    screen.blit(name_surface, name_rect)