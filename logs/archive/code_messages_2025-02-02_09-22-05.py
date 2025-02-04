C:\mygit\BLazy\repo\3dsim\main.py
Language detected: python
# Required Libraries
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
import numpy as np
import pyvista as pv
from pyvista import qt_widgets

# Main Window Class
class CarCFDSimulation(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Car CFD Simulation")
        self.setGeometry(100, 100, 800, 600)
        
        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
 
        # 3D Visualization
        self.plotter = pvqt.QVTKRenderWindowInteractor(self)
        self.layout.addWidget(self.plotter)
        self.ren_win = self.plotter.interactor
        self.mesh = None
        
        # Sliders and Input Fields
        layout_controls = QVBoxLayout()
        self.layout.addLayout(layout_controls)
        
        self.length_slider = QSlider(Qt.Horizontal)
        self.width_slider = QSlider(Qt.Horizontal)
        self.height_slider = QSlider(Qt.Horizontal)
        self.angle_slider = QSlider(Qt.Horizontal)
        
        self.length_slider.setMinimum(1)
        self.length_slider.setMaximum(10)
        self.width_slider.setMinimum(1)
        self.width_slider.setMaximum(10)
        self.height_slider.setMinimum(1)
        self.height_slider.setMaximum(10)
        self.angle_slider.setMinimum(-30)
        self.angle_slider.setMaximum(30)
        
        layout_controls.addWidget(QLineEdit("Length"))
        layout_controls.addWidget(self.length_slider)
        layout_controls.addWidget(QLineEdit("Width"))
        layout_controls.addWidget(self.width_slider)
        layout_controls.addWidget(QLineEdit("Height"))
        layout_controls.addWidget(self.height_slider)
        layout_controls.addWidget(QLineEdit("Angle"))
        layout_controls.addWidget(self.angle_slider)
        
        # Control Buttons
        self.start_button = QPushButton('Start')
        self.stop_button = QPushButton('Stop')
        
        layout_controls.addWidget(self.start_button)
        layout_controls.addWidget(self.stop_button)

# Method Implementation
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    mainWindow = CarCFDSimulation()
    mainWindow.show()

    sys.exit(app.exec_())
C:\mygit\BLazy\repo\3dsim\car_geometry.py
Language detected: python
# CarGeometry.py

# Required Libraries
import pyvista as pv
import numpy as np

class CarGeometry:
    def __init__(self, length=4.5, width=1.8, height=1.5, angle=0):
        self.length = length
        self.width = width
        self.height = height
        self.angle = angle
        self.car_mesh = None
        self.domain = None

    def create_car_shape(self):
        """
        Creates a simple box mesh representing the car.
        """
        x_len = self.length / 2
        y_len = self.width / 2
        z_len = self.height / 2
        mesh = pv.Cube(center=(0, 0, 0), x_length=x_len, y_length=y_len, z_length=z_len)
        self.car_mesh = mesh.triangulate()

    def generate_computational_domain(self, domain_size=(20, 5, 5)):
        """
        Creates a larger box representing the computational domain around the car.
        """
        x_dom, y_dom, z_dom = domain_size
        domain = pv.Box(bounds=(-x_dom/2, x_dom/2, -y_dom/2, y_dom/2, -z_dom/2, z_dom/2))
        self.domain = domain

    def refine_mesh_around_car(self, resolution=0.1):
        """
        Refines the mesh around the car for higher resolution.
        """
        if self.car_mesh:
            refined_mesh = self.car_mesh.extract_surface().subdivide_adaptive(
                criteria='quadric_error', max_err=resolution, max_iter=2
            )
            self.car_mesh = refined_mesh

    def update_car_orientation(self):
        """
        Updates the orientation of the car based on predefined angle.
        """
        if self.car_mesh:
            axis = np.array([0, 1, 0])  # Rotate around y-axis
            center = self.car_mesh.center
            transform = pv.rotate_points(self.car_mesh.points, angle=self.angle, axis=axis, point=center)
            self.car_mesh.points = transform
            self.car_mesh.point_data.update()

    def get_car_mesh(self):
        """
        Returns the current car mesh.
        """
        return self.car_mesh.copy()

    def get_domain(self):
        """
        Returns the computational domain.
        """
        return self.domain.copy()

# Example usage (can be removed or kept for testing during development)
if __name__ == '__main__':
    car_geo = CarGeometry(length=5, width=2, height=1.8, angle=15)
    car_geo.create_car_shape()
    car_geo.refine_mesh_around_car(resolution=0.05)
    car_geo.update_car_orientation()
    car_mesh = car_geo.get_car_mesh()
    domain = car_geo.get_domain()
    
    p = pv.Plotter()
    p.add_mesh(car_mesh, color='silver')
    p.add_mesh(domain, color='white', opacity=0.2)
    p.show()
C:\mygit\BLazy\repo\3dsim\cfd_solver.py
Language detected: python
# filepath: C:\mygit\BLazy\repo\3dsim\cfdsolver.py

# Required Libraries
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

class CFDSolver:
    def __init__(self, nx=64, ny=64, ns=50, dx=0.1, dy=0.1, dt=0.01, nu=0.1):
        """
        Initialize the CFD solver with grid parameters.
        
        Parameters:
            nx : int
                Number of grid points in the x direction.
            ny : int
                Number of grid points in the y direction.
            ns : int
                Number of simulation steps.
            dx : float
                Grid spacing along the x direction.
            dy : float
                Grid spacing along the y direction.
            dt : float
                Time step.
            nu : float
                Kinematic viscosity.
        """
        self.nx = nx
        self.ny = ny
        self.ns = ns
        self.dx = dx
        self.dy = dy
        self.dt = dt
        self.nu = nu
        self.u = np.zeros((ny, nx))
        self.v = np.zeros((ny, nx))
        self.p = np.zeros((ny, nx))

    def initialize_flow_field(self):
        """
        Initialize flow field with zero velocity and pressure.
        """
        self.u = np.zeros((self.ny, self.nx))
        self.v = np.zeros((self.ny, self.nx))
        self.p = np.zeros((self.ny, self.nx))

    def diffuse(self, u, v):
        """
        Diffuse velocity field using the diffusion term of the Navier-Stokes equation.

        Parameters:
            u : array
                Velocity field in the x direction.
            v : array
                Velocity field in the y direction.
        """
        un = u.copy()
        vn = v.copy()
        
        u[1:-1, 1:-1] = (
            un[1:-1, 1:-1]
            + self.dt * self.nu * (
                (un[1:-1, 2:] - 2*un[1:-1, 1:-1] + un[1:-1, 0:-2]) / self.dx**2
                + (un[2:, 1:-1] - 2*un[1:-1, 1:-1] + un[0:-2, 1:-1]) / self.dy**2
            )
        )
        
        v[1:-1, 1:-1] = (
            vn[1:-1, 1:-1]
            + self.dt * self.nu * (
                (vn[1:-1, 2:] - 2*vn[1:-1, 1:-1] + vn[1:-1, 0:-2]) / self.dx**2
                + (vn[2:, 1:-1] - 2*vn[1:-1, 1:-1] + vn[0:-2, 1:-1]) / self.dy**2
            )
        )

    def convection(self, u, v):
        """
        Convection step using the convection term of the Navier-Stokes equation.

        Parameters:
            u : array
                Velocity field in the x direction.
            v : array
                Velocity field in the y direction.
        """
        un = u.copy()
        vn = v.copy()

        u[1:-1, 1:-1] = (
            un[1:-1, 1:-1]
            - un[1:-1, 1:-1] * self.dt * ((un[1:-1, 1:-1] - un[1:-1, 0:-2]) / self.dx)
            - vn[1:-1, 1:-1] * self.dt * ((un[1:-1, 1:-1] - un[0:-2, 1:-1]) / self.dy)
        )
        
        v[1:-1, 1:-1] = (
            vn[1:-1, 1:-1]
            - un[1:-1, 1:-1] * self.dt * ((vn[1:-1, 1:-1] - vn[1:-1, 0:-2]) / self.dx)
            - vn[1:-1, 1:-1] * self.dt * ((vn[1:-1, 1:-1] - vn[0:-2, 1:-1]) / self.dy)
        )

    def solve_pressure_poisson(self):
        """
        Solve the Poisson equation for pressure.
        
        Update pressure field p.
        """
        b = np.zeros((self.ny, self.nx))
        b[1:-1, 1:-1] = self.dt * (
            (self.u[1:-1, 2:] - self.u[1:-1, 0:-2]) / (2 * self.dx)
            + (self.v[2:, 1:-1] - self.v[0:-2, 1:-1]) / (2 * self.dy)
        )

        # Solver for the pressure equation
        A = diags([-1/(self.dx * self.dx) - 1/(self.dy * self.dy)] * self.ny,
                  [0],
                  shape=(self.ny, self.ny)).toarray()
        for i in range(self.nx-2):
            A[i+1, i] = 1 / (self.dx * self.dx)
            A[i+1, i+2] = 1 / (self.dy * self.dy)
        A[-3, -1] = 0
        A[1, 1] = -(1 / (self.dx * self.dx) + 1 / (self.dy * self.dy)) + 1

        b[-2] = 0  # Top boundary
        b[0] = 0   # Bottom boundary
        p = spsolve(A, b.flatten())
        self.p = p.reshape(self.ny, self.nx)
  
    def compute_flow_variables(self):
        """
        Perform one time step of the flow computation.
        
        Includes diffusion, convection, and solving pressure Poisson equation.
        """
        self.diffuse(self.u, self.v)
        self.convection(self.u, self.v)
        self.solve_pressure_poisson()

    def update_simulation_state(self):
        """
        Update the simulation state by computing multiple flow variables.
        
        Updates self.u, self.v, and self.p.
        """
        for _ in range(self.ns):
            self.compute_flow_variables()
  
    def generate_streamlines(self, seed_points=None):
        """
        Generate streamlines based on the computed velocity fields.
        
        Parameters:
            seed_points : list or None
                List of seed points for streamline generation.
        """
        if seed_points is None:
            seed_points = []  # Default seed points

        streamline = Streamlines(self.u, self.v, seed_points)
        return streamline

class Streamlines:
    def __init__(self, u, v, seed_points=None):
        self.u = u
        self.v = v
        self.seed_points = seed_points if seed_points is not None else []

    def plot_streamlines(self, pl):
        """
        Plot streamlines using PyVista.
        
        Parameters:
            pl : pyvista.Plotter
                Instance of PyVista Plotter.
        """
        for point in self.seed_points:
            x, y = point
            pl.streamlines(u=self.u, v=self.v, point=(x, y, 0))
