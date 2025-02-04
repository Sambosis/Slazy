C:\mygit\BLazy\repo\3dsim\main.py
Language detected: python
import pygame
import moderngl
import numpy as np
import math
import random
import time

class Car:
    def __init__(self, ctx, length=4.5, width=1.8, height=1.4, color=(0.8, 0.2, 0.2)):
        self.ctx = ctx
        self.length = length
        self.width = width
        self.height = height
        self.color = color
        self.pitch = 0.0
        self.yaw = 0.0
        self.position = (0.0, 0.0, 0.0)

        # Create cube vertices for the car (simplified representation)
        vertices = np.array([
            # Front face
            [-0.5*width, -0.5*height,  0.5*length],  # 0
            [ 0.5*width, -0.5*height,  0.5*length],  # 1
            [ 0.5*width,  0.5*height,  0.5*length],  # 2
            [-0.5*width,  0.5*height,  0.5*length],  # 3
            # Back face
            [-0.5*width, -0.5*height, -0.5*length],  # 4
            [ 0.5*width, -0.5*height, -0.5*length],  # 5
            [ 0.5*width,  0.5*height, -0.5*length],  # 6
            [-0.5*width,  0.5*height, -0.5*length],  # 7
            # Top face
            [-0.5*width,  0.5*height,  0.5*length],  # 8 (same as 3)
            [ 0.5*width,  0.5*height,  0.5*length],  # 9 (same as 2)
            [ 0.5*width,  0.5*height, -0.5*length],  # 10 (same as 6)
            [-0.5*width,  0.5*height, -0.5*length],  # 11 (same as 7)
            # Bottom face
            [-0.5*width, -0.5*height,  0.5*length],  # 12 (same as 0)
            [ 0.5*width, -0.5*height,  0.5*length],  # 13 (same as 1)
            [ 0.5*width, -0.5*height, -0.5*length],  # 14 (same as 5)
            [-0.5*width, -0.5*height, -0.5*length],  # 15 (same as 4)
            # Right face
            [ 0.5*width, -0.5*height,  0.5*length],  # 16 (same as 1)
            [ 0.5*width, -0.5*height, -0.5*length],  # 17 (same as 5)
            [ 0.5*width,  0.5*height, -0.5*length],  # 18 (same as 6)
            [ 0.5*width,  0.5*height,  0.5*length],  # 19 (same as 2)
            # Left face
            [-0.5*width, -0.5*height,  0.5*length],  # 20 (same as 0)
            [-0.5*width, -0.5*height, -0.5*length],  # 21 (same as 4)
            [-0.5*width,  0.5*height, -0.5*length],  # 22 (same as 7)
            [-0.5*width,  0.5*height,  0.5*length],  # 23 (same as 3)
        ], dtype='f4')

        indices = np.array([
            0, 1, 2, 0, 2, 3,       # front
            4, 5, 6, 4, 6, 7,       # back
            8, 9, 10, 8, 10, 11,     # top
            12, 13, 14, 12, 14, 15,    # bottom
            16, 17, 18, 16, 18, 19,    # right
            20, 21, 22, 20, 22, 23     # left
        ], dtype='i4')

        self.car_vbo = ctx.buffer(vertices)
        self.car_ibo = ctx.buffer(indices)
        self.car_program = ctx.program(
            vertex_shader='''
                #version 330 core
                in vec3 in_position;
                uniform mat4 model_matrix;
                uniform mat4 projection_matrix;
                uniform mat4 view_matrix;
                void main() {
                    gl_Position = projection_matrix * view_matrix * model_matrix * vec4(in_position, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330 core
                uniform vec3 car_color;
                out vec4 f_color;
                void main() {
                    f_color = vec4(car_color, 1.0);
                }
            '''
        )
        self.car_vao = ctx.vertex_array(self.car_program, self.car_vbo, index_buffer=self.car_ibo, attributes=['in_position'])

    def render(self, projection_matrix, view_matrix):
        model_matrix = np.identity(4, dtype='f4')
        model_matrix = model_matrix @ self.rotz(self.yaw)
        model_matrix = model_matrix @ self.rotx(self.pitch)
        model_matrix[3, :3] = self.position  # Translation

        self.car_program['model_matrix'] = model_matrix
        self.car_program['projection_matrix'] = projection_matrix
        self.car_program['view_matrix'] = view_matrix
        self.car_program['car_color'] = self.color
        self.car_vao.render(mode=moderngl.TRIANGLES)

    def rotx(self, angle):
        m = np.identity(4, dtype='f4')
        m[1:3, 1:3] = [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
        return m

    def roty(self, angle):
        m = np.identity(4, dtype='f4')
        m[[0, 2], [0, 2]] = np.cos(angle)
        m[0, 2] = np.sin(angle)
        m[2, 0] = -np.sin(angle)
        return m

    def rotz(self, angle):
        m = np.identity(4, dtype='f4')
        m[0:2, 0:2] = [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
        return m


class FlowSimulation:
    def __init__(self, ctx, num_particles=10000, wind_speed=(1.0, 0.0, 0.0), air_density=1.225):
        self.ctx = ctx
        self.num_particles = num_particles
        self.wind_speed = np.array(wind_speed, dtype='f4')
        self.air_density = air_density
        self.particle_positions = np.random.uniform(-5, 5, size=(num_particles, 3)).astype('f4')
        self.particle_velocities = np.zeros((num_particles, 3), dtype='f4') + self.wind_speed

        self.particle_vbo = ctx.buffer(self.particle_positions)
        self.particle_program = ctx.program(
            vertex_shader='''
                #version 330 core
                in vec3 in_position;
                uniform mat4 projection_matrix;
                uniform mat4 view_matrix;
                uniform float particle_size;
                void main() {
                    gl_PointSize = particle_size;
                    gl_Position = projection_matrix * view_matrix * vec4(in_position, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330 core
                out vec4 f_color;
                void main() {
                    f_color = vec4(0.2, 0.8, 1.0, 0.5); // Light blue, semi-transparent
                }
            '''
        )
        self.particle_vao = ctx.vertex_array(self.particle_program, self.particle_vbo, attributes=['in_position'])
        self.particle_size = 3.0

    def update_particles(self, dt, car):
        # Basic wind influence (constant wind)
        self.particle_velocities[:, :] = self.wind_speed

        # Very simple car interaction (particles in car volume are pushed away - super basic for demo)
        car_min_x = car.position[0] - car.width * 0.5
        car_max_x = car.position[0] + car.width * 0.5
        car_min_y = car.position[1] - car.height * 0.5
        car_max_y = car.position[1] + car.height * 0.5
        car_min_z = car.position[2] - car.length * 0.5
        car_max_z = car.position[2] + car.length * 0.5

        for i in range(self.num_particles):
            pos = self.particle_positions[i]
            if (car_min_x < pos[0] < car_max_x and
                car_min_y < pos[1] < car_max_y and
                car_min_z < pos[2] < car_max_z):
                # Simple push out - just reverse velocity component towards car center.
                car_center = car.position
                direction_from_center = pos - car_center
                if np.linalg.norm(direction_from_center) > 0:
                    direction_from_center = direction_from_center / np.linalg.norm(direction_from_center)
                    self.particle_velocities[i] += direction_from_center * 10.0 # Push particles out more strongly

        self.particle_positions += self.particle_velocities * dt

        # Reset particles that go too far from origin - for visualization loop.
        reset_distance = 20.0
        for i in range(self.num_particles):
            if np.linalg.norm(self.particle_positions[i]) > reset_distance:
                self.particle_positions[i] = np.random.uniform(-5, 5, size=(3)).astype('f4')


        # Update VBO with new positions
        self.particle_vbo.write(self.particle_positions)

    def render(self, projection_matrix, view_matrix):
        self.particle_program['projection_matrix'] = projection_matrix
        self.particle_program['view_matrix'] = view_matrix
        self.particle_program['particle_size'] = self.particle_size
        self.particle_vao.render(mode=moderngl.POINTS)

class Camera:
    def __init__(self, eye=(0, 3, 5), target=(0, 0, 0), up=(0, 1, 0)):
        self.eye = np.array(eye, dtype='f4')
        self.target = np.array(target, dtype='f4')
        self.up = np.array(up, dtype='f4')
        self.distance = np.linalg.norm(self.eye - self.target)
        self.rotation_x = 0.0
        self.rotation_y = 0.0

    def update_view_matrix(self):
        forward = normalize(self.target - self.eye)
        side = normalize(np.cross(forward, self.up))
        up = normalize(np.cross(side, forward))

        view_matrix = np.identity(4, dtype='f4')
        view_matrix[:3, 0] = side
        view_matrix[:3, 1] = up
        view_matrix[:3, 2] = -forward  # Negate forward to look in +Z in world space
        view_matrix[:3, 3] = self.eye

        return view_matrix

    def rotate_camera(self, delta_x, delta_y, sensitivity=0.01):
        self.rotation_x += delta_x * sensitivity
        self.rotation_y += delta_y * sensitivity

        # Clamp vertical rotation to prevent flipping
        self.rotation_y = np.clip(self.rotation_y, -np.pi / 2, np.pi / 2)

        # Calculate new camera position in spherical coordinates
        self.eye[0] = self.target[0] + self.distance * np.sin(self.rotation_x) * np.cos(self.rotation_y)
        self.eye[1] = self.target[1] + self.distance * np.sin(self.rotation_y)
        self.eye[2] = self.target[2] + self.distance * np.cos(self.rotation_x) * np.cos(self.rotation_y)

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def main():
    pygame.init()
    size = (1280, 720)
    pygame.display.set_mode(size, flags=pygame.DOUBLEBUF | pygame.OPENGL)

    ctx = moderngl.create_context()

    car = Car(ctx)
    flow_sim = FlowSimulation(ctx)
    camera = Camera()

    projection_matrix = np.identity(4, dtype='f4')
    fov = 60.0
    aspect_ratio = size[0] / size[1]
    near_plane = 0.1
    far_plane = 100.0
    projection_matrix = perspective_projection(fov, aspect_ratio, near_plane, far_plane)

    last_time = time.time()
    running = True
    mouse_pressed = False

    # UI parameters
    ui_params = {
        "car_length": car.length,
        "car_width": car.width,
        "car_height": car.height,
        "car_pitch": 0.0,
        "car_yaw": 0.0,
        "wind_speed_x": flow_sim.wind_speed[0],
        "wind_speed_y": flow_sim.wind_speed[1],
        "wind_speed_z": flow_sim.wind_speed[2],
        "air_density": flow_sim.air_density,
        "visualization_density": flow_sim.num_particles
    }


    font = pygame.font.Font(None, 24)

    while running:
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button
                    mouse_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pressed = False
            if event.type == pygame.MOUSEMOTION:
                if mouse_pressed:
                    dx, dy = event.rel
                    camera.rotate_camera(dx, dy)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    car.yaw += 0.05
                if event.key == pygame.K_RIGHT:
                    car.yaw -= 0.05
                if event.key == pygame.K_UP:
                    car.pitch += 0.05
                if event.key == pygame.K_DOWN:
                    car.pitch -= 0.05
                if event.key == pygame.K_w:
                    flow_sim.wind_speed[2] += 0.1
                if event.key == pygame.K_s:
                    flow_sim.wind_speed[2] -= 0.1
                if event.key == pygame.K_a:
                    flow_sim.wind_speed[0] -= 0.1
                if event.key == pygame.K_d:
                    flow_sim.wind_speed[0] += 0.1
                if event.key == pygame.K_q:
                    flow_sim.num_particles = max(100, flow_sim.num_particles - 1000)
                    flow_sim.particle_positions = np.random.uniform(-5, 5, size=(flow_sim.num_particles, 3)).astype('f4')
                    flow_sim.particle_vbo = ctx.buffer(flow_sim.particle_positions)
                    flow_sim.particle_vao = ctx.vertex_array(flow_sim.particle_program, flow_sim.particle_vbo, attributes=['in_position'])

                if event.key == pygame.K_e:
                    flow_sim.num_particles += 1000
                    flow_sim.particle_positions = np.random.uniform(-5, 5, size=(flow_sim.num_particles, 3)).astype('f4')
                    flow_sim.particle_vbo = ctx.buffer(flow_sim.particle_positions)
                    flow_sim.particle_vao = ctx.vertex_array(flow_sim.particle_program, flow_sim.particle_vbo, attributes=['in_position'])


        flow_sim.wind_speed = np.array([ui_params["wind_speed_x"], ui_params["wind_speed_y"], ui_params["wind_speed_z"]], dtype='f4')
        flow_sim.num_particles = ui_params["visualization_density"]
        car.length = ui_params["car_length"]
        car.width = ui_params["car_width"]
        car.height = ui_params["car_height"]
        car.pitch = ui_params["car_pitch"]
        car.yaw = ui_params["car_yaw"]


        flow_sim.update_particles(delta_time, car)

        ctx.clear(0.1, 0.2, 0.3) # Nice dark blue background
        ctx.enable(moderngl.DEPTH_TEST | moderngl.BLEND) # Enable depth testing for 3D and blending for particles
        ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA # Standard alpha blending

        view_matrix = camera.update_view_matrix()

        car.render(projection_matrix, view_matrix)
        flow_sim.render(projection_matrix, view_matrix)

        # --- UI Display ---
        text_surface = font.render(f"Wind Speed: {flow_sim.wind_speed}", True, (255, 255, 255))
        pygame_texture = ctx.texture(text_surface.get_size(), 4, text_surface.get_buffer())
        pygame_texture.use(location=0) # Bind texture to texture unit 0. Not really used in shaders yet, just for display.
        ctx.copy_framebuffer(pygame_texture.fbo)
        screen.blit(pygame_texture.texture, (10, 10)) # Assuming 'screen' is pygame's display surface (needs import)
        pygame.display.flip() # Should be pygame.display.get_surface() or similar, but for now pygame.display.flip() often works.

        pygame.display.flip()


    pygame.quit()

def perspective_projection(fov, aspect, near, far):
    f = 1.0 / np.tan(np.radians(fov) / 2.0)
    projection_matrix = np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ], dtype='f4')
    return projection_matrix


