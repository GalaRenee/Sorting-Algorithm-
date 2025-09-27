 # main entry point 
import pygame
import math
import time
from ui.theme import BG, PANEL, STROKE_PINK, STROKE_LILAC, STROKE_ORANGE, STROKE_YEL, TEXT_DARK, FLOWERS
from ui.button import Button
from ui.panel import draw_panel
from ui.layout import compute_areas, layout_row
from ui.grid import build_grid, draw_flower_cell
from ui.graph import draw_perf_panel
from ui.state import initial_state, switch_mode, shuffle, new_dataset
from ui.graph import draw_complexity_visualization
from algos import get_generator
from ui.grid import build_grid, draw_flower_cell

ALGO_LABELS = [
    "Bubble Sort","Insertion Sort","Merge Sort",
    "Quick Sort","Heap Sort","Counting Sort",
    "Radix Sort","Bucket Sort","Quick Select Sort",
]

def draw_gradient_background(surface):
    w, h = surface.get_size()
    for y in range(h):
        ratio = y / h
        r = int(255 * (1 - ratio * 0.1))
        g = int(240 + ratio * 15)
        b = int(245 - ratio * 20)
        color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
        pygame.draw.line(surface, color, (0, y), (w, y))

def count_progressive_flowers(flowers):
    """Count flowers progressively based on how sorted the array is"""
    n = len(flowers)
    if n == 0:
        return [0, 0, 0, 0]
    
    # Count how many elements are in their correct final position
    sorted_array = sorted(flowers)
    correct_positions = 0
    
    for i in range(n):
        if flowers[i] == sorted_array[i]:
            correct_positions += 1
    
    # Calculate progress as percentage of completion
    progress = correct_positions / n
    
    # Count total flowers of each type
    total_counts = [flowers.count(i) for i in range(4)]
    
    # Return progressive counts based on how much is sorted
    progressive_counts = []
    for i in range(4):
        # Show collected flowers based on progress, starting from 0
        progressive_count = int(total_counts[i] * progress)
        progressive_counts.append(progressive_count)
    
    return progressive_counts

