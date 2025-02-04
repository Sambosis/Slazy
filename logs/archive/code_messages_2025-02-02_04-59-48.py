C:\mygit\BLazy\repo\3dsim\main.py
Language detected: python
# Required imports
import pygame
import moderngl
import numpy as np
from pyrr import Matrix44, Vector3
from moderngl_geometry import Geometry, Node, Scene, Renderer
from pygame.locals import *
from imgui.integrations.pygame import PygameRenderer
import imgui


# Initialize Pygame and set up window
pygame.init()
screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
ctx = moderngl.create_context()

# Camera setup
camera_pos = Vector3([0.0, 0.0, 5.0])
camera_front = Vector3([0.0, 0.0, -1.0])
camera_up = Vector3([0.0, 1.0, 0.0])
last_mouse_pos = None

# Mouse movement handling
def process_input(camera_pos, camera_front, camera_up):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: 
                camera_pos.z -= 0.2
            if event.button == 5:
                camera_pos.z += 0.2

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera_pos += camera_front * 0.05
    if keys[pygame.K_s]:
        camera_pos -= camera_front * 0.05
    if keys[pygame.K_a]:
        camera_pos -= camera_front.cross(camera_up).normalize() * 0.05
    if keys[pygame.K_d]:
        camera_pos += camera_front.cross(camera_up).normalize() * 0.05

    return camera_pos


# Car model creation
def create_car_model():
    # Example of creating a simple cube as the car model
    vertices = np.array([
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
    ], dtype='f4')
    indices = np.array([
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        0, 1, 5, 5, 4, 0,
        3, 2, 6, 6, 7, 3,
        1, 2, 6, 6, 5, 1,
        0, 3, 7, 7, 4, 0
    ], dtype='i4')
    vao = ctx.buffer(vertices).vertices
    ebo = ctx.buffer(indices)
    program = ctx.program(
        vertex_shader='''
        #version 330 core
        layout(location = 0) in vec3 aPos;
        
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;
        
        void main()
        {
           gl_Position = projection * view * model * vec4(aPos, 1.0);
        }
        ''',
        fragment_shader='''
        #version 330 core
        out vec4 FragColor;
        
        void main()
        {
           FragColor = vec4(1.0, 0.0, 0.0, 1.0);
        }
        '''
    )
    vao = ctx.simple_vertex_array(program, ebo, 'aPos')
    return vao


# Fluid dynamics simulation (simplified)
def simulate_fluid_flow():
    # Placeholder function for fluid dynamics simulation
    # This needs complex physics simulations based on Navier-Stokes equations
    pass


# Particle system for airflow visualization
def create_particle_system():
    # Basic particle system implementation
    particles = []
    for _ in range(1000):
        particles.append({
            'position': np.random.uniform(-10, 10, size=3),
            'velocity': np.random.uniform(-1, 1, size=3),
            'color': np.random.rand(3)
        })
    return particles


# GUI Controls for car parameters
def show_gui(car_params):
    ImGuiIO = imgui.get_io()
    imgui_pygame = PygameRenderer()
    
    while True:
        imgui_pygame.process_event(pygame.event.wait())

        imgui.new_frame()
        imgui.show_test_window()
        
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, current_query = imgui.menu_item(
                    "Quit", '', False, True
                )

                if clicked_quit:
                    pygame.quit()
                    exit(1)

                imgui.end_menu()
            imgui.end_main_menu_bar()
            
        imgui.begin("Car Parameters")
        
        _, car_params['drag_coefficient'] = imgui.slider_float('Drag Coefficient', car_params['drag_coefficient'], 0.1, 2.0)
        _, car_params['lift_coefficient'] = imgui.slider_float('Lift Coefficient', car_params['lift_coefficient'], 0.1, 2.0)
        
        imgui.end()
        imgui.render()
        imgui.end_frame()


# Main game loop
def main():
    clock = pygame.time.Clock()
    
    # Initialize car params
    car_params = {'drag_coefficient': 0.32, 'lift_coefficient': 0.09}
    
    # Setup car model
    car_vao = create_car_model()
    
    # Initial setup
    projection = Matrix44.perspective_projection(45.0, 800 / 600, 0.1, 100.0)
    view = Matrix44.look_at(
        camera_pos,
        camera_pos + camera_front,
        camera_up
    )
    model = Matrix44.from_translation(Vector3([0.0, 0.0, 0.0]))
    
    # Render objects
    renderer = Renderer(ctx)
    
    running = True
    while running:
        clock.tick(60)
        delta_time = clock.get_time()
        
        # Process user input
        camera_pos = process_input(camera_pos, camera_front, camera_up)
        show_gui(car_params)
        
        # Calculate physics and update fluid flow
        if running:
            simulate_fluid_flow()
            render_objects(car_vao, model, view, projection)
        
        pygame.display.flip()
        pygame.display.set_caption(f"FPS: {clock.get_fps():.2f}")


