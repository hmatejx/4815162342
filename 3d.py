import struct
import pygame
from pygame.locals import *

import moderngl

pygame.init()

FPS=30
clock = pygame.time.Clock()

SUPERRES = 1
REAL_RES=(840, 567)
VIRTUAL_RES=(REAL_RES[0]*SUPERRES, REAL_RES[1]*SUPERRES)

screen = pygame.Surface(VIRTUAL_RES).convert((255, 65280, 16711680, 0))
pygame.display.set_mode(REAL_RES, DOUBLEBUF|OPENGL|RESIZABLE)

ctx = moderngl.create_context()

texture_coordinates = [0, 1,  1, 1,
                       0, 0,  1, 0]

world_coordinates = [-1, -1,  1, -1,
                     -1,  1,  1,  1]

render_indices = [0, 1, 2,
                  1, 2, 3]

prog = ctx.program(
    vertex_shader='''
#version 300 es
in vec2 vert;
in vec2 in_text;
out vec2 v_text;
void main() {
   gl_Position = vec4(vert, 0.0, 1.0);
   v_text = in_text;
}
''',

fragment_shader='''
#version 300 es
precision highp float;
uniform sampler2D Texture;

out vec4 color;
in vec2 v_text;
void main() {
  vec2 center = vec2(0.5, 0.5);
  vec2 off_center = v_text - center;

  off_center *= 1.0 + 0.5 * pow(abs(off_center.yx), vec2(2.5));

  vec2 v_text2 = center+off_center;

  if (v_text2.x > 1.0 || v_text2.x < 0.0 ||
      v_text2.y > 1.0 || v_text2.y < 0.0){
    color=vec4(0.0, 0.0, 0.0, 1.0);
  } else {
    color = vec4(texture(Texture, v_text2).rgb, 1.0);
    float fv = fract(v_text2.y * float(textureSize(Texture,0).y) / 3.0);
    fv = 1.0 - pow(abs(cos(3.1415926535*(fv - 5.0/6.0))), 2.5);
    color.rgb*=fv;
  }
}
''')

screen_texture = ctx.texture(
    VIRTUAL_RES, 3,
    pygame.image.tostring(screen, "RGB", 1))

screen_texture.repeat_x = False
screen_texture.repeat_y = False

vbo = ctx.buffer(struct.pack('8f', *world_coordinates))
uvmap = ctx.buffer(struct.pack('8f', *texture_coordinates))
ibo= ctx.buffer(struct.pack('6I', *render_indices))

vao_content = [
    (vbo, '2f', 'vert'),
    (uvmap, '2f', 'in_text')
]

vao = ctx.vertex_array(prog, vao_content, ibo)

def render():
    texture_data = screen.get_view('1')
    screen_texture.write(texture_data)
    ctx.clear()
    screen_texture.use()
    vao.render()
    pygame.display.flip()

#MAIN LOOP

done=False

while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

    screen.fill((0, 32, 0))
    divx = 16
    divy = 12
    xstep = (VIRTUAL_RES[0] - 1.0) / divx
    ystep = (VIRTUAL_RES[1] - 1.0) / divy
    font = pygame.font.Font("font/PrintChar21.ttf", 24*SUPERRES)
    text = font.render('>:4 8 15 16 23 42', 0, pygame.Color("#33ff33ff"))
    screen.blit(text, (0, 0))
    screen.blit(text, (20*21*SUPERRES,11*24*SUPERRES))
    #for i in range(0, 17):
    #    pygame.draw.line(screen, (0, 255, 0), (xstep*i, 0), (xstep*i, VIRTUAL_RES[1] - 1))
    #for i in range(0, 13):
    #    pygame.draw.line(screen, (0, 255, 0), (0, ystep*i), (VIRTUAL_RES[0] - 1, ystep*i))

    render()
    clock.tick(FPS)