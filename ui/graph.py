import pygame
import math
from ui.theme import STROKE_PINK, TEXT_DARK

def draw_perf_panel(surf, rect, panel_fill, stroke, font, stats):
    """Enhanced performance panel with complexity info"""
    pygame.draw.rect(surf, panel_fill, rect, border_radius=20)
    pygame.draw.rect(surf, stroke, rect, width=2, border_radius=20)
    
    # Title
    title_font = pygame.font.Font(None, 24)
    title = title_font.render("📊 ✨ Algorithm Performance", True, (70, 30, 70))
    title_rect = title.get_rect(center=(rect.centerx, rect.y + 20))
    surf.blit(title, title_rect)
    
    subtitle = font.render("Real-time complexity visualization", True, (120, 95, 140))
    subtitle_rect = subtitle.get_rect(center=(rect.centerx, rect.y + 40))
    surf.blit(subtitle, subtitle_rect)
    
    # Three stat boxes in top row
    gap = 15
    box_w = (rect.w - 60 - 2*gap) // 3
    box_h = 60
    start_x = rect.x + 30
    
    colors = [(255, 230, 245), (255, 245, 230), (245, 230, 255)]
    strokes = [(247, 155, 195), (255, 183, 77), (215, 125, 246)]
    labels = ["Steps", "Comparisons", "Swaps"]
    values = [str(stats.get("steps", 0)), str(stats.get("comparisons", 0)), str(stats.get("swaps", 0))]
    
    for i in range(3):
        box_rect = pygame.Rect(start_x + i*(box_w + gap), rect.y + 55, box_w, box_h)
        
        pygame.draw.rect(surf, colors[i], box_rect, border_radius=12)
        pygame.draw.rect(surf, strokes[i], box_rect, width=2, border_radius=12)
        
        # Large number
        big_font = pygame.font.Font(None, 32)
        val_text = big_font.render(values[i], True, (45, 20, 60))
        val_rect = val_text.get_rect(center=(box_rect.centerx, box_rect.y + 20))
        surf.blit(val_text, val_rect)
        
        # Label
        label_text = font.render(labels[i], True, (120, 95, 140))
        label_rect = label_text.get_rect(center=(box_rect.centerx, box_rect.y + 45))
        surf.blit(label_text, label_rect)