if __name__ == '__main__':
    main()
C:\mygit\BLazy\repo\3dsim\shaders\vertex_shader.glsl
Language detected: glsl
#version 330 core

// Input vertex attributes (from vertex buffer)
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec2 textureCoord;

// Input uniform values
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform mat3 normalMatrix;

// Output values to fragment shader
out vec3 fragPosition;
out vec3 fragNormal;
out vec2 fragTextureCoord;

void main()
{
    // Transform the vertex position
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);

    // Pass through the texture coordinate
    fragTextureCoord = textureCoord;

    // Transform the vertex normal
    fragNormal = normalize(normalMatrix * normal);

    // Calculate the fragment position
    fragPosition = (modelMatrix * vec4(position, 1.0)).xyz;
}
C:\mygit\BLazy\repo\3dsim\utils\fluid_dynamics.py
Language detected: python
# fluid_dynamics.py

import numpy as np
from numba import njit

# Helper function to calculate Reynolds number
def reynolds_number(density, velocity, characteristic_length, viscosity):
    """
    Calculate the Reynolds number.
    
    Parameters:
    - density: float, Density of the fluid.
    - velocity: float, Characteristic velocity of the flow.
    - characteristic_length: float, Characteristic length (e.g., diameter of a cylinder).
    - viscosity: float, Viscosity of the fluid.

    Returns:
    - float, Reynolds number.
    """
    return (density * velocity * characteristic_length) / viscosity

# Helper function to estimate drag coefficient
def drag_coefficient(reynolds_number):
    """
    Estimate the drag coefficient based on Reynolds number.
    Note: This is a very simplified version for educational purposes.
    
    Parameters:
    - reynolds_number: float, Reynolds number.

    Returns:
    - float, Drag coefficient.
    """
    if reynolds_number < 1:
        return 24 / reynolds_number
    elif reynolds_number < 10:
        return 23.9 / reynolds_number + 0.963
    else:
        return 0.4 + 0.86 / np.sqrt(reynolds_number)

# Function to generate streamlines
def generate_streamlines(velocity_field):
    """
    Generate streamlines from the velocity field.
    
    Parameters:
    - velocity_field: np.array, 3D velocity field of the flow.

    Returns:
    - list, Streamlines represented as lists of (x, y, z) tuples.
    """
    streamlines = []
    
    def trace_streamline(start_point):
        x, y, z = start_point
        streamline = [(x, y, z)]
        while x > 0 and y > 0 and z > 0:
            vx, vy, vz = velocity_field[x, y, z]
            x += vx
            y += vy
            z += vz
            if x < 0 or y < 0 or z < 0: break
            streamline.append((x, y, z))
        return streamline
    
    for i in range(velocity_field.shape[0]):
        for j in range(velocity_field.shape[1]):
            for k in range(velocity_field.shape[2]):
                streamline = trace_streamline((i, j, k))
                if len(streamline) > 1:
                    streamlines.append(streamline)
    
    return streamlines

