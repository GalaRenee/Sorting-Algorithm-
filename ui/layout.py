import pygame

def compute_areas(W,H):
    """Compute layout areas for the garden sorter"""
    #adjust heights so boxes fit within reasonable screen bounds
    algo_h = 160       # Algorithm buttons
    action_h = 80      # Action buttons
    grid_h = 220       # Grid area
    boxes_h = 165      # Smaller boxes area so they fit on screen
    
    # Vertical spacing
    top_margin = 80   # Space for title 
    gap = 12          # Smaller gaps
    
    # Calculate y positions
    algo_y = top_margin
    action_y = algo_y + algo_h + gap
    grid_y = action_y + action_h + gap
    boxes_y = grid_y + grid_h + gap
    
    # Make sure boxes don't go off screen 
    if boxes_y + boxes_h > H - 20: # Leave 20px bottom margin 
        boxes_h = H - boxes_y - 20
        
    # Horizontal margins 
    margin = 40 
    
    return {
         "algo": pygame.Rect(margin, algo_y, W - 2*margin, algo_h),
        "action": pygame.Rect(margin, action_y, W - 2*margin, action_h),
        "grid": pygame.Rect(margin, grid_y, W - 2*margin, grid_h),
        "boxes": pygame.Rect(margin, boxes_y, W - 2*margin, boxes_h)
    }

def layout_row(rect, count, gap=10, item_h=None):
    """Layout items in a horizontal row with gaps"""
    if item_h is None:
        item_h = rect.h
        
    total_gap = gap * (count - 1)
    item_w (rect.w - total_gap) // count 
    
    rects = []
    for i in range(count):
        x = rect.x + 1 * (item_w + gap)
        y = rect.y + (rect.h - item_h) // 2 # Center vertically
        rects.append(pygame.Rect(x, y, item_w, item_h))
        
    return rects

def layout_grid(rect, rows, cols, gap=10):
    """Layout items in a grid with gaps"""
    h_gap = gap * (cols - 1)
    v_gap = gap * (rows - 1)
    
    item_w = (rect.w - h_gap) // cols
    item_h = (rect.h - v_gap) // rows
    
    rects = []
    for row in range(rows):
        for col in range(cols):
            x = rect.x + col * (item_w + gap)
            y = rect.y + row * (item_h + gap)
            rects.append(pygame.Rect(x, y, item_w, item_h))
            
    return rects