C:\mygit\BLazy\repo\3dsim\main.py
Language detected: python
import pygame
import moderngl
import numpy as np
from pygame.locals import *
import time
import sys

# Camera parameters
class Camera:
    def __init__(self, width, height):
        self.position = np.array([0.0, 2.0, 5.0])
        self.front = np.array([0.0, 0.0, -1.0])
        self.up = np.array([0.0, 1.0, 0.0])
        self.right = np.array([1.0, 0.0, 0.0])
        self.yaw = -90.0
        self.pitch = 0.0
        self.speed = 2.5
        self.sensitivity = 0.1
        self.zoom = 45.0
        self.projection = np.perspective(np.radians(self.zoom), width/height, 0.1, 100.0)
    
    def look_at(self):
        return np.look_at(self.position, self.position + self.front, self.up)

# Simulation parameters
class SimulationParams:
    def __init__(self):
        self.wind_speed = 10.0
        self.air_density = 1.225
        self.viscosity = 0.001
        self.time_step = 0.01
        self.show_streamlines = True

# Simple UI Element
class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, w, h)
        self.min = min_val
        self.max = max_val
        self.val = initial_val
        self.grabbed = False

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pos = int((self.val - self.min) / (self.max - self.min) * self.rect.w)
        pygame.draw.rect(screen, (0, 128, 255), (self.rect.x + pos - 5, self.rect.y, 10, self.rect.h))

class MainApplication:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 1280, 720
        pygame.display.set_mode((self.screen_width, self.screen_height), DOUBLEBUF|OPENGL)
        self.ctx = moderngl.create_context()
        
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.clock = pygame.time.Clock()
        
        # Initialize subsystems
        self.camera = Camera(self.screen_width, self.screen_height)
        self.params = SimulationParams()
        self.last_time = time.time()
        self.fps = 60
        
        # UI Elements
        self.sliders = {
            'wind': Slider(50, 50, 200, 20, 0, 50, self.params.wind_speed),
            'density': Slider(50, 100, 200, 20, 0, 5, self.params.air_density)
        }
        
        # Shaders
        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330
                uniform mat4 model;
                uniform mat4 view;
                uniform mat4 projection;
                
                in vec3 in_position;
                in vec3 in_normal;
                
                out vec3 normal;
                out vec3 frag_pos;
                
                void main() {
                    gl_Position = projection * view * model * vec4(in_position, 1.0);
                    normal = mat3(transpose(inverse(model))) * in_normal;
                    frag_pos = vec3(model * vec4(in_position, 1.0));
                }
            ''',
            fragment_shader='''
                #version 330
                in vec3 normal;
                in vec3 frag_pos;
                
                out vec4 color;
                
                uniform vec3 light_pos = vec3(5.0, 5.0, 5.0);
                uniform vec3 object_color = vec3(0.8, 0.2, 0.2);
                
                void main() {
                    vec3 light_dir = normalize(light_pos - frag_pos);
                    float diff = max(dot(normalize(normal), light_dir), 0.0);
                    vec3 diffuse = diff * vec3(1.0);
                    color = vec4(object_color * (0.1 + diffuse), 1.0);
                }
            '''
        )
        
        # Car model (placeholder cube)
        vertices = [
            # Position          # Normal
            -0.5, -0.5, -0.5,   0.0, 0.0, -1.0,
            0.5, -0.5, -0.5,    0.0, 0.0, -1.0,
            0.5,  0.5, -0.5,    0.0, 0.0, -1.0,
            -0.5,  0.5, -0.5,   0.0, 0.0, -1.0
        ]
        indices = [
            0, 1, 2, 2, 3, 0
        ]
        self.vbo = self.ctx.buffer(np.array(vertices, dtype='f4'))
        self.ibo = self.ctx.buffer(np.array(indices, dtype='i4'))
        self.vao = self.ctx.vertex_array(
            self.prog,
            [(self.vbo, '6f', 'in_position', 'in_normal')],
            self.ibo
        )
        
        # Initial simulation state
        from car_model import CarModel  # Assume implemented in other module
        from fluid_simulation import FluidSimulation
        
        self.car_model = CarModel()
        self.fluid_sim = FluidSimulation()

    def handle_input(self):
        delta_time = time.time() - self.last_time
        self.last_time = time.time()
        
        keys = pygame.key.get_pressed()
        if keys[K_w]: self.camera.position += self.camera.front * self.camera.speed * delta_time
        if keys[K_s]: self.camera.position -= self.camera.front * self.camera.speed * delta_time
        if keys[K_a]: self.camera.position -= self.camera.right * self.camera.speed * delta_time
        if keys[K_d]: self.camera.position += self.camera.right * self.camera.speed * delta_time
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4: self.camera.speed += 0.5
                if event.button == 5: self.camera.speed = max(0.5, self.camera.speed - 0.5)
                
            # Handle slider dragging
            if event.type == MOUSEMOTION:
                for slider in self.sliders.values():
                    if slider.grabbed:
                        rel = event.rel[0]
                        slider.val = np.clip(slider.val + rel/5, slider.min, slider.max)
                
            if event.type == MOUSEBUTTONDOWN:
                for name, slider in self.sliders.items():
                    if slider.rect.collidepoint(event.pos):
                        slider.grabbed = True
            if event.type == MOUSEBUTTONUP:
                for slider in self.sliders.values():
                    slider.grabbed = False

    def update_simulation(self):
        self.params.wind_speed = self.sliders['wind'].val
        self.params.air_density = self.sliders['density'].val
        self.fluid_sim.update_parameters(self.params)
        self.fluid_sim.step()

    def render_ui(self):
        screen_surf = pygame.Surface((self.screen_width, self.screen_height))
        screen_surf.fill((255, 255, 255), (10, 10, 200, 150))
        
        # Draw sliders
        for slider in self.sliders.values():
            slider.draw(screen_surf)
            
        # FPS counter
        font = pygame.font.Font(None, 30)
        text = font.render(f"FPS: {self.fps}", True, (255, 255, 255))
        screen_surf.blit(text, (10, 10))
        
        # Blit to screen
        texture = self.ctx.texture(screen_surf.get_size(), 4, pygame.image.tostring(screen_surf, 'RGBA'))
        texture.use(0)
        quad = self.ctx.buffer(np.array([-1, -1, 0, 0, 1, -1, 1, 0, -1, 1, 0, 1, 1, 1, 1, 1], dtype='f4'))
        self.ctx.screen.use()
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        self.ctx.vertex_array(self.prog, [(quad, '2f4 2f4', 'in_position', 'in_texcoord')]).render(moderngl.TRIANGLE_STRIP)
        self.ctx.disable(moderngl.BLEND)

    def main_loop(self):
        while True:
            self.handle_input()
            self.update_simulation()
            
            # Clear screen
            self.ctx.clear(0.1, 0.1, 0.1)
            
            # Set matrices
            model = np.identity(4)
            self.prog['model'].write(model.T.astype('f4'))
            self.prog['view'].write(self.camera.look_at().T.astype('f4'))
            self.prog['projection'].write(self.camera.projection.T.astype('f4'))
            
            # Render car
            self.vao.render()
            
            # Render UI
            self.render_ui()
            
            pygame.display.flip()
            self.clock.tick()
            self.fps = self.clock.get_fps()

if __name__ == "__main__":
    app = MainApplication()
    app.main_loop()
