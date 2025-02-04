C:\mygit\BLazy\repo\3dsim\main.py
Language detected: python
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import sys
import random

class Particle:
    def __init__(self, position):
        self.position = np.array(position, dtype=np.float32)
        self.velocity = np.array([0, 0, 0], dtype=np.float32)
        self.lifetime = random.uniform(2, 4)
        self.age = 0.0

    def update(self, dt, wind_effect):
        self.velocity += wind_effect * dt
        self.velocity *= 0.98  # Air resistance approximation
        self.position += self.velocity * dt
        self.age += dt

class Simulation:
    def __init__(self, width=1280, height=720):
        pygame.init()
        self.width = width
        self.height = height
        pygame.display.set_mode((self.width, self.height), DOUBLEBUF|OPENGL)
        glEnable(GL_DEPTH_TEST)
        gluPerspective(45, (self.width/self.height), 0.1, 100.0)
        
        self.cam_rot_x = 30
        self.cam_rot_y = 0
        self.cam_zoom = 15
        
        self.car_speed = 10.0        # m/s
        self.wind_speed = 2.0        # m/s
        self.air_density = 1.225     # kg/m3
        self.car_cd = 0.3           # Drag coefficient

        self.particles = []
        self.particle_spawn_rate = 20

    def _drag_force(self, velocity):
        return 0.5 * self.air_density * np.linalg.norm(velocity)**2 * self.car_cd * 2.0  # 2m2 cross-section

    def _emit_particles(self):
        for _ in range(self.particle_spawn_rate):
            pos = np.array([
                random.uniform(-1.0, 1.0),
                random.uniform(0.3, 1.2),
                random.uniform(-2.5, 2.5)
            ], dtype=np.float32)
            p = Particle(pos)
            base_flow = np.array([0, 0, self.car_speed + self.wind_speed])  # Wind + car movement effect
            p.velocity = base_flow + np.array([random.uniform(-1,1), random.uniform(-0.5,0.5), random.uniform(-1,1)])
            self.particles.append(p)

    def _update_particles(self, dt):
        for p in self.particles.copy():
            p.update(dt, np.array([0, -0.98, 0]))  # Simulating gravity
            if p.age >= p.lifetime or abs(p.position[2]) > 15:
                self.particles.remove(p)

    def _draw_car(self):
        glColor3f(0.2, 0.4, 1.0)
        # Car body
        glBegin(GL_QUADS)
        glVertex3f(-1.5, 0.0, -3.0)
        glVertex3f(1.5, 0.0, -3.0)
        glVertex3f(1.5, 1.0, 3.0)
        glVertex3f(-1.5, 1.0, 3.0)
        # Roof
        glVertex3f(-1.0, 1.0, -2.0)
        glVertex3f(1.0, 1.0, -2.0)
        glVertex3f(1.0, 1.8, 2.0)
        glVertex3f(-1.0, 1.8, 2.0)
        glEnd()

    def _draw_particles(self):
        glColor3f(0.8, 0.8, 0.8)
        glPointSize(2)
        glBegin(GL_POINTS)
        for p in self.particles:
            glVertex3fv(p.position)
        glEnd()

    def _draw_ui(self):
        from pygame.font import Font
        font = Font(None, 30)
        texts = [
            f"Car Speed: {self.car_speed:.1f} m/s (U/D)",
            f"Wind Speed: {self.wind_speed:.1f} m/s (J/K)",
            f"Air Density: {self.air_density:.1f} kg/m3 (L/M)",
            "[Arrows] Rotate View [PGUP/PGDN] Zoom"
        ]
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.width, self.height, 0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        for i, text in enumerate(texts):
            text_surface = font.render(text, True, (255, 255, 255))
            text_width = text_surface.get_width()
            text_height = text_surface.get_height()
            glRasterPos2d(10, 15 + i*30)
            for pixel in pygame.image.tostring(text_surface, 'RGBA', True):
                glDrawPixels(1, 1, GL_RGBA, GL_UNSIGNED_BYTE, bytes([pixel]))
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(60)/1000.0
            self._handle_input()
            self._emit_particles()
            self._update_particles(dt)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glTranslatef(0, -3, -self.cam_zoom)
            glRotatef(self.cam_rot_x, 1, 0, 0)
            glRotatef(self.cam_rot_y, 0, 1, 0)

            self._draw_car()
            self._draw_particles()
            self._draw_ui()
            pygame.display.flip()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.cam_rot_x += 5
                elif event.key == pygame.K_DOWN:
                    self.cam_rot_x -= 5
                elif event.key == pygame.K_LEFT:
                    self.cam_rot_y += 5
                elif event.key == pygame.K_RIGHT:
                    self.cam_rot_y -= 5
                elif event.key == pygame.K_PAGEUP:
                    self.cam_zoom = max(5, self.cam_zoom-2)
                elif event.key == pygame.K_PAGEDOWN:
                    self.cam_zoom += 2
                elif event.key == pygame.K_u:
                    self.car_speed += 1
                elif event.key == pygame.K_d:
                    self.car_speed = max(0, self.car_speed-1)
                elif event.key == pygame.K_j:
                    self.wind_speed += 1
                elif event.key == pygame.K_k:
                    self.wind_speed = max(0, self.wind_speed-1)
                elif event.key == pygame.K_l:
                    self.air_density += 0.1
                elif event.key == pygame.K_m:
                    self.air_density = max(0.1, self.air_density-0.1)

if __name__ == "__main__":
    sim = Simulation()
    sim.run()
