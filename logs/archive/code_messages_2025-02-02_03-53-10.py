C:\mygit\BLazy\repo\3dsim\main.py
Language detected: python
import pygame
import moderngl
import numpy as np
from pyrr import Matrix44, Vector3, matrix44
import math
import random
import imgui
from imgui.integrations.pygame import PygameRenderer

class CarFlowSimulation:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen_width, self.screen_height = 1280, 720
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 
                                            pygame.OPENGL | pygame.DOUBLEBUF)
        
        # Create ModernGL context
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.BLEND)
        
        # Setup ImGui
        imgui.create_context()
        self.imgui_renderer = PygameRenderer()
        
        # Camera variables
        self.camera_pos = Vector3([0, 2, 5])
        self.camera_rot = Vector3([-25, 0, 0])
        self.proj = Matrix44.perspective_projection(45, self.screen_width/self.screen_height, 0.1, 100)
        
        # Simulation variables
        self.particles = []
        self.wind_direction = Vector3([1, 0, 0])
        self.simulation_speed = 1.0
        self.is_camera_free = False
        
        # Initialize components
        self.init_shaders()
        self.init_car_model()
        self.init_particle_system()
        
    def init_shaders(self):
        # Car shader
        self.car_prog = self.ctx.program(
            vertex_shader='''
                #version 330
                uniform mat4 model;
                uniform mat4 view;
                uniform mat4 proj;
                in vec3 in_position;
                void main() {
                    gl_Position = proj * view * model * vec4(in_position, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330
                out vec4 fragColor;
                void main() {
                    fragColor = vec4(0.2, 0.6, 1.0, 1.0);
                }
            '''
        )
        
        # Particle shader
        self.particle_prog = self.ctx.program(
            vertex_shader='''
                #version 330
                uniform mat4 view;
                uniform mat4 proj;
                in vec3 in_position;
                void main() {
                    gl_Position = proj * view * vec4(in_position, 1.0);
                    gl_PointSize = 3.0;
                }
            ''',
            fragment_shader='''
                #version 330
                out vec4 fragColor;
                void main() {
                    fragColor = vec4(1.0, 0.5, 0.2, 0.7);
                }
            '''
        )

    def init_car_model(self):
        # Simple cube model (replace with actual car model)
        car_vertices = [
            -1.0, -0.5, -2.0,  1.0, -0.5, -2.0,
            1.0, -0.5, 2.0,  -1.0, -0.5, 2.0,
            -1.0, 0.5, -2.0,  1.0, 0.5, -2.0,
            1.0, 0.5, 2.0,  -1.0, 0.5, 2.0
        ]
        self.car_vbo = self.ctx.buffer(np.array(car_vertices, dtype='f4'))
        self.car_vao = self.ctx.simple_vertex_array(self.car_prog, self.car_vbo, 'in_position')

    def init_particle_system(self):
        # Initialize particles
        self.particle_vbo = self.ctx.buffer(reserve=1024 * 4 * 3)
        self.update_particles()
        
    def update_particles(self):
        # Regenerate particles
        new_particles = []
        for _ in range(100):
            new_particles.append({
                'pos': Vector3([random.uniform(-1.5, 1.5), 0.5, -1.5]),
                'vel': Vector3([random.uniform(-0.5, 0.5), 0, random.uniform(0.5, 1.5)])
            })
        self.particles = new_particles

    def update_camera(self):
        view = Matrix44.identity()
        view = matrix44.multiply(view, Matrix44.from_translation(-self.camera_pos))
        view = matrix44.multiply(view, Matrix44.from_euler(self.camera_rot))
        return view

    def handle_input(self):
        delta_time = pygame.time.get_ticks() / 1000.0
        keys = pygame.key.get_pressed()
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        
        # Camera rotation with mouse
        if pygame.mouse.get_pressed()[0]:
            self.camera_rot.x += mouse_dy * 0.1
            self.camera_rot.y += mouse_dx * 0.1

        # Camera movement
        if self.is_camera_free:
            move_speed = 0.1
            if keys[pygame.K_w]:
                self.camera_pos.z -= move_speed
            if keys[pygame.K_s]:
                self.camera_pos.z += move_speed
            if keys[pygame.K_a]:
                self.camera_pos.x -= move_speed
            if keys[pygame.K_d]:
                self.camera_pos.x += move_speed

    def update_physics(self, delta_time):
        # Update particle positions with physics
        for p in self.particles:
            p['vel'] += self.wind_direction * delta_time * 0.1
            p['pos'] += p['vel'] * delta_time * self.simulation_speed

            # Simple collision with car
            if -1.0 < p['pos'].x < 1.0 and -2.0 < p['pos'].z < 2.0 and p['pos'].y < 1.0:
                p['vel'] *= -0.5
                p['pos'] += p['vel'] * 0.1

            # Reset particles that go out of bounds
            if p['pos'].length() > 10:
                p['pos'] = Vector3([random.uniform(-1.5, 1.5), 0.5, -1.5])

    def render_ui(self):
        imgui.new_frame()
        imgui.begin("Simulation Controls")
        
        changed, self.wind_direction.x = imgui.slider_float("Wind X", self.wind_direction.x, -1.0, 1.0)
        changed, self.wind_direction.y = imgui.slider_float("Wind Y", self.wind_direction.y, -1.0, 1.0)
        changed, self.simulation_speed = imgui.slider_float("Speed", self.simulation_speed, 0.1, 5.0)
        
        if imgui.button("Reset Particles"):
            self.update_particles()
            
        imgui.end()

    def draw(self):
        self.ctx.clear(0.1, 0.1, 0.1)
        view = self.update_camera()
        
        # Draw car
        car_model = Matrix44.from_translation([0, -0.5, 0]) * Matrix44.from_scale([1, 0.5, 2])
        self.car_prog['model'].write(car_model.astype('f4'))
        self.car_prog['view'].write(view.astype('f4'))
        self.car_prog['proj'].write(self.proj.astype('f4'))
        self.car_vao.render(moderngl.TRIANGLE_STRIP)
        
        # Draw particles
        particle_data = np.array([p['pos'] for p in self.particles], dtype='f4')
        self.particle_vbo.write(particle_data.tobytes())
        self.particle_prog['view'].write(view.astype('f4'))
        self.particle_prog['proj'].write(self.proj.astype('f4'))
        self.ctx.enable(moderngl.BLEND)
        self.ctx.simple_vertex_array(self.particle_prog, self.particle_vbo, 'in_position').render(moderngl.POINTS)
        self.ctx.disable(moderngl.BLEND)

        # Render UI
        imgui.render()
        self.imgui_renderer.render(imgui.get_draw_data())

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            clock.tick(60)
            delta_time = clock.get_time() / 1000.0
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.imgui_renderer.process_event(event)
            
            # Update components
            self.handle_input()
            self.update_physics(delta_time)
            
            # Render everything
            self.draw()
            
        pygame.quit()