if __name__ == "__main__":
    main()
C:\mygit\BLazy\repo\3dsim\shaders\vertex_shader.glsl
Language detected: glsl
#version 300 es
precision mediump float;

// Vertex attributes
in vec3 a_position;
in vec3 a_normal;

// Uniforms (matrices)
uniform mat4 u_modelMatrix;
uniform mat4 u_viewMatrix;
uniform mat4 u_projectionMatrix;
uniform mat4 u_normalMatrix; // For correct normal transformations

// Varyings (to be passed to fragment shader)
out vec3 v_worldPosition;
out vec3 v_worldNormal;

void main() {
    // 1. Vertex positions and transformations
    vec4 worldPosition = u_modelMatrix * vec4(a_position, 1.0);
    vec4 viewPosition = u_viewMatrix * worldPosition;
    gl_Position = u_projectionMatrix * viewPosition;

    // Pass world position to fragment shader
    v_worldPosition = worldPosition.xyz;

    // 2. Normal calculations for lighting
    // Transform normal to world space. Use mat3 to avoid translation issues and for efficiency if normalMatrix is correctly computed
    v_worldNormal = normalize(mat3(u_normalMatrix) * a_normal);
}
C:\mygit\BLazy\repo\3dsim\flow_simulation.py
Language detected: python
import numpy as np
import moderngl
import pyrr
import math
import random
import time
import concurrent.futures