def draw_complexity_visualization(screen, rect, algorithm_name, font):
    """Draw a visual complexity chart with enhanced hover information and working graphs"""
    
    # Algorithm complexity data
    complexity_info = {
        "Bubble Sort": ("O(n²)", "O(1)", "Comparison-based", "Learning", (255, 100, 100)),
        "Insertion Sort": ("O(n²)", "O(1)", "Comparison-based", "Small datasets", (255, 150, 100)),
        "Merge Sort": ("O(n log n)", "O(n)", "Comparison-based", "Large datasets", (100, 255, 100)),
        "Quick Sort": ("O(n log n)", "O(log n)", "Comparison-based", "General purpose", (100, 255, 150)),
        "Heap Sort": ("O(n log n)", "O(1)", "Comparison-based", "Memory constrained", (150, 255, 100)),
        "Counting Sort": ("O(n + k)", "O(k)", "Non-comparison", "Integer sorting", (100, 150, 255)),
        "Radix Sort": ("O(d × n)", "O(n + k)", "Non-comparison", "Integer sorting", (150, 100, 255)),
        "Bucket Sort": ("O(n + k)", "O(n)", "Distribution", "Uniform data", (255, 100, 255)),
        "Quick Select Sort": ("O(n)", "O(log n)", "Comparison-based", "Finding kth element", (255, 255, 100))
    }
    
    if algorithm_name not in complexity_info:
        # Draw error message if algorithm not found
        error_font = pygame.font.Font(None, 24)
        error_text = error_font.render(f"No complexity data for: {algorithm_name}", True, (255, 100, 100))
        error_rect = error_text.get_rect(center=rect.center)
        screen.blit(error_text, error_rect)
        return
        
    time_comp, space_comp, algo_type, best_for, color = complexity_info[algorithm_name]
    
    # Draw main chart area - FIXED: Proper background
    chart_inner = rect.inflate(-40, -40)
    pygame.draw.rect(screen, (255, 255, 255), chart_inner, border_radius=16)
    pygame.draw.rect(screen, STROKE_PINK, chart_inner, width=2, border_radius=16)
    
    # Title
    title_font = pygame.font.Font(None, 24)
    title = title_font.render("Algorithm Complexity Visualization", True, TEXT_DARK)
    title_rect = title.get_rect(center=(chart_inner.centerx, chart_inner.y + 30))
    screen.blit(title, title_rect)
    
    # Draw complexity info boxes - FIXED: Better positioning
    info_y = chart_inner.y + 70
    info_boxes = [
        (f"Time: {time_comp}", (255, 230, 245), (247, 155, 195)),
        (f"Space: {space_comp}", (255, 245, 230), (255, 183, 77)),
        (f"Type: {algo_type}", (245, 230, 255), (215, 125, 246)),
        (f"Best for: {best_for}", (230, 255, 245), (34, 197, 94))
    ]
    
    box_w = (chart_inner.w - 80 - 3*15) // 4
    for i, (text, bg_color, border_color) in enumerate(info_boxes):
        box_rect = pygame.Rect(chart_inner.x + 40 + i*(box_w + 15), info_y, box_w, 40)
        
        pygame.draw.rect(screen, bg_color, box_rect, border_radius=8)
        pygame.draw.rect(screen, border_color, box_rect, width=1, border_radius=8)
        
        text_font = pygame.font.Font(None, 16)
        text_surface = text_font.render(text, True, TEXT_DARK)
        text_rect = text_surface.get_rect(center=box_rect.center)
        screen.blit(text_surface, text_rect)
    
    # FIXED: Working graph area
    graph_area = pygame.Rect(chart_inner.x + 40, info_y + 60, chart_inner.w - 80, chart_inner.h - 150)
    pygame.draw.rect(screen, (250, 250, 250), graph_area, border_radius=8)
    pygame.draw.rect(screen, (200, 200, 200), graph_area, width=1, border_radius=8)
    
    # FIXED: Working complexity curve visualization
    points = []
    data_points = []
    n_values = 20
    
    for i in range(n_values):
        n = i + 1
        x = graph_area.x + (i * graph_area.w) // (n_values - 1)
        
        # FIXED: Proper complexity calculations
        if "n²" in time_comp:
            time_value = n * n
            y_ratio = min(1.0, (i / n_values) ** 2)
        elif "n log n" in time_comp:
            if n > 1:
                time_value = n * math.log2(n)
                y_ratio = min(1.0, (i / n_values) * math.log2(max(2, i)) / 4)
            else:
                time_value = 1
                y_ratio = 0
        elif "n + k" in time_comp:
            k = 4  # Assume k=4 for visualization
            time_value = n + k
            y_ratio = min(1.0, (i / n_values) * 1.2)
        elif time_comp == "O(n)":
            time_value = n
            y_ratio = i / n_values
        else:  # Default linear
            time_value = n
            y_ratio = i / n_values
        
        y = graph_area.y + graph_area.h - int(y_ratio * (graph_area.h - 40)) - 20
        points.append((x, y))
        data_points.append((x, y, n, int(time_value)))
    
    # FIXED: Draw the curve properly
    if len(points) > 1:
        try:
            pygame.draw.lines(screen, color, False, points, 3)
        except:
            # Fallback if points are invalid
            for i in range(len(points) - 1):
                pygame.draw.line(screen, color, points[i], points[i+1], 3)
    
    # FIXED: Working hover detection
    mouse_pos = pygame.mouse.get_pos()
    hover_info = None
    
    for x, y, n, time_val in data_points:
        # Draw data points
        pygame.draw.circle(screen, color, (int(x), int(y)), 6)
        pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), 3)
        
        # Check for hover
        if abs(mouse_pos[0] - x) < 15 and abs(mouse_pos[1] - y) < 15:
            hover_info = (x, y, n, time_val)
    
    # FIXED: Working hover display
    if hover_info:
        hx, hy, n, time_val = hover_info
        
        hover_text = [
            f"Input Size: {n}",
            f"Operations: {time_val}",
            f"Algorithm: {algorithm_name}",
            f"Complexity: {time_comp}"
        ]
        
        hover_font = pygame.font.Font(None, 16)
        text_heights = [hover_font.get_height() for _ in hover_text]
        text_widths = [hover_font.size(text)[0] for text in hover_text]
        
        box_w = max(text_widths) + 20
        box_h = sum(text_heights) + 15
        
        # Position hover box
        box_x = min(hx + 15, screen.get_width() - box_w - 10)
        box_y = max(hy - box_h - 15, 10)
        
        hover_rect = pygame.Rect(box_x, box_y, box_w, box_h)
        
        # Draw hover box
        pygame.draw.rect(screen, (255, 255, 255), hover_rect, border_radius=8)
        pygame.draw.rect(screen, color, hover_rect, width=2, border_radius=8)
        
        # Draw hover text
        y_offset = 8
        for text in hover_text:
            text_surface = hover_font.render(text, True, TEXT_DARK)
            screen.blit(text_surface, (hover_rect.x + 10, hover_rect.y + y_offset))
            y_offset += hover_font.get_height()