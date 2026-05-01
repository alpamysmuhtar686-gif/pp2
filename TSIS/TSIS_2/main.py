import math
from collections import deque
from datetime import datetime
import sys, shutil, os
from tools import Painter
import pygame
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
                    painter.save_canvas(canvas)

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