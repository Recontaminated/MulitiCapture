import pygame
import cv2
import numpy as np

def main():
    pygame.init()
    
    # Get the display info for Mac screen size
    display_info = pygame.display.Info()
    WINDOW_WIDTH = int(display_info.current_w * 0.8)  # 80% of screen width
    WINDOW_HEIGHT = int(display_info.current_h * 0.8)  # 80% of screen height
    
    # Create resizable window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("4-Camera View")
    
    # Track fullscreen state
    is_fullscreen = False

    # Initialize video captures (adjust indices as needed)
    cameras = []
    for i in range(4):
        cap = cv2.VideoCapture(i)
        if not cap.isOpened():
            print(f"Error: Could not open camera {i}")
            return
        cameras.append(cap)

    # Set lower resolution for capture cards
    for cap in cameras:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Calculate dimensions for each video feed
    feed_width = WINDOW_WIDTH // 2
    feed_height = WINDOW_HEIGHT // 2
    
    # Initialize clock for FPS tracking
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)  # Default font, size 36
    
    running = True
    while running:
        # Start of frame
        clock.tick()  # Track time since last frame
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:  # F11 to toggle fullscreen
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
            elif event.type == pygame.VIDEORESIZE and not is_fullscreen:
                WINDOW_WIDTH, WINDOW_HEIGHT = event.size
                screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
                
        # Recalculate feed dimensions based on current window size
        feed_width = screen.get_width() // 2
        feed_height = screen.get_height() // 2

        screen.fill((0, 0, 0))  # Clear screen

        # Process and display each camera feed
        for i, cap in enumerate(cameras):
            ret, frame = cap.read()
            if ret:
                # Calculate position for this feed
                x = (i % 2) * feed_width
                y = (i // 2) * feed_height

                # Optimize: Use faster interpolation method
                frame = cv2.resize(frame, (feed_width, feed_height), 
                                 interpolation=cv2.INTER_NEAREST)
                
                # Optimize: Convert directly to RGB without intermediate steps
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert to pygame surface more efficiently
                frame = np.rot90(frame)
                surface = pygame.surfarray.make_surface(frame)
                
                # Draw frame
                screen.blit(surface, (x, y))
                
                # Draw rectangle around feed
                rect_color = (255, 0, 0)  # Red
                rect_thickness = 3
                pygame.draw.rect(screen, rect_color, 
                               (x, y, feed_width, feed_height), 
                               rect_thickness)

        # Draw FPS counter in top left
        fps = int(clock.get_fps())
        fps_text = font.render(f'FPS: {fps}', True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

        pygame.display.flip()

    # Cleanup
    for cap in cameras:
        cap.release()
    pygame.quit()

if __name__ == "__main__":
    main()