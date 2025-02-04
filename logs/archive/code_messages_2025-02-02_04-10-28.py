C:\mygit\BLazy\repo\3dsim\main.py
Language detected: python
import pygame
import moderngl
import numpy as np
import imgui
from imgui.integrations.pygame import PygameRenderer

class AirflowSimulation:
    def __init__(self):
        """
        Initializes the Airflow Simulation application.
        Sets up Pygame, ModernGL, ImGui, shaders, camera, and simulation parameters.
        """
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)

        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
        pygame.display.set_caption("3D Car Airflow Simulation")

        self.ctx = moderngl.create_context()

        imgui.create_context()
        self.imgui_renderer = PygameRenderer()

        self.load_shaders()
        self.setup_geometry()
        self.setup_camera()
        self.initialize_parameters()

    def load_shaders(self):
        """
        Loads vertex and fragment shaders.
        For now, using basic shaders for colored rendering.
        """
        vertex_shader = """
            #version 330 core

            in vec3 in_position;
            in vec3 in_color;
            out vec3 color;

            uniform mat4 model_matrix;
            uniform mat4 view_matrix;
            uniform mat4 projection_matrix;

            void main() {
                gl_Position = projection_matrix * view_matrix * model_matrix * vec4(in_position, 1.0);
                color = in_color;
            }
        """

        fragment_shader = """
            #version 330 core

            in vec3 color;
            out vec4 fragColor;

            void main() {
                fragColor = vec4(color, 1.0);
            }
        """

        self.program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

    def setup_geometry(self):
        """
        Sets up the geometry for the car (initially a simple cube).
        """
        # Define vertices, colors, and indices for a cube
        vertices = np.array([
            # Front face
            (-0.5, -0.5, 0.5), (1, 0, 0), # Bottom left
            (0.5, -0.5, 0.5), (1, 0, 0),  # Bottom right
            (0.5, 0.5, 0.5), (1, 0, 0),   # Top right
            (-0.5, 0.5, 0.5), (1, 0, 0),  # Top left

            # Back face
            (-0.5, -0.5, -0.5), (0, 1, 0),# Bottom left
            (0.5, -0.5, -0.5), (0, 1, 0), # Bottom right
            (0.5, 0.5, -0.5), (0, 1, 0),  # Top right
            (-0.5, 0.5, -0.5), (0, 1, 0), # Top left

            # Right face
            (0.5, -0.5, 0.5), (0, 0, 1),  # Bottom front
            (0.5, -0.5, -0.5), (0, 0, 1), # Bottom back
            (0.5, 0.5, -0.5), (0, 0, 1),  # Top back
            (0.5, 0.5, 0.5), (0, 0, 1),   # Top front

            # Left face
            (-0.5, -0.5, 0.5), (1, 1, 0), # Bottom front
            (-0.5, -0.5, -0.5), (1, 1, 0),# Bottom back
            (-0.5, 0.5, -0.5), (1, 1, 0), # Top back
            (-0.5, 0.5, 0.5), (1, 1, 0),  # Top front

            # Top face
            (-0.5, 0.5, 0.5), (1, 0, 1),  # Front left
            (0.5, 0.5, 0.5), (1, 0, 1),   # Front right
            (0.5, 0.5, -0.5), (1, 0, 1),  # Back right
            (-0.5, 0.5, -0.5), (1, 0, 1), # Back left

            # Bottom face
            (-0.5, -0.5, 0.5), (0, 1, 1), # Front left
            (0.5, -0.5, 0.5), (0, 1, 1),  # Front right
            (0.5, -0.5, -0.5), (0, 1, 1), # Back right
            (-0.5, -0.5, -0.5), (0, 1, 1) # Back left
        ], dtype='f4')

        indices = np.array([
            0, 1, 2, 2, 3, 0,       # Front face
            4, 5, 6, 6, 7, 4,       # Back face
            8, 9, 10, 10, 11, 8,     # Right face
            12, 13, 14, 14, 15, 12,    # Left face
            16, 17, 18, 18, 19, 16,    # Top face
            20, 21, 22, 22, 23, 20     # Bottom face
        ], dtype='i4')

        self.vbo = self.ctx.buffer(vertices)
        self.ibo = self.ctx.buffer(indices)
        self.car_vao = self.ctx.vertex_array(
            self.program,
            [
                (self.vbo, '3f 3f', 'in_position', 'in_color')
            ],
            index_buffer=self.ibo
        )
        self.num_vertices = len(indices)

    def setup_camera(self):
        """
        Sets up the initial camera position and perspective projection.
        """
        self.camera_position = np.array([3.0, 3.0, 3.0], dtype='f4')
        self.camera_target = np.array([0.0, 0.0, 0.0], dtype='f4')
        self.camera_up = np.array([0.0, 1.0, 0.0], dtype='f4')

        self.projection_matrix = self.get_projection_matrix()
        self.view_matrix = self.get_view_matrix()

    def get_projection_matrix(self):
        """
        Calculates the perspective projection matrix.
        """
        aspect_ratio = self.width / self.height
        fovy = 45.0  # Field of view in degrees
        near_plane = 0.1
        far_plane = 100.0

        perspective_matrix = self.ctx.projection_perspective(fovy=fovy, aspect=aspect_ratio, near=near_plane, far=far_plane)
        return perspective_matrix

    def get_view_matrix(self):
        """
        Calculates the view matrix based on camera position, target, and up vector.
        """
        lookat_matrix = self.ctx.lookat(self.camera_position, self.camera_target, self.camera_up)
        return lookat_matrix

    def initialize_parameters(self):
        """
        Initializes customizable simulation parameters.
        """
        self.car_length = 4.5  # meters
        self.car_width = 1.8   # meters
        self.car_height = 1.5  # meters
        self.car_pitch = 0.0   # degrees
        self.car_yaw = 0.0     # degrees
        self.wind_speed = 20.0  # m/s
        self.air_density = 1.225 # kg/m^3 (standard sea level)
        self.temperature = 25.0 # Celsius

    def handle_input(self, event):
        """
        Handles user input events (keyboard, mouse, etc.).
        For now, just handles ImGui events and window resizing.
        """
        self.imgui_renderer.process_event(event)
        if event.type == pygame.VIDEORESIZE:
            self.ctx.viewport = (0, 0, event.w, event.h)
            self.width, self.height = event.w, event.h
            self.projection_matrix = self.get_projection_matrix()

    def render_ui(self):
        """
        Renders the ImGui user interface for controlling simulation parameters.
        """
        imgui.new_frame()

        imgui.begin("Simulation Parameters")

        changed, self.car_length = imgui.slider_float("Car Length (m)", self.car_length, 1.0, 10.0)
        changed, self.car_width = imgui.slider_float("Car Width (m)", self.car_width, 0.5, 3.0)
        changed, self.car_height = imgui.slider_float("Car Height (m)", self.car_height, 0.5, 3.0)
        changed, self.car_pitch = imgui.slider_float("Car Pitch (deg)", self.car_pitch, -30.0, 30.0)
        changed, self.car_yaw = imgui.slider_float("Car Yaw (deg)", self.car_yaw, -180.0, 180.0)
        changed, self.wind_speed = imgui.slider_float("Wind Speed (m/s)", self.wind_speed, 0.0, 50.0)
        changed, self.air_density = imgui.slider_float("Air Density (kg/m^3)", self.air_density, 0.5, 2.0)
        changed, self.temperature = imgui.slider_float("Temperature (°C)", self.temperature, -20.0, 50.0)

        imgui.end()
        imgui.render()

    def update_simulation(self):
        """
        Updates the simulation state based on current parameters.
        Currently a placeholder, simulation logic will be added here later.
        """
        # Placeholder for simulation update logic
        pass

    def render_scene(self):
        """
        Renders the 3D scene using ModernGL.
        Currently just renders a colored cube representing the car.
        """
        self.ctx.clear(0.2, 0.2, 0.2)  # Clear to a dark grey color
        self.ctx.enable(moderngl.DEPTH_TEST)

        # Model matrix for car transformations (scaling based on dimensions, rotation based on angles)
        model_matrix = self.ctx.matrix44.identity()
        model_matrix = model_matrix * self.ctx.matrix44.scaling(self.car_length, self.car_height, self.car_width) # Scale based on car dimensions
        model_matrix = model_matrix * self.ctx.matrix44.rotz(np.radians(self.car_yaw)) # Yaw rotation
        model_matrix = model_matrix * self.ctx.matrix44.rotx(np.radians(self.car_pitch)) # Pitch rotation


        # Update matrices in the shader program
        self.program['model_matrix'] = model_matrix
        self.program['view_matrix'] = self.view_matrix
        self.program['projection_matrix'] = self.projection_matrix

        self.car_vao.render(mode=moderngl.TRIANGLES, vertices=self.num_vertices)

    def render(self):
        """
        Renders the entire frame, including the 3D scene and the UI.
        """
        self.render_scene()
        self.imgui_renderer.render(imgui.get_draw_data())
        pygame.display.flip()

    def run(self):
        """
        Main simulation loop.
        Handles events, updates simulation, renders frames.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_input(event)

            self.render_ui()
            self.update_simulation()
            self.render()

        pygame.quit()

if __name__ == "__main__":
    sim = AirflowSimulation()
    sim.run()
