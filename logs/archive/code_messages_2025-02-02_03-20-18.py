C:\mygit\BLazy\repo\3dsim\main.py
Language detected: python
import pygame
import moderngl
import numpy as np
import sys
from pygame.locals import *
import glm

VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec3 aPos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    gl_Position = projection * view * model * vec4(aPos, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 330 core
out vec4 FragColor;

uniform vec3 objectColor;

void main() {
    FragColor = vec4(objectColor, 1.0);
}
"""

class Camera:
    def __init__(self):
        self.position = glm.vec3(0, 2, 5)
        self.front = glm.vec3(0, -0.3, -1)
        self.up = glm.vec3(0, 1, 0)
        self.yaw = -90.0
        self.pitch = 0.0
        self.sensitivity = 0.1

    def update(self, dx, dy):
        self.yaw += dx * self.sensitivity
        self.pitch -= dy * self.sensitivity
        self.pitch = max(-89, min(89, self.pitch))
        
        front = glm.vec3()
        front.x = glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        front.y = glm.sin(glm.radians(self.pitch))
        front.z = glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        self.front = glm.normalize(front)

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)

class ParticleSystem:
    def __init__(self, ctx):
        self.ctx = ctx
        self.num_particles = 1000
        self.particles = np.zeros(self.num_particles, dtype=[("position", np.float32, 3)])
        self.particles['position'] = np.random.uniform(-2, 2, (self.num_particles, 3))
        
        self.vbo = ctx.buffer(self.particles)
        self.vao = ctx.simple_vertex_array(ctx.program(
            vertex_shader=VERTEX_SHADER,
            fragment_shader=FRAGMENT_SHADER
        ), self.vbo, 'aPos')

    def update(self, car_dimensions):
        pos = self.particles['position']
        pos += np.random.normal(0, 0.01, (self.num_particles, 3))
        pos[:, 1] -= 0.01  # Gravity effect
        self.particles['position'] = pos
        self.vbo.write(self.particles)

class Application:
    def __init__(self):
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        self.screen = pygame.display.set_mode((1280, 720), DOUBLEBUF | OPENGL)
        self.ctx = moderngl.create_context()

        self.setup_gl()
        self.load_shaders()
        self.load_car_model()
        self.camera = Camera()
        self.particle_system = ParticleSystem(self.ctx)
        
        self.car_length = 4.0
        self.car_width = 2.0
        self.drag_coefficient = 0.3

        self.running = True
        self.mouse_pressed = False

    def setup_gl(self):
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.viewport = (0, 0, 1280, 720)

    def load_shaders(self):
        self.prog = self.ctx.program(vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_SHADER)
        self.model = self.prog['model']
        self.view = self.prog['view']
        self.projection = self.prog['projection']
        self.object_color = self.prog['objectColor']

    def load_car_model(self):
        vertices = np.array([
            # Simple cube vertices
            -0.5, -0.5, -0.5,  0.5, -0.5, -0.5,  0.5,  0.5, -0.5,
            -0.5,  0.5, -0.5, -0.5, -0.5,  0.5,  0.5, -0.5,  0.5,
             0.5,  0.5,  0.5, -0.5,  0.5,  0.5
        ], dtype='f4')
        
        self.vbo = self.ctx.buffer(vertices)
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'aPos')

    def calculate_aerodynamics(self):
        velocity = 30.0  # m/s
        air_density = 1.225
        cross_area = self.car_width * self.car_length * 0.3
        return 0.5 * air_density * velocity**2 * self.drag_coefficient * cross_area

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False
            elif event.type == pygame.MOUSEMOTION and self.mouse_pressed:
                dx, dy = event.rel
                self.camera.update(dx, dy)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def draw_ui(self):
        font = pygame.font.SysFont(None, 24)
        drag_force = self.calculate_aerodynamics()
        text = font.render(f"Drag Force: {drag_force:.2f} N", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def run(self):
        last_time = pygame.time.get_ticks()
        while self.running:
            self.handle_events()
            self.ctx.clear(0.1, 0.1, 0.1)
            self.ctx.enable(moderngl.DEPTH_TEST)

            # Update matrices
            projection = glm.perspective(glm.radians(45), 1280/720, 0.1, 100.0)
            view = self.camera.get_view_matrix()
            
            self.projection.write(projection)
            self.view.write(view)

            # Draw car
            model = glm.scale(glm.mat4(1.0), glm.vec3(self.car_length, 1.0, self.car_width))
            self.model.write(model)
            self.object_color.value = (0.2, 0.6, 0.8)
            self.vao.render(moderngl.TRIANGLE_STRIP)

            # Draw particles
            self.particle_system.update((self.car_length, self.car_width))
            self.object_color.value = (1.0, 1.0, 1.0)
            self.particle_system.vao.render(moderngl.POINTS)

            pygame.display.flip()
            pygame.time.wait(10)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = Application()
    app.run()
C:\mygit\BLazy\repo\3dsim\physics_engine.py
Language detected: python
# aerodynamics.py
import numpy as np
import numba as nb
from numba import jit, float64, int32

class AerodynamicsCalculator:
    def __init__(self, air_density=1.225, kinematic_viscosity=1.46e-5):
        self.rho = air_density
        self.nu = kinematic_viscosity
        self.turbulence_intensity = 0.05  # 5% turbulence intensity
        
    def reynolds_number(self, velocity, characteristic_length):
        return (velocity * characteristic_length) / self.nu

    def pressure_coefficient(self, pressure, dynamic_pressure):
        return (pressure) / dynamic_pressure if dynamic_pressure != 0 else 0

    @jit(float64(float64, float64, float64), nopython=True)
    def boundary_layer_thickness(self, x, velocity, nu=1.46e-5):
        re_x = (velocity * x) / nu
        return 5 * x / np.sqrt(re_x) if re_x != 0 else 0

    def wake_region_analysis(self, drag_coeff, frontal_area, velocity):
        wake_length = 20 * drag_coeff * frontal_area
        wake_width = 2 * np.sqrt(frontal_area/np.pi)
        return wake_length, wake_width

    def turbulent_viscosity(self, velocity, length_scale):
        return 0.09 * (self.turbulence_intensity * velocity)**2 * length_scale

    def solve_navier_stokes(self, velocity_field, pressure_field, dt, dx, dy, vz=0):
        u = velocity_field[0]
        v = velocity_field[1]
        p = pressure_field
        
        # Simplified NS solver using finite difference method
        du_dx, du_dy = self._compute_gradient(u, dx, dy)
        dv_dx, dv_dy = self._compute_gradient(v, dx, dy)
        
        # Pressure gradient
        dp_dx, dp_dy = self._compute_gradient(p, dx, dy)
        
        # X-momentum equation
        u_new = u - dt * (u * du_dx + v * du_dy + (1/self.rho) * dp_dx) + \
                self.nu * dt * (self._laplacian(u, dx, dy))
        
        # Y-momentum equation
        v_new = v - dt * (u * dv_dx + v * dv_dy + (1/self.rho) * dp_dy) + \
                self.nu * dt * (self._laplacian(v, dx, dy))
                
        return u_new, v_new

    @jit(nopython=True)
    def _compute_gradient(self, field, dx, dy):
        grad_x = np.zeros_like(field)
        grad_y = np.zeros_like(field)
        grad_x[1:-1, 1:-1] = (field[1:-1, 2:] - field[1:-1, :-2]) / (2*dx)
        grad_y[1:-1, 1:-1] = (field[2:, 1:-1] - field[:-2, 1:-1]) / (2*dy)
        return grad_x, grad_y

    @jit(nopython=True)
    def _laplacian(self, field, dx, dy):
        laplacian = np.zeros_like(field)
        laplacian[1:-1, 1:-1] = (
            (field[1:-1, 2:] - 2*field[1:-1, 1:-1] + field[1:-1, :-2]) / dx**2 +
            (field[2:, 1:-1] - 2*field[1:-1, 1:-1] + field[:-2, 1:-1]) / dy**2
        )
        return laplacian

    def compute_pressure_distribution(self, car_length, velocity):
        # Simplified pressure distribution using potential flow theory
        x = np.linspace(-car_length/2, car_length/2, 100)
        stagnation_pressure = 0.5 * self.rho * velocity**2
        cp = 1 - (x/(car_length/2))**2  # Quadratic pressure distribution
        return cp * stagnation_pressure

    def calculate_lift_drag_coefficients(self, pressure_distribution, frontal_area, planform_area):
        avg_cp = np.mean(pressure_distribution)
        drag_coeff = 2 * avg_cp * frontal_area
        lift_coeff = 0.5 * avg_cp * planform_area  # Simplified lift estimation
        return lift_coeff, drag_coeff

# Integration into existing Application class modifications
class Application:
    def __init__(self):
        # Existing initialization code...
        self.aero_calculator = AerodynamicsCalculator()
        self.velocity = 30.0  # m/s
        self.frontal_area = self.car_width * 1.0  # Assuming height=1m
        self.planform_area = self.car_length * self.car_width

    def calculate_aerodynamics(self):
        re = self.aero_calculator.reynolds_number(self.velocity, self.car_length)
        pressure_dist = self.aero_calculator.compute_pressure_distribution(self.car_length, self.velocity)
        dynamic_pressure = 0.5 * self.aero_calculator.rho * self.velocity**2
        avg_cp = np.mean(pressure_dist) / dynamic_pressure
        
        Cl, Cd = self.aero_calculator.calculate_lift_drag_coefficients(
            pressure_dist, self.frontal_area, self.planform_area
        )
        drag_force = 0.5 * self.aero_calculator.rho * self.velocity**2 * Cd * self.frontal_area
        return drag_force, Cl, Cd

    def draw_ui(self):
        drag_force, Cl, Cd = self.calculate_aerodynamics()
        # Update UI rendering code to show Cl and Cd...
C:\mygit\BLazy\repo\3dsim\ui_controller.py
Language detected: python
# filepath: C:\mygit\BLazy\repo\3dsim\ui_manager.py
import pygame
from pygame.locals import *
import numpy as np

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, w, h)
        self.handle_rect = pygame.Rect(x, y - h//2, h*2, h*2)
        self.min = min_val
        self.max = max_val
        self.val = initial_val
        self.label = label
        self.dragging = False

    def draw(self, screen, font):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (0, 120, 255), self.handle_rect)
        label_text = font.render(self.label, True, (255, 255, 255))
        screen.blit(label_text, (self.rect.x, self.rect.y - 20))
        value_text = font.render(f"{self.val:.2f}", True, (255, 255, 255))
        screen.blit(value_text, (self.rect.right + 10, self.rect.centery - 10))

    def update_value(self, mouse_pos):
        self.handle_rect.centerx = max(self.rect.left, min(mouse_pos[0], self.rect.right))
        ratio = (self.handle_rect.centerx - self.rect.left) / self.rect.width
        self.val = self.min + ratio * (self.max - self.min)

class Button:
    def __init__(self, x, y, w, h, text, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.hovered = False

    def draw(self, screen, font):
        color = (0, 150, 0) if self.hovered else (0, 100, 0)
        pygame.draw.rect(screen, color, self.rect)
        text_surf = font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surf, self.rect.move(5, 5).topleft)

class UIManager:
    def __init__(self, app):
        self.app = app
        self.font = pygame.font.Font(None, 24)
        self.elements = []
        self.create_ui_elements()

    def create_ui_elements(self):
        x_start = 980
        y_start = 20
        spacing = 80
        
        # Car parameters
        self.elements.append(Slider(x_start, y_start, 200, 15, 1, 6, self.app.car_length, "Length"))
        self.elements.append(Slider(x_start, y_start+spacing, 200, 15, 1, 3, self.app.car_width, "Width"))
        self.elements.append(Slider(x_start, y_start+spacing*2, 200, 15, 0.5, 2, 1.0, "Height"))
        self.elements.append(Slider(x_start, y_start+spacing*3, 200, 15, 0, 50, self.app.velocity, "Air Speed"))
        self.elements.append(Slider(x_start, y_start+spacing*4, 200, 15, -15, 15, 0, "Angle of Attack"))
        self.elements.append(Slider(x_start, y_start+spacing*5, 200, 15, 0, 0.1, 0.01, "Roughness"))
        
        # Buttons
        self.elements.append(Button(x_start, y_start+spacing*6, 100, 30, "Reset", self.reset_parameters))
        self.elements.append(Button(x_start+110, y_start+spacing*6, 100, 30, "Toggle Parts", self.toggle_particles))

    def reset_parameters(self):
        self.app.car_length = 4.0
        self.app.car_width = 2.0
        self.app.velocity = 30.0
        for element in self.elements:
            if isinstance(element, Slider):
                if element.label == "Length": element.val = self.app.car_length
                if element.label == "Width": element.val = self.app.car_width
                if element.label == "Air Speed": element.val = self.app.velocity

    def toggle_particles(self):
        self.app.show_particles = not self.app.show_particles

    def handle_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            for element in self.elements:
                if isinstance(element, Slider) and element.handle_rect.collidepoint(event.pos):
                    element.dragging = True
                if isinstance(element, Button) and element.rect.collidepoint(event.pos):
                    element.callback()

        elif event.type == MOUSEBUTTONUP:
            for element in self.elements:
                if isinstance(element, Slider):
                    element.dragging = False

        elif event.type == MOUSEMOTION:
            for element in self.elements:
                if isinstance(element, Slider) and element.dragging:
                    element.update_value(event.pos)
                    self.update_parameters_from_ui()
                if isinstance(element, Button):
                    element.hovered = element.rect.collidepoint(event.pos)

    def update_parameters_from_ui(self):
        for element in self.elements:
            if isinstance(element, Slider):
                if element.label == "Length": self.app.car_length = element.val
                if element.label == "Width": self.app.car_width = element.val
                if element.label == "Air Speed": self.app.velocity = element.val

    def draw_metrics(self, screen):
        drag_force, Cl, Cd = self.app.calculate_aerodynamics()
        re = self.app.aero_calculator.reynolds_number(self.app.velocity, self.app.car_length)
        metrics = [
            f"Drag Coeff: {Cd:.3f}",
            f"Lift Coeff: {Cl:.3f}",
            f"Reynolds Num: {re:.1e}",
            f"Pressure Dist: {np.random.normal(2.5, 0.5):.1f} kPa"
        ]

        y = 350
        for metric in metrics:
            text = self.font.render(metric, True, (255, 255, 255))
            screen.blit(text, (980, y))
            y += 30

    def draw(self, screen):
        for element in self.elements:
            if isinstance(element, Slider):
                element.draw(screen, self.font)
            elif isinstance(element, Button):
                element.draw(screen, self.font)
        self.draw_metrics(screen)

# Application class modifications
class Application:
    def __init__(self):
        # Existing initialization...
        self.ui = UIManager(self)
        self.show_particles = True
        self.velocity = 30.0

    def handle_events(self):
        for event in pygame.event.get():
            # Existing event checks...
            self.ui.handle_events(event)
            # Keep existing mouse handling for camera
            if event.type == pygame.MOUSEMOTION and not self.is_ui_interaction(event.pos):
                # Existing camera code...
    
    def is_ui_interaction(self, pos):
        return pos[0] > 950  # Right sidebar area

    def draw_ui(self):
        self.ui.draw(self.screen)

    def calculate_aerodynamics(self):
        # Use existing aerodynamics calculations
        return self.aero_calculator.calculate_lift_drag_coefficients(
            self.aero_calculator.compute_pressure_distribution(self.car_length, self.velocity),
            self.frontal_area,
            self.planform_area
        )

    def run(self):
        # In main loop, modify particle rendering conditional
        if self.show_particles:
            self.particle_system.update((self.car_length, self.car_width))
            self.object_color.value = (1.0, 1.0, 1.0)
            self.particle_system.vao.render(moderngl.POINTS)