class AirflowSimulator:
    def __init__(self, num_particles, simulation_area_size=(10, 10, 10), initial_velocity_range=(-1, 1), viscosity=0.01, dt=0.01, turbulence_factor=0.01, boundary_damping=0.8):
        """
        Initializes the AirflowSimulator.

        Args:
            num_particles (int): Number of particles in the simulation.
            simulation_area_size (tuple): Size of the simulation area (x, y, z).
            initial_velocity_range (tuple): Range for initial random velocities (-v, v).
            viscosity (float): Viscosity of the air.
            dt (float): Time step for simulation.
            turbulence_factor (float): Factor controlling turbulence magnitude.
            boundary_damping (float): Damping factor for velocity at boundaries.
        """
        self.num_particles = num_particles
        self.simulation_area_size = np.array(simulation_area_size)
        self.initial_velocity_range = initial_velocity_range
        self.viscosity = viscosity
        self.dt = dt
        self.turbulence_factor = turbulence_factor
        self.boundary_damping = boundary_damping

        self.particles_position = np.random.rand(num_particles, 3) * self.simulation_area_size
        initial_velocities = np.random.uniform(initial_velocity_range[0], initial_velocity_range[1], (num_particles, 3))
        self.particles_velocity = initial_velocities

        # Placeholder for car model interaction (can be expanded)
        self.car_position = np.array([0, 0, 0]) # Example car position
        self.car_size = np.array([2, 1, 0.5]) # Example car size (length, width, height - in x, y, z)

        # For optimization (placeholder for now, can use Numba for more performance)
        self.executor = concurrent.futures.ThreadPoolExecutor() # Or ProcessPoolExecutor for CPU-bound tasks

    def set_car_parameters(self, car_position, car_size):
        """
        Updates the car parameters for interaction.

        Args:
            car_position (np.array): Position of the car (3D).
            car_size (np.array): Size of the car (3D - e.g., length, width, height).
        """
        self.car_position = np.array(car_position)
        self.car_size = np.array(car_size)

    def update_parameter(self, parameter_name, new_value):
        """
        Updates a simulation parameter in real-time.

        Args:
            parameter_name (str): The name of the parameter to update (e.g., 'viscosity', 'dt', 'turbulence_factor').
            new_value (float): The new value for the parameter.
        """
        if hasattr(self, parameter_name):
            setattr(self, parameter_name, new_value)
        else:
            print(f"Parameter '{parameter_name}' not found.")

    def _apply_boundary_conditions(self):
        """
        Applies boundary conditions to particles, reflecting them at the edges
        and applying damping.
        """
        for i in range(3): # Iterate through x, y, z dimensions
            # Upper boundary
            boundary_max = self.simulation_area_size[i]
            exceed_max_indices = self.particles_position[:, i] > boundary_max
            self.particles_position[exceed_max_indices, i] = boundary_max
            self.particles_velocity[exceed_max_indices, i] *= -self.boundary_damping # Reverse and dampen velocity

            # Lower boundary
            exceed_min_indices = self.particles_position[:, i] < 0
            self.particles_position[exceed_min_indices, i] = 0
            self.particles_velocity[exceed_min_indices, i] *= -self.boundary_damping # Reverse and dampen velocity


    def _calculate_viscosity_force(self):
        """
        Simplified viscosity force - dampens velocities to simulate viscous effects.
        """
        return -self.viscosity * self.particles_velocity

    def _calculate_turbulence_force(self):
        """
        Simplified turbulence force - adds random noise to simulate turbulent fluctuations.
        """
        return self.turbulence_factor * np.random.randn(self.num_particles, 3)

    def _calculate_car_interaction_force(self):
        """
        Simplified car interaction - deflects particles around a box representing the car.
        This is a VERY basic model. More sophisticated methods would require CFD.
        """
        force = np.zeros((self.num_particles, 3))
        car_min = self.car_position - self.car_size / 2.0
        car_max = self.car_position + self.car_size / 2.0

        for i in range(self.num_particles):
            pos = self.particles_position[i]
            vel = self.particles_velocity[i]

            # Simple box collision/deflection
            if (car_min[0] < pos[0] < car_max[0] and
                car_min[1] < pos[1] < car_max[1] and
                car_min[2] < pos[2] < car_max[2]):

                # Very crude deflection - reverse velocity component based on closest face.
                # Improved: use surface normals of the car model for deflection if a proper model is used.
                dist_min_x = abs(pos[0] - car_min[0])
                dist_max_x = abs(pos[0] - car_max[0])
                dist_min_y = abs(pos[1] - car_min[1])
                dist_max_y = abs(pos[1] - car_max[1])
                dist_min_z = abs(pos[2] - car_min[2])
                dist_max_z = abs(pos[2] - car_max[2])

                min_dist = min(dist_min_x, dist_max_x, dist_min_y, dist_max_y, dist_min_z, dist_max_z)

                if min_dist == dist_min_x or min_dist == dist_max_x:
                    force[i, 0] -= 2 * vel[0]  # Reverse x velocity
                elif min_dist == dist_min_y or min_dist == dist_max_y:
                    force[i, 1] -= 2 * vel[1] # Reverse y velocity
                elif min_dist == dist_min_z or min_dist == dist_max_z:
                    force[i, 2] -= 2 * vel[2] # Reverse z velocity


        return force


    def step(self):
        """
        Performs one simulation step.  This is a basic Euler integration step.
        For more accuracy, consider using more advanced integration methods (e.g., Runge-Kutta).
        """
        viscosity_force = self._calculate_viscosity_force()
        turbulence_force = self._calculate_turbulence_force()
        car_force = self._calculate_car_interaction_force()

        total_force = viscosity_force + turbulence_force + car_force # Sum of forces

        # Basic Euler integration
        self.particles_velocity += total_force * self.dt
        self.particles_position += self.particles_velocity * self.dt

        self._apply_boundary_conditions() # Keep particles within simulation area

        return self.particles_position.copy()  # Return a copy for rendering to avoid modification issues


