# small launcher (just imports ui.app and runs)

import pygame
from ui.app import run_app

if __name__ == "__main__":
    pygame.init()
    try:
        run_app(1280, 900, title="Garden Algorithm Sorter")
    finally:
        pygame.quit()