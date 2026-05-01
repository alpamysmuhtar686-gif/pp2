import math
from collections import deque
from datetime import datetime
import sys, shutil, os

import pygame


class Painter:
    def __init__(self):
        self.color = (0, 0, 255)
        self.tool = 'brush'
        self.text_font = pygame.font.SysFont(None, 32)

        # brush
        self.drawing = False
        self.current_stroke = []
        self.brush_size = 5

        # rectangle
        self.rect_start = None
        self.rect_current = None

        # circle
        self.circle_start = None
        self.circle_current = None

        # eraser
        self.eraser_radius = 20

        # square
        self.square_start = None
        self.square_current = None

        # right triangle
        self.rtri_start = None
        self.rtri_current = None

        # equilateral triangle
        self.etri_start = None
        self.etri_current = None

        # rhombus
        self.rhombus_start = None
        self.rhombus_current = None

        # line
        self.line_start = None
        self.line_current = None

        # text
        self.text_position = None
        self.text_buffer = ''
        self.text_active = False

    # ---------------- COLOR ----------------
    def set_color(self, key):
        if key == 'r':
            self.color = (255, 0, 0)
        elif key == 'g':
            self.color = (0, 255, 0)
        elif key == 'b':
            self.color = (0, 0, 255)
        elif key == 'w':
            self.color = (255, 255, 255)

    # ---------------- TOOL ----------------
    def set_tool(self, tool):
        self.tool = tool

    # ---------------- BRUSH ----------------
    def start_draw(self, pos):
        self.drawing = True
        self.current_stroke = [pos]

    def add_point(self, pos):
        if self.drawing:
            self.current_stroke.append(pos)

    def stop_draw(self, canvas):
        if not (self.drawing and self.current_stroke):
            self.drawing = False
            self.current_stroke = []
            return

        if len(self.current_stroke) == 1:
            point = self.current_stroke[0]
            color = (255, 255, 255) if self.tool == 'eraser' else self.color
            radius = self.eraser_radius // 2 if self.tool == 'eraser' else max(1, self.brush_size // 2)
            pygame.draw.circle(canvas, color, point, radius)
        else:
            color = (255, 255, 255) if self.tool == 'eraser' else self.color
            width = self.eraser_radius if self.tool == 'eraser' else self.brush_size
            for i in range(len(self.current_stroke) - 1):
                pygame.draw.line(
                    canvas,
                    color,
                    self.current_stroke[i],
                    self.current_stroke[i + 1],
                    width,
                )

        self.drawing = False
        self.current_stroke = []

    # ---------------- TEXT ----------------
    def start_text(self, pos):
        self.text_position = pos
        self.text_buffer = ''
        self.text_active = True

    def cancel_text(self):
        self.text_position = None
        self.text_buffer = ''
        self.text_active = False

    def commit_text(self, canvas):
        if self.text_active and self.text_position and self.text_buffer:
            text_surface = self.text_font.render(self.text_buffer, True, self.color)
            canvas.blit(text_surface, self.text_position)
        self.cancel_text()

    def handle_text_input(self, event, canvas):
        if self.tool != 'text' or not self.text_active:
            return False

        if event.key == pygame.K_RETURN:
            self.commit_text(canvas)
            return True

        if event.key == pygame.K_ESCAPE:
            self.cancel_text()
            return True

        if event.key == pygame.K_BACKSPACE:
            self.text_buffer = self.text_buffer[:-1]
            return True

        if event.unicode and event.unicode.isprintable():
            self.text_buffer += event.unicode
            return True

        return False

    # ---------------- Flood fill ----------------
    def flood_fill(self, pos, canvas):
        x, y = pos
        width, height = canvas.get_size()

        if x < 0 or x >= width or y < 0 or y >= height:
            return

        target_color = canvas.get_at((x, y))[:3]
        fill_color = self.color

        if target_color == fill_color:
            return

        queue = deque([(x, y)])

        while queue:
            px, py = queue.popleft()

            if px < 0 or px >= width or py < 0 or py >= height:
                continue

            if canvas.get_at((px, py))[:3] != target_color:
                continue

            canvas.set_at((px, py), fill_color)
            queue.append((px + 1, py))
            queue.append((px - 1, py))
            queue.append((px, py + 1))
            queue.append((px, py - 1))

    # ---------------- RECT ----------------
    def make_rect(self, start, end):
        x1, y1 = start
        x2, y2 = end

        x = min(x1, x2)
        y = min(y1, y2)
        w = abs(x2 - x1)
        h = abs(y2 - y1)

        return pygame.Rect(x, y, w, h)

    # ---------------- CIRCLE ----------------
    def make_radius(self, start, end):
        x1, y1 = start
        x2, y2 = end
        return int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)

    def mouse_down(self, pos, canvas=None):
        if self.tool == 'brush' or self.tool == 'eraser':
            self.start_draw(pos)

        elif self.tool == 'rect':
            self.rect_start = pos
            self.rect_current = pos

        elif self.tool == 'circle':
            self.circle_start = pos
            self.circle_current = pos

        elif self.tool == 'square':
            self.square_start = pos
            self.square_current = pos

        elif self.tool == 'rtriangle':
            self.rtri_start = pos
            self.rtri_current = pos

        elif self.tool == 'etriangle':
            self.etri_start = pos
            self.etri_current = pos

        elif self.tool == 'rhombus':
            self.rhombus_start = pos
            self.rhombus_current = pos

        elif self.tool == 'line':
            self.line_start = pos
            self.line_current = pos

        elif self.tool == 'text':
            self.start_text(pos)

        elif self.tool == 'fill' and canvas is not None:
            self.flood_fill(pos, canvas)

    def mouse_move(self, pos):
        if self.tool == 'brush' or self.tool == 'eraser':
            self.add_point(pos)

        elif self.tool == 'rect' and self.rect_start:
            self.rect_current = pos

        elif self.tool == 'circle' and self.circle_start:
            self.circle_current = pos

        elif self.tool == 'square' and self.square_start:
            self.square_current = pos

        elif self.tool == 'rtriangle' and self.rtri_start:
            self.rtri_current = pos

        elif self.tool == 'etriangle' and self.etri_start:
            self.etri_current = pos

        elif self.tool == 'rhombus' and self.rhombus_start:
            self.rhombus_current = pos

        elif self.tool == 'line' and self.line_start:
            self.line_current = pos

    def mouse_up(self, pos, canvas):
        if self.tool == 'brush' or self.tool == 'eraser':
            self.stop_draw(canvas)

        elif self.tool == 'rect' and self.rect_start:
            rect = self.make_rect(self.rect_start, pos)
            pygame.draw.rect(canvas, self.color, rect, self.brush_size)
            self.rect_start = None
            self.rect_current = None

        elif self.tool == 'circle' and self.circle_start:
            radius = self.make_radius(self.circle_start, pos)
            pygame.draw.circle(canvas, self.color, self.circle_start, radius, self.brush_size)
            self.circle_start = None
            self.circle_current = None

        elif self.tool == 'square' and self.square_start:
            square = self.make_square(self.square_start, pos)
            pygame.draw.rect(canvas, self.color, square, self.brush_size)
            self.square_start = None
            self.square_current = None

        elif self.tool == 'rtriangle' and self.rtri_start:
            tri = self.make_rtriangle(self.rtri_start, pos)
            pygame.draw.polygon(canvas, self.color, tri, self.brush_size)
            self.rtri_start = None
            self.rtri_current = None

        elif self.tool == 'etriangle' and self.etri_start:
            tri = self.make_etriangle(self.etri_start, pos)
            pygame.draw.polygon(canvas, self.color, tri, self.brush_size)
            self.etri_start = None
            self.etri_current = None

        elif self.tool == 'rhombus' and self.rhombus_start:
            rh = self.make_rhombus(self.rhombus_start, pos)
            pygame.draw.polygon(canvas, self.color, rh, self.brush_size)
            self.rhombus_start = None
            self.rhombus_current = None

        elif self.tool == 'line' and self.line_start:
            pygame.draw.line(canvas, self.color, self.line_start, pos, self.brush_size)
            self.line_start = None
            self.line_current = None

    # ---------------- DRAW ----------------
    def draw(self, surface):
        if self.tool in ('brush', 'eraser') and self.drawing:
            color = (255, 255, 255) if self.tool == 'eraser' else self.color
            width = self.eraser_radius if self.tool == 'eraser' else self.brush_size

            if len(self.current_stroke) == 1:
                radius = self.eraser_radius // 2 if self.tool == 'eraser' else max(1, self.brush_size // 2)
                pygame.draw.circle(surface, color, self.current_stroke[0], radius)
            else:
                for i in range(len(self.current_stroke) - 1):
                    pygame.draw.line(
                        surface,
                        color,
                        self.current_stroke[i],
                        self.current_stroke[i + 1],
                        width,
                    )

        if self.tool == 'rect' and self.rect_start and self.rect_current:
            rect = self.make_rect(self.rect_start, self.rect_current)
            pygame.draw.rect(surface, self.color, rect, self.brush_size)

        if self.tool == 'circle' and self.circle_start and self.circle_current:
            radius = self.make_radius(self.circle_start, self.circle_current)
            pygame.draw.circle(surface, self.color, self.circle_start, radius, self.brush_size)

        if self.tool == 'square' and self.square_start and self.square_current:
            square = self.make_square(self.square_start, self.square_current)
            pygame.draw.rect(surface, self.color, square, self.brush_size)

        if self.tool == 'rtriangle' and self.rtri_start and self.rtri_current:
            tri = self.make_rtriangle(self.rtri_start, self.rtri_current)
            pygame.draw.polygon(surface, self.color, tri, self.brush_size)

        if self.tool == 'etriangle' and self.etri_start and self.etri_current:
            tri = self.make_etriangle(self.etri_start, self.etri_current)
            pygame.draw.polygon(surface, self.color, tri, self.brush_size)

        if self.tool == 'rhombus' and self.rhombus_start and self.rhombus_current:
            rh = self.make_rhombus(self.rhombus_start, self.rhombus_current)
            pygame.draw.polygon(surface, self.color, rh, self.brush_size)

        if self.tool == 'line' and self.line_start and self.line_current:
            pygame.draw.line(surface, self.color, self.line_start, self.line_current, self.brush_size)

        if self.tool == 'text' and self.text_active and self.text_position:
            text_surface = self.text_font.render(self.text_buffer, True, self.color)
            surface.blit(text_surface, self.text_position)

            if (pygame.time.get_ticks() // 500) % 2 == 0:
                cursor_x = self.text_position[0] + text_surface.get_width()
                cursor_y = self.text_position[1]
                cursor_height = self.text_font.get_height()
                pygame.draw.line(
                    surface,
                    self.color,
                    (cursor_x, cursor_y),
                    (cursor_x, cursor_y + cursor_height),
                    2,
                )

        if self.tool == 'eraser':
            mx, my = pygame.mouse.get_pos()
            pygame.draw.circle(surface, (0, 0, 0), (mx, my), self.eraser_radius, 1)

    # square
    def make_square(self, start, end):
        x1, y1 = start
        x2, y2 = end

        side = min(abs(x2 - x1), abs(y2 - y1))

        # preserve direction (dragging left/up)
        x = x1 if x2 >= x1 else x1 - side
        y = y1 if y2 >= y1 else y1 - side

        return pygame.Rect(x, y, side, side)

    # right triangle
    def make_rtriangle(self, start, end):
        x1, y1 = start
        x2, y2 = end

        return [
            (x1, y1),
            (x1, y2),
            (x2, y2),
        ]

    def make_etriangle(self, start, end):
        x1, y1 = start
        x2, y2 = end

        side = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        height = (math.sqrt(3) / 2) * side
        sign = 1 if y2 >= y1 else -1

        p1 = (x1, y1)
        p2 = (x1 - side / 2, y1 + sign * height)
        p3 = (x1 + side / 2, y1 + sign * height)

        return [p1, p2, p3]

    def make_rhombus(self, start, end):
        x1, y1 = start
        x2, y2 = end

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        cx, cy = x1, y1

        return [
            (cx, cy - dy),
            (cx + dx, cy),
            (cx, cy + dy),
            (cx - dx, cy),
        ]

    # Get info
    def get_color(self):
        if self.color == (255, 0, 0):
            return 'red'
        elif self.color == (0, 255, 0):
            return 'green'
        elif self.color == (0, 0, 255):
            return 'blue'
        elif self.color == (255, 255, 255):
            return 'white'
        else:
            return 'None'

    def get_tool_type(self):
        return str(self.tool)


def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Mini Paint')

    clock = pygame.time.Clock()
    brush_size_info = {
        2: 'small (2)',
        5: 'medium (5)',
        10: 'large (10)',
    }
    canvas = pygame.Surface((800, 600))
    canvas.fill((255, 255, 255))
    painter = Painter()
    font = pygame.font.SysFont(None, 25)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if painter.handle_text_input(event, canvas):
                    continue

                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f'canvas_{timestamp}.png'
                    pygame.image.save(canvas, filename)
                    try:
                        os.mkdir("images")
                    except: pass
                    shutil.copy2(filename, f"images/{filename}")
                    os.remove(filename)
                    continue

                if event.key == pygame.K_r:
                    painter.set_color('r')
                elif event.key == pygame.K_g:
                    painter.set_color('g')
                elif event.key == pygame.K_b:
                    painter.set_color('b')
                elif event.key == pygame.K_w:
                    painter.set_color('w')

                if event.key == pygame.K_t:
                    painter.set_tool('rect')
                elif event.key == pygame.K_p:
                    painter.set_tool('brush')
                elif event.key == pygame.K_c:
                    painter.set_tool('circle')
                elif event.key == pygame.K_e:
                    painter.set_tool('eraser')
                elif event.key == pygame.K_s:
                    painter.set_tool('square')
                elif event.key == pygame.K_d:
                    painter.set_tool('rtriangle')
                elif event.key == pygame.K_f:
                    painter.set_tool('etriangle')
                elif event.key == pygame.K_h:
                    painter.set_tool('rhombus')
                elif event.key == pygame.K_l:
                    painter.set_tool('line')
                elif event.key == pygame.K_k:
                    painter.set_tool('fill')
                elif event.key == pygame.K_i:
                    painter.set_tool('text')

                if event.key == pygame.K_z:
                    painter.eraser_radius += 5
                elif event.key == pygame.K_x:
                    painter.eraser_radius = max(5, painter.eraser_radius - 5)

                if event.key == pygame.K_1:
                    painter.brush_size = 2
                elif event.key == pygame.K_2:
                    painter.brush_size = 5
                elif event.key == pygame.K_3:
                    painter.brush_size = 10

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    painter.mouse_down(event.pos, canvas)

            if event.type == pygame.MOUSEMOTION:
                painter.mouse_move(event.pos)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    painter.mouse_up(event.pos, canvas)

        screen.fill((255, 255, 255))
        screen.blit(canvas, (0, 0))
        painter.draw(screen)

        tool = painter.get_tool_type()
        if tool == 'brush':
            tool = 'brush (pencil)'

        tool_type = font.render(f'tool: {tool}', True, (0, 0, 0))
        current_color = font.render(f'color: {painter.get_color()}', True, (0, 0, 0))
        eraser_radius = font.render(f'Eraser radius: {painter.eraser_radius}', True, (0, 0, 0))
        screen.blit(tool_type, (5, 5))

        size_info = brush_size_info.get(painter.brush_size, 'N/A')
        size_text = font.render(f'size: {size_info}', True, (0, 0, 0))
        screen.blit(size_text, (5, 45))
        if painter.get_tool_type() == 'eraser':
            screen.blit(eraser_radius, (5, 25))
        else:
            screen.blit(current_color, (5, 25))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()