if __name__ == '__main__':
    # Example usage with ModernGL (minimal setup for demonstration - rendering not included, just data generation)
    import time

    num_particles = 5000
    simulator = AirflowSimulator(num_particles=num_particles, simulation_area_size=(20, 10, 10), viscosity=0.02, turbulence_factor=0.03)
    simulator.set_car_parameters(car_position=[5, 5, 2.5], car_size=[4, 2, 1]) # Example car setup

    start_time = time.time()
    frame_count = 0

    try:
        while True: # Simulation loop
            positions = simulator.step() # Get updated particle positions

            # --- ModernGL rendering would go here ---
            # Example: pass 'positions' to a ModernGL buffer and draw points.
            # You would need to set up a ModernGL context, shaders, VAO, VBO, etc.
            # Example pseudocode for rendering preparation:
            # ctx = moderngl.create_context()
            # program = ctx.program(...) # Vertex and Fragment shaders
            # vbo = ctx.buffer(positions.astype('f4').tobytes())
            # vao = ctx.vertex_array(program, [(vbo, '3f', 'in_position')])
            # ... inside render loop:
            # ctx.clear()
            # vao.render(mode=moderngl.POINTS)
            # ctx.gc_collect() # Optional garbage collection
            # window.swap_buffers() # or similar for your windowing system

            frame_count += 1
            if frame_count % 100 == 0: # Print FPS every 100 frames
                elapsed_time = time.time() - start_time
                fps = frame_count / elapsed_time
                print(f"FPS: {fps:.2f}, Particles count: {num_particles}")
                start_time = time.time()
                frame_count = 0


            time.sleep(0.01) # Control simulation speed (adjust as needed)


    except KeyboardInterrupt:
        print("Simulation stopped by user.")
C:\mygit\BLazy\repo\3dsim\ui_controls.py
Language detected: python
import pygame
import numpy as np
import math

class Slider:
    def __init__(self, surface, x, y, w, h, min_val, max_val, initial_val, param_name):
        self.surface = surface
        self.rect = pygame.Rect(x, y, w, h)
        self.thumb_w = 10
        self.thumb_h = h
        self.thumb_rect = pygame.Rect(x, y, self.thumb_w, self.thumb_h)
        self.min_val = min_val
        self.max_val = max_val
        self.current_val = initial_val
        self.param_name = param_name
        self.is_dragging = False
        self._update_thumb_pos()

    def _update_thumb_pos(self):
        ratio = (self.current_val - self.min_val) / (self.max_val - self.min_val) if self.max_val > self.min_val else 0
        self.thumb_rect.x = self.rect.x + int(ratio * (self.rect.width - self.thumb_w))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.thumb_rect.collidepoint(event.pos):
                self.is_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                mouse_x = event.pos[0]
                pos_ratio = min(1, max(0, (mouse_x - self.rect.x) / (self.rect.width - self.thumb_w))) if (self.rect.width - self.thumb_w) > 0 else 0.5
                self.current_val = self.min_val + pos_ratio * (self.max_val - self.min_val)
                self._update_thumb_pos()

    def draw(self):
        pygame.draw.rect(self.surface, (100, 100, 100), self.rect) # Slider track
        pygame.draw.rect(self.surface, (200, 200, 200), self.thumb_rect) # Slider thumb

    def get_value(self):
        return self.current_val

    def set_value(self, value):
        self.current_val = value
        self._update_thumb_pos()

class SimulationUI:
    def __init__(self, screen_width, screen_height):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Simulation UI Controls")
        self.font = pygame.font.Font(None, 24)
        self.running = True
        self.parameters = {
            "car_length": 5.0,
            "car_width": 2.0,
            "car_height": 1.5,
            "car_pitch": 0.0,
            "car_yaw": 0.0,
            "wind_speed": 10.0,
            "air_density": 1.225,
            "visualization_density": 50.0,
        }
        self.sliders = {}
        self.init_ui_elements()

    def init_ui_elements(self):
        slider_y_start = 50
        slider_height = 20
        slider_width = 200
        slider_spacing = 40
        slider_x = 50

        # Car Dimensions
        self.sliders["car_length"] = Slider(self.screen, slider_x, slider_y_start, slider_width, slider_height, 1.0, 10.0, self.parameters["car_length"], "Car Length")
        self.sliders["car_width"] = Slider(self.screen, slider_x, slider_y_start + slider_spacing, slider_width, slider_height, 0.5, 5.0, self.parameters["car_width"], "Car Width")
        self.sliders["car_height"] = Slider(self.screen, slider_x, slider_y_start + 2*slider_spacing, slider_width, slider_height, 0.5, 3.0, self.parameters["car_height"], "Car Height")

        # Car Angles
        self.sliders["car_pitch"] = Slider(self.screen, slider_x, slider_y_start + 4*slider_spacing, slider_width, slider_height, -90.0, 90.0, self.parameters["car_pitch"], "Car Pitch")
        self.sliders["car_yaw"] = Slider(self.screen, slider_x, slider_y_start + 5*slider_spacing, slider_width, slider_height, -180.0, 180.0, self.parameters["car_yaw"], "Car Yaw")

        # Environment Parameters
        self.sliders["wind_speed"] = Slider(self.screen, slider_x, slider_y_start + 7*slider_spacing, slider_width, slider_height, 0.0, 50.0, self.parameters["wind_speed"], "Wind Speed")
        self.sliders["air_density"] = Slider(self.screen, slider_x, slider_y_start + 8*slider_spacing, slider_width, slider_height, 0.1, 2.0, self.parameters["air_density"], "Air Density")
        self.sliders["visualization_density"] = Slider(self.screen, slider_x, slider_y_start + 9*slider_spacing, slider_width, slider_height, 10, 200, self.parameters["visualization_density"], "Vis. Density")

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            for slider in self.sliders.values():
                slider.handle_event(event)

    def update_parameters(self):
        for name, slider in self.sliders.items():
            self.parameters[name] = slider.get_value()

    def draw_ui(self):
        self.screen.fill((50, 50, 50)) # Dark background

        text_y_start = 20
        line_spacing = 20

        # Title
        title_text = self.font.render("Simulation Parameters", True, (255, 255, 255))
        self.screen.blit(title_text, (50, text_y_start))

        # Draw Sliders and Parameter Names
        slider_label_x = 50
        slider_value_x = slider_label_x + 220 # Offset to the right of slider
        slider_y = 50
        slider_spacing = 40

        for name, slider in self.sliders.items():
            slider.draw()
            label_text = self.font.render(f"{slider.param_name}:", True, (255, 255, 255))
            value_text = self.font.render(f"{self.parameters[name]:.2f}", True, (255, 255, 255))
            self.screen.blit(label_text, (slider_label_x, slider_y - 5)) # Slightly above the slider
            self.screen.blit(value_text, (slider_value_x, slider_y - 5 ))
            slider_y += slider_spacing

        # Camera Controls Instructions (Placeholder)
        camera_text = self.font.render("Camera Controls (Placeholder):", True, (255, 255, 255))
        camera_instructions = self.font.render("Functionality to be implemented...", True, (255, 255, 255))
        self.screen.blit(camera_text, (50, slider_y + line_spacing)) # Below last slider
        self.screen.blit(camera_instructions, (50, slider_y + 2*line_spacing))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update_parameters()
            self.draw_ui()
        pygame.quit()