if __name__ == "__main__":
    try:
        sim = CarFlowSimulation()
        sim.run()
    except Exception as e:
        print(f"Error occurred: {str(e)}")
C:\mygit\BLazy\repo\3dsim\main.py
Language detected: python
import pygame
import moderngl
import numpy as np
import sys
from simulation import AirflowSimulation
from ui_manager import UIManager
from camera import Camera

class MainApp:
    def __init__(self):
        # Initialize pygame and window
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720), pygame.OPENGL | pygame.DOUBLEBUF)
        self.ctx = moderngl.create_context()
        
        # Window configuration
        pygame.display.set_caption("3D Car Airflow Simulation")
        self.clock = pygame.time.Clock()
        self.running = True
        self.simulation_running = True
        self.simulation_speed = 1.0

        # Initialize components
        self.camera = Camera(position=(0, 2, 5))
        self.simulation = AirflowSimulation(ctx=self.ctx)
        self.ui_manager = UIManager(self.screen)

        # Set OpenGL states
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.simulation_running = not self.simulation_running
                elif event.key == pygame.K_UP:
                    self.simulation_speed = min(2.0, self.simulation_speed + 0.1)
                elif event.key == pygame.K_DOWN:
                    self.simulation_speed = max(0.5, self.simulation_speed - 0.1)
            
            # Camera handling
            self.camera.handle_event(event)
            
            # UI event propagation
            self.ui_manager.handle_event(event)

    def update(self):
        if self.simulation_running:
            self.simulation.update(delta_time=self.clock.get_time() * self.simulation_speed / 1000)
        self.camera.update()

    def render(self):
        self.ctx.clear(0.1, 0.2, 0.3, 1.0)
        
        # Simulation rendering
        self.simulation.render(
            projection_matrix=self.camera.projection_matrix,
            view_matrix=self.camera.view_matrix
        )
        
        # UI rendering
        self.ui_manager.render()
        
        pygame.display.flip()

    def run(self):
        try:
            while self.running:
                self.handle_events()
                self.update()
                self.render()
                self.clock.tick(60)
        except Exception as e:
            print(f"Error: {str(e)}")
            pygame.quit()
            sys.exit(1)
        finally:
            pygame.quit()
            sys.exit(0)

if __name__ == "__main__":
    app = MainApp()
    app.run()