# Function to calculate velocity field using simplified Navier-Stokes (3D)
@njit
def calculate_velocity_field(density, viscosity, force_field, pressure_field, velocity_field, dt=0.1):
    """
    Simplified calculation of velocity field using the Navier-Stokes equation.
    Note: This is highly simplified for demonstration purposes.
    
    Parameters:
    - density: float, Density of the fluid.
    - viscosity: float, Viscosity of the fluid.
    - force_field: np.array, 3D array representing the external forces.
    - pressure_field: np.array, 3D array representing the pressure field.
    - velocity_field: np.array, 3D velocity field of the flow.
    - dt: float, Time step.
    
    Returns:
    - np.array, Updated velocity field.
    """
    nu = viscosity / density
    rho = density
    
    u = velocity_field[:, :, :, 0]
    v = velocity_field[:, :, :, 1]
    w = velocity_field[:, :, :, 2]

    u_t = (-u * (u[1:, :] - u[:-1, :]) / dx - v * (u[:, 1:] - u[:, :-1]) / dy - w * (u[:, :, 1:] - u[:, :, :-1]) / dz +
           nu * ((u[1:, 1:, :] - 2 * u[1:, :, :] + u[:-1, :, :]) / (dx**2) +
                 (u[:, 1:, :] - 2 * u[:, :, :] + u[:, :-1, :]) / (dy**2) +
                 (u[:, :, 1:] - 2 * u[:, :, :] + u[:, :, :-1]) / (dz**2)) -
           (pressure_field[1:, :, :] - pressure_field[:-1, :, :]) / dx
          )
    
    v_t = (-u * (v[1:, :] - v[:-1, :]) / dx - v * (v[:, 1:] - v[:, :-1]) / dy - w * (v[:, :, 1:] - v[:, :, :-1]) / dz +
           nu * ((v[1:, 1:, :] - 2 * v[1:, :, :] + v[:-1, :, :]) / (dx**2) +
                 (v[:, 1:, :] - 2 * v[:, :, :] + v[:, :-1, :]) / (dy**2) +
                 (v[:, :, 1:] - 2 * v[:, :, :] + v[:, :, :-1]) / (dz**2)) -
           (pressure_field[:, 1:, :] - pressure_field[:, :-1, :]) / dy
          )
    
    w_t = (-u * (w[1:, :] - w[:-1, :]) / dx - v * (w[:, 1:] - w[:, :-1]) / dy - w * (w[:, :, 1:] - w[:, :, :-1]) / dz +
           nu * ((w[1:, 1:, :] - 2 * w[1:, :, :] + w[:-1, :, :]) / (dx**2) +
                 (w[:, 1:, :] - 2 * w[:, :, :] + w[:, :-1, :]) / (dy**2) +
                 (w[:, :, 1:] - 2 * w[:, :, :] + w[:, :, :-1]) / (dz**2)) -
           (pressure_field[:, :, 1:] - pressure_field[:, :, :-1]) / dz
          )

    u = u + dt * u_t 
    v = v + dt * v_t 
    w = w + dt * w_t 

    return np.stack([u, v, w], axis=-1)

# Function to calculate pressure field using a simple Poisson solver
@njit
def calculate_pressure_field(velocity_field, dx, dy, dz, alpha, max_iter=500, tolerance=1e-6):
    """
    Calculate the pressure field using a simplified Poisson solver.

    Parameters:
    - velocity_field: np.array, 3D velocity field of the flow.
    - dx: float, Grid spacing in x direction.
    - dy: float, Grid spacing in y direction.
    - dz: float, Grid spacing in z direction.
    - alpha: float, Relaxation factor.
    - max_iter: int, Maximum number of iterations.
    - tolerance: float, Convergence tolerance.
    
    Returns:
    - np.array, Pressure field.
    """
    u = velocity_field[:, :, :, 0]
    v = velocity_field[:, :, :, 1]
    w = velocity_field[:, :, :, 2]
    
    p = np.zeros_like(u)
    
    for _ in range(max_iter):
        p_new = np.copy(p)
        
        p_new[1:-1, 1:-1, 1:-1] = (
            (p[1:-1, 1:-1, :-2] + p[1:-1, 1:-1, 2:]) * dy**2 * dz**2 +
            (p[1:-1, :-2, 1:-1] + p[1:-1, 2:, 1:-1]) * dx**2 * dz**2 +
            (((alpha * u[1:-1, 1:-1, :-1] - u[:-1, 1:-1, :-1])**2 -
              (alpha * u[1:-1, 1:-1, 1:] - u[:-1, 1:-1, 1:])**2) / dx**2 +
             ((v[1:-1, :-1, 1:-1] - v[:-1, :-1, 1:-1])**2 -
              (alpha * v[1:-1, 1:, 1:-1] - v[:-1, 1:, 1:-1])**2) / dy**2 +
             ((w[:-1, 1:-1, 1:-1] - w[:-1, 1:-1, :-1])**2 -
              (alpha * w[1:, 1:-1, 1:-1] - w[1:, 1:-1, :-1])**2) / dz**2)
        ) / (2 * (dx**2 + dy**2 + dz**2))
        
        err = np.abs((p[1:-1, 1:-1, 1:-1] - p_new[1:-1, 1:-1, 1:-1]))
        if np.max(err) < tolerance:
            break
        
        p = p_new

    # Apply boundary conditions
    p[0] = p[1]
    p[-1] = p[-2]
    p[:, 0] = p[:, 1]
    p[:, -1] = p[:, -2]
    p[:, :, 0] = p[:, :, 1]
    p[:, :, -1] = p[:, :, -2]
    
    return p

# Placeholder functions to demonstrate structure
def handle_boundary_conditions():
    pass

def particle_advection(velocity_field):
    pass

def vorticity_calculation(velocity_field):
    pass

