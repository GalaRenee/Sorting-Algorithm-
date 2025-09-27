import pygame
from ui.theme import TEXT_DARK, STROKE_LILAC

class Button:
    def __init__(self, label, rect, font, fill, stroke, radius=16, hover_scale=1.06):
        self.label = label 
        self.base_rect = pygame.Rect(rect)
        self.font = font 
        self.fill = fill 
        self.stroke = stroke 
        self.radius = radius
        self.hover_scale = hover_scale
        self.selected = False
        self._hover = 0.0 
        
    @property
    def rect(self):
        if self._hover <= 0:
            return self.base_rect
        r = self.base_rect.copy()
        scale = 1.0 + (self.hover_scale - 1.0) * self._hover
        r.width  = int(self.base_rect.w * scale)
        r.height = int(self.base_rect.h * scale)
        r.center = self.base_rect.center
        return r
    
    def update(self, mouse_pos, dt):
        inside = self.base_rect.collidepoint(mouse_pos)
        target = 1.0 if inside else 0.0
        if target > self._hover:
            self._hover = min(1.0, self._hover + dt*10)
        else:
            self._hover = max(0.0, self._hover - dt*8)
            
    def draw(self, surf):
        stroke_color = STROKE_LILAC if self.selected else self.stroke
        pygame.draw.rect(surf, self.fill, self.rect, border_radius=self.radius)
        pygame.draw.rect(surf, stroke_color, self.rect, width=2, border_radius=self.radius)
        txt = self.font.render(self.label, True, TEXT_DARK)
        surf.blit(txt, txt.get_rect(center=self.rect.center))
        
    def hit(self, pos):
        return self.rect.collidepoint(pos)