if __name__ == '__main__':
    ui = SimulationUI(800, 600)
    ui.run()
C:\mygit\BLazy\repo\3dsim\requirements.txt
Language detected: text
pygame>=2.5.0
numpy>=1.24.0
moderngl>=5.8.2
moderngl-window>=2.4.4
pyrr>=0.10.3
pillow>=10.0.0
C:\mygit\BLazy\repo\3dsim\particle_system.py
Language detected: python
import numpy as np
import moderngl
import random
from math3d import vec3
from OpenGL.GL import *
from OpenGL.GLU import *
import time

class ParticleSystem:
    def __init__(self, num_particles, simulation_size=10.0, wind_velocity=vec3(1.0, 0.0, 0.0), air_resistance_coefficient=0.1, turbulence_factor=0.01):
        self.num_particles = num_particles
        self.simulation_size = simulation_size
        self.wind_velocity = wind_velocity
        self.air_resistance_coefficient = air_resistance_coefficient
        self.turbulence_factor = turbulence_factor

        self.positions = np.random.uniform(-simulation_size/2, simulation_size/2, size=(num_particles, 3)).astype(np.float32)
        self.velocities = np.random.uniform(-1.0, 1.0, size=(num_particles, 3)).astype(np.float32) * 0.1 # Initial small random velocities
        self.initial_positions = self.positions.copy() # Store initial positions for recycling

    def update_particles(self, dt, car_geometry=None): # car_geometry placeholder for future use
        # Apply wind force
        wind_force = self.wind_velocity * dt
        self.velocities += wind_force

        # Apply air resistance (simplified: force proportional to velocity)
        air_resistance_force = -self.air_resistance_coefficient * self.velocities * dt
        self.velocities += air_resistance_force

        # Apply turbulence (random small force)
        turbulence = np.random.uniform(-self.turbulence_factor, self.turbulence_factor, size=(self.num_particles, 3)).astype(np.float32) * dt
        self.velocities += turbulence

        # Update positions
        self.positions += self.velocities * dt

        # Handle simulation boundaries and recycling (simple box boundaries)
        for i in range(self.num_particles):
            if np.linalg.norm(self.positions[i]) > self.simulation_size * 1.5: # Recycle particles leaving a larger boundary
                self.positions[i] = self.initial_positions[i].copy() # Reset to initial position for simplicity
                self.velocities[i] = np.random.uniform(-1.0, 1.0, 3).astype(np.float32) * 0.1 # Re-initialize velocity

    def set_wind_velocity(self, wind_velocity):
        self.wind_velocity = vec3(*wind_velocity)

    def set_air_resistance(self, air_resistance_coefficient):
        self.air_resistance_coefficient = air_resistance_coefficient

    def set_turbulence_factor(self, turbulence_factor):
        self.turbulence_factor = turbulence_factor

    def set_particle_density(self, num_particles):
        self.num_particles = num_particles
        self.positions = np.random.uniform(-self.simulation_size/2, self.simulation_size/2, size=(num_particles, 3)).astype(np.float32)
        self.velocities = np.random.uniform(-1.0, 1.0, size=(num_particles, 3)).astype(np.float32) * 0.1
        self.initial_positions = self.positions.copy()


