import hashlib
import bitstring
import pygame


def get_rgb(hsh):
    hsh = hsh.copy()
    return hsh.read(f"uint:8"), hsh.read(f"uint:8"), hsh.read(f"uint:8")


def get_hex(hsh):
    r, g, b = get_rgb(hsh)
    return hex_2_digits(format(r, "x")).upper(), hex_2_digits(format(g, "x").upper()), hex_2_digits(format(b, "x").upper())


def hex_2_digits(h):
    return ("0" * (2 - len(h))) + h


if __name__ == '__main__':
    s = input("Enter a String: ")
    hsh = bitstring.BitStream(hashlib.sha256(s.encode()).digest())

    r, g, b = get_rgb(hsh)
    hr, hg, hb = get_hex(hsh)

    print(f"RGB: {r} {g} {b}")
    print(f"HEX: #{hr}{hg}{hb}")

    pygame.init()
    display_size = (800, 600)
    screen = pygame.display.set_mode(display_size, pygame.RESIZABLE)
    pygame.display.set_caption("Text to Color - " + s)
    font = pygame.font.SysFont(None, 80)

    running = True
    while running:
        screen.fill((r, g, b))

        text = font.render(s, True, (255, 255, 255))
        text_x = (display_size[0] - text.get_width()) / 2
        text_y = (display_size[1] - text.get_height()) / 2
        screen.blit(text, (text_x, text_y))

        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.VIDEORESIZE:
                display_size = e.w, e.h