def main():
    # Example usage of the functions
    density = 1.225  # kg/m^3 (air density at sea level)
    viscosity = 1.81e-5  # Pa*s (viscosity of air at sea level)
    dx, dy, dz = 0.1, 0.1, 0.1  # Grid spacing
    size_x, size_y, size_z = 10, 10, 10  # Domain size
    time_step = 0.01  # Time step
    
    U = np.zeros((size_x, size_y, size_z, 3))
    F = np.zeros_like(U)
    P = np.zeros((size_x, size_y, size_z))
    
    # Initialize velocity and pressure fields
    U = np.random.rand(size_x, size_y, size_z, 3) - 0.5
    P = np.zeros_like(U[:, :, :, 0])
    
    # Update velocity field
    U = calculate_velocity_field(density, viscosity, F, P, U, dt=time_step)
    
    # Update pressure field
    P = calculate_pressure_field(U, dx, dy, dz, alpha=1.0)

# Example usage
if __name__ == "__main__":
    main()
C:\mygit\BLazy\repo\3dsim\utils\car_model.py
Language detected: python
"""
3D Car Model Module

This module provides a CarModel class to generate and manipulate a 3D car model.
"""

import numpy as np
from pyrr import Vector3, vector3, geometry

class CarModel:
    def __init__(self, length=4.5, width=1.8, height=1.5, hood_angle=20, rear_angle=-15):
        """
        Initialize the CarModel with customizable parameters.

        :param length: Length of the car in meters.
        :param width: Width of the car in meters.
        :param height: Height of the car in meters.
        :param hood_angle: Hood angle in degrees.
        :param rear_angle: Rear angle in degrees.
        """
        self.length = length
        self.width = width
        self.height = height
        self.hood_angle = hood_angle
        self.rear_angle = rear_angle

    def generate_basic_car_geometry(self):
        """
        Generate the vertices and indices for the basic car geometry.

        :return: A tuple (vertices, indices)
        """
        length, width, height, self.hood_angle, self.rear_angle = self.length, self.width, self.height, self.hood_angle, self.rear_angle
        vertices = np.array([
            [0, 0, 0],  # Front Bottom Left
            [length, 0, 0],  # Front Bottom Right
            [length, width, 0],  # Back Bottom Right
            [0, width, 0],  # Back Bottom Left
            [length, 0, height],  # Front Top Right
            [0, 0, height],  # Front Top Left
            [length, width, height],  # Back Top Right
            [0, width, height]  # Back Top Left
        ], dtype=np.float32)

        indices = np.array([
            0, 2, 1,
            1, 2, 3,
            4, 5, 6,
            6, 7, 4,
            0, 4, 5,
            5, 4, 1,
            0, 3, 7,
            7, 3, 4,
            2, 6, 7,
            7, 6, 3,
            2, 7, 6,
            6, 7, 3
        ], dtype=np.uint32)

        return vertices, indices

    def create_mesh(self):
        """
        Generate the mesh based on generated vertices and indices.

        :return: The generated mesh.
        """
        vertices, indices = self.generate_basic_car_geometry()
        mesh = geometry.create_mesh(vertices=vertices, indices=indices, calculate_normals=True)
        return mesh

    def update_parameters(self, length=None, width=None, height=None, hood_angle=None, rear_angle=None):
        """
        Update model parameters.

        :param length: New length of the car.
        :param width: New width of the car.
        :param height: New height of the car.
        :param hood_angle: New hood angle.
        :param rear_angle: New rear angle.
        """
        if length is not None:
            self.length = length
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if hood_angle is not None:
            self.hood_angle = hood_angle
        if rear_angle is not None:
            self.rear_angle = rear_angle

    def compute_aerodynamic_properties(self):
        """
        Compute the aerodynamic properties such as surface area.

        :return: Aerodynamic surface area.
        """
        vertices, _ = self.generate_basic_car_geometry()
        front_area = np.linalg.norm(np.cross(vertices[4] - vertices[5], vertices[5] - vertices[0]))
        rear_area = np.linalg.norm(np.cross(vertices[7] - vertices[2], vertices[2] - vertices[3]))
        top_area = np.linalg.norm(np.cross(vertices[4] - vertices[0], vertices[0] - vertices[1]))

        aerodynamic_surface_area = front_area + rear_area + top_area
        return aerodynamic_surface_area

    def optimize_mesh(self):
        """
        Perform mesh optimization.

        This is a placeholder method for mesh optimization logic.
        """
        # Placeholder for mesh optimization logic
        pass

