import pygame
import textobject

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    running = True

    write = textobject.create_multiline_writing_text_object("Text line one lorem ipsum dolor sit amet\nText line two consectetur adipiscing elit\nText line three shorter sed do eiusmod", 1)
    write.set_position((200, 200))

    group = pygame.sprite.Group()
    group.add(write)

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                write.force_complete()

        # Update
        group.update()
        
        # Draw
        screen.fill(pygame.Color(120, 50, 50, 255))
        group.draw(screen)

        pygame.display.flip()
        clock.tick(60)
        


if __name__ == "__main__":
    main()