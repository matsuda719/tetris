"""
Main entry point for the Simple Tetris game.
"""
import pygame
import sys
from src.game_engine import GameEngine
from src.game_display import GameDisplay


def main():
    """
    Main game loop.
    """
    # Initialize game components
    game_engine = GameEngine()
    game_display = GameDisplay()
    
    # Game loop variables
    clock = pygame.time.Clock()
    running = True
    
    # Input tracking for continuous movement
    keys_held = {
        'left': False,
        'right': False,
        'down': False,
        'up': False
    }
    
    try:
        while running:
            dt = clock.tick(60) / 1000.0  # Delta time in seconds
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    # Handle key press events - only set flags, don't move immediately
                    if event.key == pygame.K_LEFT:
                        keys_held['left'] = True
                    elif event.key == pygame.K_RIGHT:
                        keys_held['right'] = True
                    elif event.key == pygame.K_DOWN:
                        keys_held['down'] = True
                    elif event.key == pygame.K_UP:
                        keys_held['up'] = True
                    elif event.key == pygame.K_r and game_engine.game_over:
                        # Restart game
                        game_engine = GameEngine()
                
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        keys_held['left'] = False
                    elif event.key == pygame.K_RIGHT:
                        keys_held['right'] = False
                    elif event.key == pygame.K_DOWN:
                        keys_held['down'] = False
                    elif event.key == pygame.K_UP:
                        keys_held['up'] = False
            
            # Update game logic
            game_engine.update(dt)
            
            # Handle continuous input (for held keys)
            game_engine.handle_input(keys_held)
            
            # Render
            game_display.clear_screen()
            game_display.draw_board(game_engine.board)
            game_display.draw_piece(game_engine.current_piece)
            game_display.draw_next_piece(game_engine.next_piece)
            
            game_state = game_engine.get_game_state()
            game_display.draw_score(game_state['score'], game_state['lines_cleared'])
            
            if game_engine.game_over:
                game_display.draw_game_over()
            
            game_display.update_display()
    
    finally:
        game_display.quit()
        sys.exit()


if __name__ == "__main__":
    main()