class Renderer:
    def __init__(self, particle_system):
        self.ctx = moderngl.create_standalone_context()

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330

                in vec3 in_position;
                uniform mat4 modelview_matrix;
                uniform mat4 projection_matrix;

                void main() {
                    gl_Position = projection_matrix * modelview_matrix * vec4(in_position, 1.0);
                    gl_PointSize = 3.0;
                }
            ''',
            fragment_shader='''
                #version 330

                out vec4 fragColor;

                void main() {
                    fragColor = vec4(1.0, 1.0, 1.0, 1.0); // White particles
                }
            '''
        )
        self.particle_system = particle_system
        self.vbo = self.ctx.buffer(self.particle_system.positions)
        self.vao = self.ctx.vertex_array(self.prog, [(self.vbo, '3f', 'in_position')])

        self.camera_position = vec3(0.0, 0.0, 15.0)
        self.target = vec3(0.0, 0.0, 0.0)
        self.up_vector = vec3(0.0, 1.0, 0.0)

        self.projection_matrix = self.perspective_projection(45.0, 1.0, 0.1, 100.0) # FOV, aspect ratio, near, far

    def update_vbo(self):
        self.vbo.write(self.particle_system.positions)

    def render_frame(self):
        glEnable(GL_PROGRAM_POINT_SIZE) # Enable point size in vertex shader
        self.ctx.clear(0.0, 0.0, 0.0) # Clear to black

        modelview_matrix = self.look_at(self.camera_position, self.target, self.up_vector)

        self.prog['modelview_matrix'] = modelview_matrix
        self.prog['projection_matrix'] = self.projection_matrix

        self.vao.render(mode=moderngl.POINTS)
        self.ctx.finish() # Ensure all commands are processed

    def perspective_projection(self, fov, aspect, near, far):
        f = 1.0 / np.tan(np.radians(fov) / 2.0)
        nf = 1.0 / (near - far)
        return np.array([
            [f / aspect, 0.0, 0.0, 0.0],
            [0.0, f, 0.0, 0.0],
            [0.0, 0.0, (far + near) * nf, -1.0],
            [0.0, 0.0, (2.0 * far * near) * nf, 0.0],
        ], dtype=np.float32).T

    def look_at(self, eye, target, up):
        z = (eye - target).normalized()
        x = up.cross(z).normalized()
        y = z.cross(x).normalized()
        m = np.identity(4, dtype=np.float32)
        m[:3, :3] = np.array([x, y, z])
        m[:3, 3] = -np.array([x.dot(eye), y.dot(eye), z.dot(eye)])
        return m


def main():
    num_particles = 5000
    simulation_size = 10.0
    particle_system = ParticleSystem(num_particles, simulation_size)
    renderer = Renderer(particle_system)

    last_time = time.time()

    while True:
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time

        particle_system.update_particles(dt)
        renderer.update_vbo()
        renderer.render_frame()

        # Performance monitoring (crude frame rate)
        frame_rate = 1.0 / dt if dt > 0 else 0
        print(f"Frame Rate: {frame_rate:.2f} FPS", end='\r')


if __name__ == '__main__':
    main()
C:\mygit\BLazy\repo\3dsim\config.py
Language detected: python
# Configuration file for 3D Car Airflow Simulation

# Window Settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = '3D Car Airflow Simulation'

# Car Default Parameters
DEFAULT_CAR_LENGTH = 4.5  # meters
DEFAULT_CAR_WIDTH = 1.8   # meters
DEFAULT_CAR_HEIGHT = 1.4  # meters
DEFAULT_SURFACE_SMOOTHNESS = 0.8  # 0-1 scale

# Airflow Parameters
DEFAULT_WIND_SPEED = 30.0  # m/s
DEFAULT_AIR_DENSITY = 1.225  # kg/m3
DEFAULT_TEMPERATURE = 20.0  # Celsius
DEFAULT_TURBULENCE_INTENSITY = 0.1  # 0-1 scale

# Visualization Parameters
PARTICLE_COUNT = 10000
PARTICLE_SIZE = 2.0
PARTICLE_TRAIL_LENGTH = 10
PARTICLE_TRAIL_DECAY = 0.95

# Physics Parameters
TIMESTEP = 0.016  # ~60 FPS
SIMULATION_SCALE = 0.1  # Scale factor for visualization

# Camera Settings
CAMERA_INITIAL_POSITION = (0.0, 2.0, -5.0)
CAMERA_INITIAL_TARGET = (0.0, 0.0, 0.0)
CAMERA_MOVEMENT_SPEED = 0.1
CAMERA_ROTATION_SPEED = 0.01

# Colors (RGB format)
BACKGROUND_COLOR = (0.1, 0.1, 0.2, 1.0)
CAR_COLOR = (0.7, 0.7, 0.7, 1.0)
PARTICLE_COLOR = (0.0, 0.6, 1.0, 0.5)
UI_TEXT_COLOR = (255, 255, 255)
UI_BACKGROUND_COLOR = (40, 40, 40)

# Performance Settings
MAX_FPS = 60
MULTITHREADING = True
PARTICLE_BATCH_SIZE = 1000
C:\mygit\BLazy\repo\3dsim\shaders.py
Language detected: python
VERTEX_SHADER = """
#version 330

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_color;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

out vec3 frag_normal;
out vec3 frag_pos;
out vec3 frag_color;

void main() {
    frag_pos = vec3(model * vec4(in_position, 1.0));
    frag_normal = mat3(transpose(inverse(model))) * in_normal;
    frag_color = in_color;
    gl_Position = projection * view * model * vec4(in_position, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 330

in vec3 frag_normal;
in vec3 frag_pos;
in vec3 frag_color;

uniform vec3 light_pos;
uniform vec3 view_pos;

out vec4 out_color;

void main() {
    // Ambient
    float ambient_strength = 0.2;
    vec3 ambient = ambient_strength * vec3(1.0);

    // Diffuse
    vec3 norm = normalize(frag_normal);
    vec3 light_dir = normalize(light_pos - frag_pos);
    float diff = max(dot(norm, light_dir), 0.0);
    vec3 diffuse = diff * vec3(1.0);

    // Specular
    float specular_strength = 0.5;
    vec3 view_dir = normalize(view_pos - frag_pos);
    vec3 reflect_dir = reflect(-light_dir, norm);
    float spec = pow(max(dot(view_dir, reflect_dir), 0.0), 32);
    vec3 specular = specular_strength * spec * vec3(1.0);

    vec3 result = (ambient + diffuse + specular) * frag_color;
    out_color = vec4(result, 1.0);
}
"""

PARTICLE_VERTEX_SHADER = """
#version 330

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_velocity;
layout (location = 2) in float in_life;

uniform mat4 projection;
uniform mat4 view;

out float life;

void main() {
    gl_Position = projection * view * vec4(in_position, 1.0);
    gl_PointSize = max(1.0, 10.0 * in_life);
    life = in_life;
}
"""

PARTICLE_FRAGMENT_SHADER = """
#version 330

in float life;
out vec4 out_color;

uniform vec4 particle_color;

void main() {
    vec2 coord = gl_PointCoord - vec2(0.5);
    float r = length(coord) * 2.0;
    float a = 1.0 - smoothstep(0.8, 1.0, r);
    out_color = particle_color * vec4(1.0, 1.0, 1.0, life * a);
}
"""

if __name__ == '__main__':
    print("Shader programs are defined as Python strings:")
    print("VERTEX_SHADER =\n", VERTEX_SHADER)
    print("\nFRAGMENT_SHADER =\n", FRAGMENT_SHADER)
    print("\nPARTICLE_VERTEX_SHADER =\n", PARTICLE_VERTEX_SHADER)
    print("\nPARTICLE_FRAGMENT_SHADER =\n", PARTICLE_FRAGMENT_SHADER)
C:\mygit\BLazy\repo\3dsim\__init__.py
Language detected: python
# __init__.py
# This file is intentionally left blank to make this directory a Python package.
C:\mygit\BLazy\repo\3dsim\main.py
Language detected: python
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from math import *
import random
import sys

# config.py
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "3D Car Airflow Simulation"
DEFAULT_WIND_SPEED = 5.0
DEFAULT_AIR_DENSITY = 1.225  # kg/m^3 (sea level, standard temperature)
PARTICLE_SIZE = 3.0
CAMERA_ROTATION_SPEED = 0.01
MAX_FPS = 60
UI_TEXT_COLOR = (255, 255, 255)

# car_geometry.py
class CarGeometry:
    def __init__(self):
        # Define car vertices - Simple box shape
        self.vertices = np.array([
            [1, 0, 1], [1, 1, 1], [-1, 1, 1], [-1, 0, 1],
            [1, 0, -1], [1, 1, -1], [-1, 1, -1], [-1, 0, -1]
        ], dtype=np.float32)

        self.faces = [
            (0, 1, 2, 3),  # Front
            (3, 2, 6, 7),  # Left
            (7, 6, 5, 4),  # Back
            (4, 5, 1, 0),  # Right
            (1, 5, 6, 2),  # Top
            (0, 4, 7, 3)   # Bottom
        ]
        self.colors = [(1.0, 0.5, 0.0) for _ in range(6)] # Orange color for each face

    def render(self):
        glPushMatrix()
        glTranslatef(0, 0, 0) # Car position
        glColor3f(1.0, 1.0, 1.0) # White color for car body
        glBegin(GL_QUADS)
        for i, face in enumerate(self.faces):
            glColor3fv(self.colors[i]) # Set face color
            for vertex_index in face:
                glVertex3fv(self.vertices[vertex_index])
        glEnd()
        glPopMatrix()


# particle_system.py
class ParticleSystem:
    def __init__(self, num_particles=500):
        self.num_particles = num_particles
        self.particles = np.random.rand(num_particles, 3).astype(np.float32) * 10 - 5 # Initialize particles randomly in a cube around origin
        self.velocities = np.zeros((num_particles, 3), dtype=np.float32)
        self.particle_colors = np.array([(0.0, 0.0, 1.0, 0.5) for _ in range(num_particles)], dtype=np.float32) # Semi-transparent blue

    def update(self, wind_speed, air_density, car):
        dt = 0.016 # Assuming approximately 60 FPS
        wind_force = np.array([wind_speed, 0, 0], dtype=np.float32) * air_density
        drag_coefficient = 0.01 # Example drag coefficient, adjust as needed

        for i in range(self.num_particles):
            # Basic wind influence
            self.velocities[i] += wind_force * dt

            # Simple drag force (proportional to velocity squared and opposite direction)
            drag_force = -drag_coefficient * air_density * np.linalg.norm(self.velocities[i])**2 * (self.velocities[i] / (np.linalg.norm(self.velocities[i]) + 1e-6)) # avoid division by zero
            self.velocities[i] += drag_force * dt

            self.particles[i] += self.velocities[i] * dt

            # Reset particles if they go too far
            if self.particles[i][0] > 20:
                self.particles[i] = np.random.rand(3).astype(np.float32) * 10 - 5
                self.particles[i][0] -= 10 # Start from behind


    def render(self):
        glPushMatrix()
        glBegin(GL_POINTS)
        for i in range(self.num_particles):
            glColor4fv(self.particle_colors[i])
            glVertex3fv(self.particles[i])
        glEnd()
        glPopMatrix()


class AirflowSimulation:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
        pygame.display.set_caption(WINDOW_TITLE)

        self.setup_gl()
        self.car = CarGeometry()
        self.particles = ParticleSystem()
        self.clock = pygame.time.Clock()

        self.camera_distance = 10.0
        self.camera_angle_x = 0.0
        self.camera_angle_y = 0.0

        # Simulation parameters
        self.wind_speed = DEFAULT_WIND_SPEED
        self.air_density = DEFAULT_AIR_DENSITY
        self.running = True

    def setup_gl(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_POINT_SMOOTH)
        glPointSize(PARTICLE_SIZE)

        # Set up lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, (5.0, 5.0, 5.0, 1.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))

        glClearColor(0.0, 0.0, 0.0, 1.0) # Set clear color to black

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (WINDOW_WIDTH/WINDOW_HEIGHT), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  # Left mouse button
                    self.camera_angle_x += event.rel[0] * CAMERA_ROTATION_SPEED
                    self.camera_angle_y += event.rel[1] * CAMERA_ROTATION_SPEED
                    self.camera_angle_y = max(min(self.camera_angle_y, pi/2), -pi/2)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Mouse wheel up
                    self.camera_distance = max(5.0, self.camera_distance - 1.0)
                elif event.button == 5:  # Mouse wheel down
                    self.camera_distance = min(20.0, self.camera_distance + 1.0)

    def update(self):
        keys = pygame.key.get_pressed()
        # Update wind speed
        if keys[pygame.K_UP]:
            self.wind_speed = min(50.0, self.wind_speed + 0.5)
        if keys[pygame.K_DOWN]:
            self.wind_speed = max(0.0, self.wind_speed - 0.5)

        self.particles.update(self.wind_speed, self.air_density, self.car)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Set up camera
        cam_x = self.camera_distance * cos(self.camera_angle_y) * sin(self.camera_angle_x)
        cam_y = self.camera_distance * sin(self.camera_angle_y)
        cam_z = self.camera_distance * cos(self.camera_angle_y) * cos(self.camera_angle_x)

        gluLookAt(cam_x, cam_y, cam_z,  # Camera position
                  0, 0, 0,              # Look at point
                  0, 1, 0)              # Up vector

        # Draw car
        self.car.render()

        # Draw particles
        self.particles.render()

        # Draw UI
        self.render_ui()

        pygame.display.flip()

    def render_ui(self):
        # Switch to 2D rendering for UI
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)

        # Render text using pygame
        font = pygame.font.Font(None, 36)
        text = font.render(f"Wind Speed: {self.wind_speed:.1f} m/s", True, UI_TEXT_COLOR)
        pygame.display.get_surface().blit(text, (10, 10))

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.render()
            self.clock.tick(MAX_FPS)

def main():
    simulation = AirflowSimulation()
    simulation.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
C:\mygit\BLazy\repo\3dsim\particle_system.py
Language detected: python
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import random
from math import *

# config.py (create this file in the same directory)
class Config:
    PARTICLE_COUNT = 5000
    PARTICLE_TRAIL_LENGTH = 20
    TIMESTEP = 0.01
    DEFAULT_TURBULENCE_INTENSITY = 0.5
    PARTICLE_SIZE = 3.0

config = Config() # Instantiate the class to access attributes
PARTICLE_COUNT = config.PARTICLE_COUNT
PARTICLE_TRAIL_LENGTH = config.PARTICLE_TRAIL_LENGTH
TIMESTEP = config.TIMESTEP
DEFAULT_TURBULENCE_INTENSITY = config.DEFAULT_TURBULENCE_INTENSITY
PARTICLE_SIZE = config.PARTICLE_SIZE


class ParticleSystem:
    def __init__(self):
        # Initialize particle arrays using numpy for better performance
        self.positions = np.random.uniform(-5, 5, (PARTICLE_COUNT, 3))
        self.velocities = np.zeros((PARTICLE_COUNT, 3))
        self.lifetimes = np.ones(PARTICLE_COUNT)
        self.colors = np.ones((PARTICLE_COUNT, 4))
        self.colors[:, 3] = 0.5  # Alpha channel

        # Trail effect - store previous positions
        self.trails = np.zeros((PARTICLE_COUNT, PARTICLE_TRAIL_LENGTH, 3))

        # Initialize generator planes
        self.setup_generator_planes()

    def setup_generator_planes(self):
        # Create particle generation planes around the simulation space
        self.generator_bounds = {
            'x_min': -5.0,
            'x_max': 5.0,
            'y_min': -2.0,
            'y_max': 2.0,
            'z_min': -2.0,
            'z_max': 2.0
        }

    def generate_new_particle(self, index):
        # Randomly choose which plane to generate from
        if random.random() < 0.7:  # 70% chance to generate from front
            x = self.generator_bounds['x_min']
            y = random.uniform(self.generator_bounds['y_min'], self.generator_bounds['y_max'])
            z = random.uniform(self.generator_bounds['z_min'], self.generator_bounds['z_max'])
        else:  # Generate from top or sides
            x = random.uniform(self.generator_bounds['x_min'], self.generator_bounds['x_max'])
            if random.random() < 0.5:
                y = self.generator_bounds['y_max']
                z = random.uniform(self.generator_bounds['z_min'], self.generator_bounds['z_max'])
            else:
                y = random.uniform(self.generator_bounds['y_min'], self.generator_bounds['y_max'])
                z = self.generator_bounds['z_max'] if random.random() < 0.5 else self.generator_bounds['z_min']

        self.positions[index] = [x, y, z]
        self.velocities[index] = [0, 0, 0]
        self.lifetimes[index] = 1.0
        self.trails[index] = np.tile(self.positions[index], (PARTICLE_TRAIL_LENGTH, 1))

    def apply_forces(self, wind_speed, air_density, car):
        # Update velocities based on wind and other forces
        time_step = TIMESTEP

        # Base wind velocity (mainly in x direction)
        wind_velocity = np.array([wind_speed, 0, 0])

        # Update each particle
        for i in range(PARTICLE_COUNT):
            pos = self.positions[i]

            # Skip dead particles
            if self.lifetimes[i] <= 0:
                self.generate_new_particle(i)
                continue

            # Check for collision with car
            if car.is_point_inside(pos):
                normal = car.get_surface_normal(pos)
                # Reflect velocity with some energy loss
                vel = self.velocities[i]
                reflection = vel - 2 * np.dot(vel, normal) * normal
                self.velocities[i] = reflection * 0.8  # 20% energy loss
                # Move particle slightly away from surface
                self.positions[i] = pos + normal * 0.1
                continue

            # Apply wind force
            rel_velocity = wind_velocity - self.velocities[i]
            drag_force = 0.5 * air_density * np.linalg.norm(rel_velocity) * rel_velocity

            # Add some turbulence
            turbulence = np.random.normal(0, DEFAULT_TURBULENCE_INTENSITY, 3)

            # Update velocity using forces
            acceleration = (drag_force + turbulence) / air_density
            self.velocities[i] += acceleration * time_step

            # Update position
            self.positions[i] += self.velocities[i] * time_step

            # Update trails
            self.trails[i, :-1] = self.trails[i, 1:]
            self.trails[i, -1] = self.positions[i]

            # Update lifetime
            self.lifetimes[i] -= 0.01

            # Check bounds
            if any(abs(pos) > 10):  # If particle is too far away
                self.generate_new_particle(i)

    def update(self, wind_speed, air_density, car):
        self.apply_forces(wind_speed, air_density, car)

    def render(self):
        glDisable(GL_LIGHTING)
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Draw particles
        glPointSize(PARTICLE_SIZE)
        glBegin(GL_POINTS)
        for i in range(PARTICLE_COUNT):
            if self.lifetimes[i] > 0:
                # Color varies with velocity
                speed = np.linalg.norm(self.velocities[i])
                color = np.array([0.2, 0.6, 1.0]) * min(1.0, speed/30.0)
                glColor4f(*color, self.lifetimes[i] * 0.5)
                glVertex3f(*self.positions[i])
        glEnd()

        # Draw trails
        glBegin(GL_LINES)
        for i in range(PARTICLE_COUNT):
            if self.lifetimes[i] > 0:
                for j in range(PARTICLE_TRAIL_LENGTH-1):
                    alpha = (j/PARTICLE_TRAIL_LENGTH) * self.lifetimes[i] * 0.3
                    glColor4f(0.2, 0.6, 1.0, alpha)
                    glVertex3f(*self.trails[i,j])
                    glVertex3f(*self.trails[i,j+1])
        glEnd()

        glEnable(GL_LIGHTING)
C:\mygit\BLazy\repo\3dsim\main.py
Language detected: python
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import sys

# Assume car_geometry.py, particle_system.py, and config.py are in the same directory
# If not, you will need to adjust the import paths accordingly.
try:
    from car_geometry import CarGeometry
    from particle_system import ParticleSystem
    from config import *
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure that car_geometry.py, particle_system.py, and config.py are in the same directory as this script, or update the import paths.")
    sys.exit()

class AirflowSimulation:
    def __init__(self):
        # Initialize Pygame and OpenGL
        pygame.init()
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
        pygame.display.set_caption(WINDOW_TITLE)

        # Set up OpenGL
        self.setup_gl()

        # Initialize simulation components
        self.car = CarGeometry()
        self.particles = ParticleSystem()

        # Simulation parameters
        self.wind_speed = DEFAULT_WIND_SPEED
        self.air_density = AIR_DENSITY

        # Camera parameters
        self.camera_rotation = [0, 0, 0]
        self.camera_distance = CAMERA_DISTANCE

        # UI state
        self.paused = False
        self.show_help = False
        self.clock = pygame.time.Clock()

    def setup_gl(self):
        # Set up perspective
        glMatrixMode(GL_PROJECTION)
        gluPerspective(CAMERA_FOV, WINDOW_WIDTH/WINDOW_HEIGHT, CAMERA_NEAR, CAMERA_FAR)

        # Set up lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, LIGHT_POSITION)
        glLightfv(GL_LIGHT0, GL_AMBIENT, AMBIENT_LIGHT)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, DIFFUSE_LIGHT)
        glLightfv(GL_LIGHT0, GL_SPECULAR, SPECULAR_LIGHT)

        # Enable depth testing and smooth shading
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        # Set up blending for particles
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_h:
                    self.show_help = not self.show_help
                elif event.key == pygame.K_UP:
                    self.wind_speed += WIND_SPEED_INCREMENT
                elif event.key == pygame.K_DOWN:
                    self.wind_speed = max(0, self.wind_speed - WIND_SPEED_INCREMENT)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Mouse wheel up
                    self.camera_distance = max(5, self.camera_distance - ZOOM_SPEED)
                elif event.button == 5:  # Mouse wheel down
                    self.camera_distance = min(20, self.camera_distance + ZOOM_SPEED)

        # Handle continuous mouse movement for camera rotation
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            rel_x, rel_y = pygame.mouse.get_rel()
            self.camera_rotation[1] += rel_x * ROTATION_SPEED
            self.camera_rotation[0] = min(max(-45, self.camera_rotation[0] - rel_y * ROTATION_SPEED), 45)
        else:
            pygame.mouse.get_rel()  # Clear relative movement

    def update(self):
        if not self.paused:
            self.particles.update(self.wind_speed, self.air_density, self.car)

    def render(self):
        # Clear the screen and depth buffer
        glClearColor(*BACKGROUND_COLOR)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Set up camera
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -self.camera_distance)
        glRotatef(self.camera_rotation[0], 1, 0, 0)
        glRotatef(self.camera_rotation[1], 0, 1, 0)

        # Draw coordinate grid
        self.draw_grid()

        # Draw car
        self.car.render()

        # Draw particles
        self.particles.render()

        # Draw UI
        self.render_ui()

        pygame.display.flip()

    def draw_grid(self):
        glDisable(GL_LIGHTING)
        glBegin(GL_LINES)
        glColor4f(*GRID_COLOR)

        # Draw grid lines
        for i in range(-10, 11, 2):
            glVertex3f(i, 0, -10)
            glVertex3f(i, 0, 10)
            glVertex3f(-10, 0, i)
            glVertex3f(10, 0, i)

        glEnd()
        glEnable(GL_LIGHTING)

    def render_ui(self):
        if not self.show_help:
            return

        # Switch to 2D rendering for UI
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Draw help text
        self.draw_text([
            f"Wind Speed: {self.wind_speed:.1f} m/s",
            "Controls:",
            "  Mouse Left: Rotate camera",
            "  Mouse Wheel: Zoom",
            "  Up/Down: Adjust wind speed",
            "  Space: Pause/Resume",
            "  H: Toggle help",
            "  Esc: Quit"
        ])

        # Restore 3D rendering
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def draw_text(self, lines):
        font = pygame.font.Font(None, UI_FONT_SIZE)
        y = UI_PADDING

        for line in lines:
            text_surface = font.render(line, True, (255, 255, 255))
            text_data = pygame.image.tostring(text_surface, "RGBA", True)
            text_width, text_height = text_surface.get_size()

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            # Draw text background
            glColor4f(*UI_BACKGROUND_COLOR)
            glBegin(GL_QUADS)
            glVertex2f(UI_PADDING - 5, y - 2)
            glVertex2f(UI_PADDING + text_width + 5, y - 2)
            glVertex2f(UI_PADDING + text_width + 5, y + text_height + 2)
            glVertex2f(UI_PADDING - 5, y + text_height + 2)
            glEnd()

            # Draw text
            glRasterPos2f(UI_PADDING, y)
            glDrawPixels(text_width, text_height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

            y += text_height + 5

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.handle_input()
            self.update()
            self.render()

if __name__ == "__main__":
    simulation = AirflowSimulation()
    simulation.run()