def draw_sorting_boxes(screen, boxes_area, font, flowers):
    box_colors = [
        ((255, 230, 245), (247, 155, 195)),
        ((255, 245, 230), (255, 109, 24)),
        ((255, 255, 230), (255, 183, 0)),
        ((245, 230, 255), (168, 85, 247))
    ]
    
    gap = 15
    box_w = (boxes_area.w - 3 * gap) // 4 - 10
    box_h = boxes_area.h - 20
    
    start_x = boxes_area.x + 5
    start_y = boxes_area.y + 15
    
    progressive_counts = count_progressive_flowers(flowers)
    
    for i in range(4):
        x = start_x + i * (box_w + gap)
        y = start_y
        box_rect = pygame.Rect(x, y, box_w, box_h)
        
        bg_color, border_color = box_colors[i]
        
        pygame.draw.rect(screen, bg_color, box_rect, border_radius=12)
        pygame.draw.rect(screen, border_color, box_rect, width=2, border_radius=12)
        
        emoji, name = FLOWERS[i]
        header_font_size = max(16, min(20, box_w // 8))
        header_font = pygame.font.Font(None, header_font_size)
        title_text = header_font.render(f"{emoji} {name} Box", True, TEXT_DARK)
        title_rect = title_text.get_rect(center=(box_rect.centerx, box_rect.y + box_h * 0.2))
        screen.blit(title_text, title_rect)
        
        count = progressive_counts[i]
        total_count = flowers.count(i)
        
        badge_w = min(50, box_w - 10)
        badge_h = min(20, box_h // 6)
        count_badge = pygame.Rect(box_rect.centerx - badge_w//2, box_rect.y + box_h * 0.35, badge_w, badge_h)
        pygame.draw.rect(screen, border_color, count_badge, border_radius=8)
        
        count_font_size = max(12, min(16, box_w // 10))
        count_font = pygame.font.Font(None, count_font_size)
        count_text = count_font.render(f"{count} / {total_count}", True, (255, 255, 255))
        count_text_rect = count_text.get_rect(center=count_badge.center)
        screen.blit(count_text, count_text_rect)
        
        circle_size = max(6, min(10, box_w // 15))
        circles_per_row = 2
        circle_spacing = max(15, box_w // 8)
        
        start_circle_x = box_rect.centerx - circle_spacing // 2
        start_circle_y = box_rect.y + box_h * 0.6
        
        for row in range(2):
            for col in range(2):
                circle_x = start_circle_x + col * circle_spacing
                circle_y = start_circle_y + row * (circle_spacing * 0.8)
                circle_color = border_color if count > (row * 2 + col) else (200, 200, 200)
                pygame.draw.circle(screen, circle_color, (int(circle_x), int(circle_y)), circle_size)       
 
def draw_performance_screen(screen, W, H, stats, algorithm, font_title, font_ui):
    """Draw the performance analysis screen with enhanced timing information"""
    draw_gradient_background(screen)
    
    # Back button
    back_button = pygame.Rect(50, 50, 100, 40)
    pygame.draw.rect(screen, (247, 155, 195), back_button, border_radius=12)
    pygame.draw.rect(screen, STROKE_PINK, back_button, width=2, border_radius=12)
    back_text = font_ui.render("← Back", True, TEXT_DARK)
    screen.blit(back_text, back_text.get_rect(center=back_button.center))
    
    # Title
    title = font_title.render("📊 Algorithm Performance Analysis", True, TEXT_DARK)
    screen.blit(title, title.get_rect(center=(W//2, 100)))
    
    if algorithm:
        algo_text = font_ui.render(f"Algorithm: {algorithm}", True, TEXT_DARK)
        screen.blit(algo_text, algo_text.get_rect(center=(W//2, 140)))
    
    # Enhanced performance stats with timing
    stats_y = 200
    box_w = 150
    gap = 40
    start_x = (W - (4 * box_w + 3 * gap)) // 2
    
    colors = [(255, 230, 245), (255, 245, 230), (245, 230, 255), (230, 255, 245)]
    strokes = [(247, 155, 195), (255, 183, 77), (215, 125, 246), (34, 197, 94)]
    labels = ["Steps", "Comparisons", "Swaps", "Time (ms)"]
    
    # Format time nicely
    time_value = stats.get("time", 0)
    time_display = f"{time_value*1000:.1f}" if time_value > 0 else "0.0"
    
    values = [
        str(stats.get("steps", 0)), 
        str(stats.get("comparisons", 0)), 
        str(stats.get("swaps", 0)),
        time_display
    ]
    
    for i in range(4):
        box_rect = pygame.Rect(start_x + i*(box_w + gap), stats_y, box_w, 80)
        pygame.draw.rect(screen, colors[i], box_rect, border_radius=16)
        pygame.draw.rect(screen, strokes[i], box_rect, width=2, border_radius=16)
        
        big_font = pygame.font.Font(None, 36)
        val_text = big_font.render(values[i], True, TEXT_DARK)
        label_text = font_ui.render(labels[i], True, (120, 95, 140))
        
        screen.blit(val_text, val_text.get_rect(center=(box_rect.centerx, box_rect.y + 25)))
        screen.blit(label_text, label_text.get_rect(center=(box_rect.centerx, box_rect.y + 55)))
    
    # Complexity info
    complexity_y = 320
    complexity_title = font_title.render("Big O Complexity Analysis", True, TEXT_DARK)
    screen.blit(complexity_title, complexity_title.get_rect(center=(W//2, complexity_y)))
    
    # Draw the complexity visualization
    chart_rect = pygame.Rect(150, complexity_y + 50, W-300, 300)
    draw_complexity_visualization(screen, chart_rect, algorithm, font_ui)
    
    return back_button

def run_app(W, H, title="Dreamy Garden Sorter"):
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()
    
    title_font = pygame.font.Font(None, 42)
    h2_font = pygame.font.Font(None, 24)
    ui_font = pygame.font.Font(None, 20)
    cell_font = pygame.font.Font(None, 16)
    
    L = compute_areas(W, H)
    st = initial_state("garden")
    st["current_screen"] = "main"
    
    # Algorithm buttons
    algo_inner = L["algo"].inflate(-20, -15)
    row1 = layout_row(pygame.Rect(algo_inner.x, algo_inner.y + 10, algo_inner.w, 60), 5, 15, item_h=55)
    row2 = layout_row(pygame.Rect(algo_inner.x, algo_inner.y + 80, algo_inner.w, 60), 4, 15, item_h=55)
    algo_rects = row1 + row2
    algo_buttons = [Button(label, r, ui_font, (255,255,255), STROKE_PINK) for label, r in zip(ALGO_LABELS, algo_rects)]
    
    # Action buttons
    action_inner = L["action"].inflate(-30, -10)
    action_rects = layout_row(action_inner, 4, gap=15, item_h=50)
    btn_start = Button("🚀 Start", action_rects[0], ui_font, (247, 155, 195), STROKE_PINK)
    btn_shuffle = Button("🔀 Shuffle", action_rects[1], ui_font, (255, 190, 120), STROKE_ORANGE)
    btn_new = Button("✨ New", action_rects[2], ui_font, (235, 220, 255), STROKE_LILAC)
    btn_perf = Button("📊 Show Performance", action_rects[3], ui_font, (235, 240, 255), STROKE_YEL)
    
    # Grid with better proportions
    cells = build_grid(L["grid"], rows=4, cols=4, gap=15)
    gen = None
    highlighted_cells = set()
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        mouse = pygame.mouse.get_pos()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
                
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if st["current_screen"] == "performance":
                    # Check back button on performance screen
                    back_button = pygame.Rect(50, 50, 100, 40)
                    if back_button.collidepoint(ev.pos):
                        st["current_screen"] = "main"
                
                elif st["current_screen"] == "main":
                    for b in algo_buttons:
                        if b.hit(ev.pos):
                            for x in algo_buttons: 
                                x.selected = False
                            b.selected = True
                            st["algorithm"] = b.label
                    
                    if btn_start.hit(ev.pos) and not st["sorting"] and st["algorithm"]:
                        # Reset stats before starting new sort
                        st["stats"] = {"steps": 0, "comparisons": 0, "swaps": 0, "time": 0}
                        gen = get_generator(st["algorithm"], st["arr"])
                        st["sorting"] = True
                        
                    elif btn_shuffle.hit(ev.pos) and not st["sorting"]:
                        shuffle(st)
                        
                    elif btn_new.hit(ev.pos) and not st["sorting"]:
                        new_dataset(st)
                        
                    elif btn_perf.hit(ev.pos):
                        st["current_screen"] = "performance"
        
        # Update buttons only on main screen
        if st["current_screen"] == "main":
            for b in algo_buttons + [btn_start, btn_shuffle, btn_new, btn_perf]:
                b.update(mouse, dt)
            
            # Step sorting with enhanced timing
            highlighted_cells.clear()
            if st["sorting"] and gen:
                try:
                    arr, meta = next(gen)
                    st["arr"] = arr
                    
                    # Update all statistics including timing
                    st["stats"]["steps"] = meta.get("steps", st["stats"]["steps"])
                    st["stats"]["comparisons"] = meta.get("comparisons", st["stats"]["comparisons"])
                    st["stats"]["swaps"] = meta.get("swaps", st["stats"]["swaps"])
                    st["stats"]["time"] = meta.get("time", st["stats"]["time"])
                    
                    if "compare" in meta:
                        highlighted_cells.update(meta["compare"])
                    if "swap" in meta:
                        highlighted_cells.update(meta["swap"])
                    if "highlight" in meta:  # For non-comparison sorts
                        highlighted_cells.update(meta["highlight"])
                        
                    if meta.get("done"):
                        st["sorting"] = False
                        gen = None
                        highlighted_cells.clear()
                        print(f"Sorting completed! Final stats: {st['stats']}")  # Debug info
                        
                except StopIteration:
                    st["sorting"] = False
                    gen = None
        
        # DRAW based on current screen
        if st["current_screen"] == "performance":
            draw_performance_screen(screen, W, H, st["stats"], st["algorithm"], title_font, ui_font)
        
        else:  # main screen
            draw_gradient_background(screen)
            
            title_text = title_font.render("🌸 Dreamy Garden Sorter ", True, TEXT_DARK)
            screen.blit(title_text, title_text.get_rect(center=(W//2, 30)))
            
            subtitle = h2_font.render("Choose your magical sorting algorithm", True, (210, 120, 160))
            screen.blit(subtitle, subtitle.get_rect(center=(W//2, 55)))
            
            draw_panel(screen, L["algo"], PANEL, STROKE_PINK)
            for b in algo_buttons:
                b.draw(screen)
                
            draw_panel(screen, L["action"], PANEL, STROKE_PINK)
            btn_start.draw(screen)
            btn_shuffle.draw(screen)
            btn_new.draw(screen)
            btn_perf.draw(screen)
            
            draw_panel(screen, L["grid"], (255,250,253), STROKE_PINK)
            
            grid_title = h2_font.render("🌸 Mixed Dreamy Garden", True, TEXT_DARK)
            grid_title_rect = grid_title.get_rect(center=(L["grid"].centerx, L["grid"].y + 25))
            screen.blit(grid_title, grid_title_rect)
            
            if st["algorithm"]:
                algo_text = ui_font.render(f"Algorithm: {st['algorithm']}", True, TEXT_DARK)
                algo_text_rect = algo_text.get_rect(center=(L["grid"].centerx, L["grid"].y + 50))
                screen.blit(algo_text, algo_text_rect)
            
            # Show real-time stats during sorting
            if st["sorting"] or any(v > 0 for v in st["stats"].values()):
                stats_text = ui_font.render(
                    f"Steps: {st['stats']['steps']} | Comparisons: {st['stats']['comparisons']} | Swaps: {st['stats']['swaps']} | Time: {st['stats']['time']*1000:.1f}ms", 
                    True, TEXT_DARK
                )
                stats_rect = stats_text.get_rect(center=(L["grid"].centerx, L["grid"].y + 75))
                screen.blit(stats_text, stats_rect)
            
            for idx, cell in enumerate(cells):
                if idx < len(st["arr"]):
                    flower_type = st["arr"][idx]
                    highlighted = idx in highlighted_cells
                    draw_flower_cell(screen, cell, flower_type, cell_font, highlighted)
            
            draw_sorting_boxes(screen, L["boxes"], ui_font, st["arr"])
            
        pygame.display.flip()