import pygame


def main():
    print("Launching Clutch Draw...")

    pygame.init()

    screen = pygame.display.set_mode((1280, 720))

    clock = pygame.time.Clock()

    # This happens once at the start not once per frame

    screen.fill("purple")  # Fill the display with a solid color

    # Everything inside the while loop happpens on every frame

    while True:

        # Process player inputs.
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                print("Got the quit event")
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                print(x, y)
                rect = pygame.Rect(x, y, 10, 10)
                pygame.draw.rect(screen, pygame.Color(255, 0, 0), rect)

        # Do logical updates here.
        # ...

        # Render the graphics here.
        # ...

        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)  # wait until next frame (at 60 FPS)


if __name__ == "__main__":
    main()
