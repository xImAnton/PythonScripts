import pygame


pygame.init()


class LineVisualizer:
    """
    class for managing line data and rendering
    """
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.pixmap = []
        self.x = 0
        self.y = 0
        for xx in range(self.dx + 1):
            yyy = []
            for yy in range(self.dy + 1):
                yyy.append(False)
            self.pixmap.append(yyy)
        self.running = False
        self.screen = None

    def recalc(self):
        """
        recalculates border margin and tile sizes
        """
        height = self.dy + 1
        width = self.dx + 1
        screen_w, screen_h = self.screen.get_width(), self.screen.get_height()
        # calculate the size of a tile
        self.rect_l = min((self.screen.get_height() - 20) // height, (self.screen.get_width() - 20) // width)
        # calculate the margin on the left and right
        self.margin_rl = (screen_w - (self.rect_l * width)) // 2
        # calculate the margin on the top and bottom
        self.margin_tb = (screen_h - (self.rect_l * height)) // 2
        # calculates the boundaries of the tile map in the middle of the window
        self.bounds = ((self.margin_rl, self.margin_tb), (self.rect_l * width + self.margin_rl, self.rect_l * height + self.margin_tb))

    def start(self):
        """
        starts the rendering of a line from the origin to the specified coordinates
        """

        # setup screen
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        self.recalc()
        self.running = True
        # calculate tiles that match the line
        self.bresenham_line()
        # render the line
        self.render()
        pygame.display.flip()
        while self.running:
            for event in pygame.event.get():
                # close on close
                if event.type == pygame.QUIT:
                    self.running = False
                # recalculate and rerender when the window size changes
                if event.type == pygame.VIDEORESIZE:
                    self.recalc()
                    self.render()
                    pygame.display.flip()

    def set_pixel(self, x, y):
        """
        inverts a pixel on the pixmap
        :param x: x coordinate of the pixel to change
        :param y: y coordinate of the pixel to change
        """
        self.pixmap[x][y] = not self.pixmap[x][y]

    def bresenham_line(self):
        """
        implementation of the bresenham algorithm to pick the pixels that are on the line
        """
        self.set_pixel(self.x, self.y)
        error = self.dx/2
        while self.x < self.dx:
            self.x += 1
            error -= self.dy
            if error < 0:
                self.y += 1
                error += self.dx
            self.set_pixel(self.x, self.y)

    def render(self):
        """
        render the current line and tilemap with spacings
        """
        height = self.dy + 1
        width = self.dx + 1
        # draw background of pixmap
        pygame.draw.rect(self.screen, (200, 200, 200), [self.margin_rl, self.margin_tb, self.rect_l * width, self.rect_l * height])
        for x in range(len(self.pixmap)):
            for y in range(len(self.pixmap[x])):
                # color the current pixel it is set
                if self.pixmap[x][y]:
                    pygame.draw.rect(self.screen, (67, 237, 55), (self.margin_rl + (x-1) * self.rect_l + self.rect_l, self.margin_tb + (y-1) * self.rect_l + self.rect_l, self.rect_l, self.rect_l))

        # draw vertical lines between tiles
        for x in range(len(self.pixmap) + 1):
            pygame.draw.line(self.screen, (255, 255, 255), (self.margin_rl + x * self.rect_l, self.margin_tb), (self.margin_rl + x * self.rect_l, self.bounds[1][1]), 1)
        # draw horizontal lines between tiles
        for y in range(len(self.pixmap[0]) + 1):
            pygame.draw.line(self.screen, (255, 255, 255), (self.margin_rl, self.margin_tb + y * self.rect_l), (self.bounds[1][0], self.margin_tb + y * self.rect_l), 1)
        # draw the specified line
        pygame.draw.line(self.screen, (0, 0, 0), (self.margin_rl + self.rect_l / 2, self.margin_tb + self.rect_l / 2), (self.bounds[1][0] - self.rect_l / 2, self.bounds[1][1] - self.rect_l / 2), 5)


def main():
    dx = int(input("X? "))
    dy = int(input("Y? "))
    if dy > dx:
        # swap values back when inverted
        dx, dy = dy, dx
    LineVisualizer(dx - 1, dy - 1).start()


if __name__ == '__main__':
    main()