# Example Usage:
# car_model = CarModel(length=4.5, width=1.8, height=1.5, hood_angle=20, rear_angle=-15)
# car_mesh = car_model.create_mesh()
# print(f"Aerodynamic Surface Area: {car_model.compute_aerodynamic_properties()} m^2")
C:\mygit\BLazy\repo\3dsim\main.py
Language detected: python
"""
Main Python script for the 3D car aerodynamics simulation.
This script initializes the 3D environment, sets up the camera system,
implements a GUI for parameter adjustment, loads shader programs, creates
the car model, and runs the main simulation loop.
"""

import pygame
from pygame.locals import *
import moderngl
import numpy as np

# Initialize Pygame and set up OpenGL context
def init_pygame():
    """
    Initialize pygame and create a window with an OpenGL context.
    """
    pygame.init()
    pygame.display.gl_set_attribute(GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(GL_CONTEXT_PROFILE_MASK, GL_CONTEXT_PROFILE_CORE)
    screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    return screen

# Define Camera class for managing the camera
class Camera:
    """
    Camera class for managing the view matrix and interactive controls.
    """

    def __init__(self):
        self.position = np.array([0, 1, -5], dtype=np.float32)
        self.yaw, self.pitch = -90.0, 0.0
        self.update_view_matrix()

    def update_view_matrix(self):
        """
        Update the view matrix based on current camera position and orientation.
        """
        mat4 = moderngl.math.mat4
        yaw_cos = np.cos(np.radians(self.yaw))
        yaw_sin = np.sin(np.radians(self.yaw))
        pitch_cos = np.cos(np.radians(self.pitch))
        pitch_sin = np.sin(np.radians(self.pitch))

        view_translation = mat4.translation((-self.position[0], -self.position[1], -self.position[2]))
        x_axis = moderngl.math.vec3((pitch_sin * yaw_cos, pitch_sin * yaw_sin, pitch_cos))
        y_axis = moderngl.math.vec3((-yaw_sin, yaw_cos, 0))
        z_axis = -moderngl.math.cross(x_axis, y_axis)

        yaw_rotation = mat4.yrotation(np.radians(self.yaw))
        pitch_rotation = mat4.xrotation(np.radians(self.pitch))
        view_rotation = mat4.transpose(yaw_rotation * pitch_rotation)

        self.view_matrix = value.reshape((4, 4))

    def rotate_pitch(self, angle):
        """
        Rotate the camera around the x-axis.
        """
        self.pitch += angle

    def rotate_yaw(self, angle):
        """
        Rotate the camera around the y-axis.
        """
        self.yaw += angle

    def move_forward(self, distance):
        """
        Move the camera forward.
        """
        self.position += distance * moderngl.math.normalize(
            moderngl.math.vec3(moderngl.math.rotate(self.yaw)(moderngl.math.X_AXIS))
        )

    def move_backward(self, distance):
        """
        Move the camera backward.
        """
        self.move_forward(-distance)

    def strafe_left(self, distance):
        """
        Move the camera left.
        """
        self.position += distance * moderngl.math.normalize(
            moderngl.math.vec3(moderngl.math.rotate(self.yaw + 90)(moderngl.math.X_AXIS))
        )

    def strafe_right(self, distance):
        """
        Move the camera right.
        """
        self.strafe_left(-distance)

# Implement the GuiController for adjusting simulation parameters
class GuiController:
    """
    GUI controller class for adjusting various simulation parameters.
    """

    def __init__(self, car):
        self.car = car
        self.wind_speed = 0.0
        self.viscosity = 1.0
        self.particle_density = 100
        self.streamlines = True
        # Add more parameters and methods...

# Define CarModel class
class CarModel:
    """
    Class for loading and rendering the car model.
    """
    def __init__(self, ctx):
        self.ctx = ctx
        # Add code to load and compile shaders and vertex data

    def render(self):
        """
        Render the car model.
        """
        # Add code to render the model

# Define MainSimulation class
class MainSimulation:
    """
    Main simulation class that initializes everything and runs the simulation loop.
    """

    def __init__(self):
        self.screen = init_pygame()
        self.clock = pygame.time.Clock()
        self.ctx = moderngl.create_context()
        self.camera = Camera()
        self.car = CarModel(self.ctx)
        self.gui_controller = GuiController(self.car)
        # Initialize other components...
    
    def simulate(self):
        """
        Main simulation loop that handles events, updates the model, renders, etc.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle keyboard and mouse events to control the camera
                # Use pygame and moderngl to handle rendering, updating, etc.

            # Update camera controls
            # Perform fluid dynamics calculations
            # Update particle system
            # Interact with the GUI
            # Render the scene
            # Update the display

            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    sim = MainSimulation()
    sim.simulate()
