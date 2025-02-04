C:\mygit\BLazy\repo\3dsim\main.py
Language detected: python
import pygame
import moderngl
import numpy as np
import scipy
import pyrr
import os
import json
import math
from typing import Tuple

class SimulationParameters:
    def __init__(self):
        self.velocity = 50.0  # m/s
        self.air_density = 1.225  # kg/m3
        self.yaw_angle = 0.0  # degrees
        self.turbulence_intensity = 0.1

class Camera:
    def __init__(self, window_size: Tuple[int, int]):
        self.position = pyrr.Vector3([0.0, 2.0, 5.0])
        self.front = pyrr.Vector3([0.0, 0.0, -1.0])
        self.up = pyrr.Vector3([0.0, 1.0, 0.0])
        self.right = pyrr.Vector3([1.0, 0.0, 0.0])
        self.fov = 60.0
        self.aspect_ratio = window_size[0] / window_size[1]
        self.near = 0.1
        self.far = 100.0
        self.sensitivity = 0.1
        self.yaw = -90.0
        self.pitch = 0.0

    def get_view_matrix(self):
        return pyrr.matrix44.create_look_at(
            self.position,
            self.position + self.front,
            self.up
        )

    def get_projection_matrix(self):
        return pyrr.matrix44.create_perspective_projection(
            self.fov, self.aspect_ratio, self.near, self.far
        )

class ShaderProgram:
    def __init__(self, ctx, vert_path, frag_path):
        self.ctx = ctx
        self.program = self.load_shaders(vert_path, frag_path)

    def load_shaders(self, vert_path, frag_path):
        with open(vert_path) as f:
            vertex_shader = f.read()
        with open(frag_path) as f:
            fragment_shader = f.read()
        return self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )

class UI:
    def __init__(self, screen, params):
        self.screen = screen
        self.params = params
        self.font = pygame.font.Font(None, 24)
        self.sliders = []
        self.init_ui_elements()

    class Slider:
        def __init__(self, x, y, w, h, min_val, max_val, initial):
            self.rect = pygame.Rect(x, y, w, h)
            self.handle_rect = pygame.Rect(x, y, 10, h)
            self.min = min_val
            self.max = max_val
            self.value = initial
            self.dragging = False

    def init_ui_elements(self):
        # Velocity slider
        self.sliders.append(self.Slider(20, 40, 200, 20, 0, 100, self.params.velocity))

    def draw(self):
        # Draw sliders
        for slider in self.sliders:
            pygame.draw.rect(self.screen, (200, 200, 200), slider.rect)
            pygame.draw.rect(self.screen, (100, 100, 200), slider.handle_rect)
            
        # Draw labels
        label = self.font.render(f"Velocity: {self.params.velocity:.1f} m/s", True, (255, 255, 255))
        self.screen.blit(label, (20, 20))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for slider in self.sliders:
                if slider.handle_rect.collidepoint(event.pos):
                    slider.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            for slider in self.sliders:
                slider.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            for slider in self.sliders:
                if slider.dragging:
                    slider.handle_rect.x = max(
                        slider.rect.left, 
                        min(event.pos[0], slider.rect.right - slider.handle_rect.width)
                    )
                    ratio = (slider.handle_rect.x - slider.rect.left) / slider.rect.width
                    slider.value = slider.min + (slider.max - slider.min) * ratio
                    self.params.velocity = slider.value

class MainApp:
    def __init__(self):
        pygame.init()
        self.window_size = (1280, 720)
        self.screen = pygame.display.set_mode(self.window_size, pygame.DOUBLEBUF | pygame.OPENGL)
        self.ctx = moderngl.create_context()
        
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.BLEND)
        self.clock = pygame.time.Clock()
        
        self.camera = Camera(self.window_size)
        self.params = SimulationParameters()
        self.ui = UI(pygame.display.get_surface(), self.params)
        
        self.shader_program = ShaderProgram(self.ctx, "shaders/vert.glsl", "shaders/frag.glsl")
        
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEMOTION:
                dx, dy = event.rel
                self.camera.yaw += dx * self.camera.sensitivity
                self.camera.pitch -= dy * self.camera.sensitivity
                self.camera.pitch = max(-89, min(89, self.camera.pitch))
                
                front = pyrr.Vector3()
                front.x = math.cos(math.radians(self.camera.yaw)) * math.cos(math.radians(self.camera.pitch))
                front.y = math.sin(math.radians(self.camera.pitch))
                front.z = math.sin(math.radians(self.camera.yaw)) * math.cos(math.radians(self.camera.pitch))
                self.camera.front = front.normalized
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.ui.handle_event(event)
                
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                quit()

    def run(self):
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        
        while True:
            self.clock.tick(60)
            self.handle_input()
            
            # Clear buffers
            self.ctx.clear(0.1, 0.1, 0.1)
            self.ctx.viewport = (0, 0, self.window_size[0], self.window_size[1])
            
            # Update UI
            self.screen.fill((0, 0, 0, 0))
            self.ui.draw()
            pygame.display.flip()

if __name__ == "__main__":
    app = MainApp()
    app.run()
C:\mygit\BLazy\repo\3dsim\shaders\vertex_shader.glsl
Language detected: glsl
#version 330 core

// Input vertex attributes
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;

// Uniform matrices for transformation
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// Output variables to fragment shader
out vec3 Color;
out vec3 WorldPos;

void main()
{
    // Calculate world position for airflow visualization
    vec4 worldPosition = model * vec4(aPos, 1.0);
    WorldPos = worldPosition.xyz;
    
    // Final position calculation for vertex transformation
    gl_Position = projection * view * worldPosition;
    
    // Pass color data to fragment shader
    Color = aColor;
}
C:\mygit\BLazy\repo\3dsim\shaders\fragment_shader.glsl
Language detected: glsl
#version 330 core

// Inputs from vertex shader
in vec3 FragPos;
in vec3 Normal;
in vec3 ParticleVelocity;
in float ParticlePressure;

// Uniform variables
uniform vec3 uAmbientColor;
uniform vec3 uDiffuseColor;
uniform vec3 uSpecularColor;
uniform vec3 uLightColor;
uniform vec3 uLightPos;
uniform vec3 uViewPos;

uniform vec3 uLowVelColor;
uniform vec3 uHighVelColor;
uniform vec3 uLowPressureColor;
uniform vec3 uHighPressureColor;
uniform float uVelocityScale;
uniform float uPressureScale;
uniform sampler2D uNoiseTex;
uniform float uTime;
uniform float uAlphaTransparency;

// Fragment color output
out vec4 FragColor;

void main()
{
    // Normalize inputs
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(uLightPos - FragPos);
    vec3 viewDir = normalize(uViewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);

    // Phong lighting components
    float diff = max(dot(norm, lightDir), 0.0);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);
    
    vec3 ambient = uAmbientColor * uLightColor;
    vec3 diffuse = diff * uDiffuseColor * uLightColor;
    vec3 specular = spec * uSpecularColor * uLightColor;
    vec3 lighting = ambient + diffuse + specular;

    // Velocity-based color mapping
    float velocityMagnitude = length(ParticleVelocity) * uVelocityScale;
    vec3 velColor = mix(uLowVelColor, uHighVelColor, velocityMagnitude);

    // Pressure-based color mapping
    float pressure = ParticlePressure * uPressureScale;
    vec3 pressColor = mix(uLowPressureColor, uHighPressureColor, pressure);

    // Combine flow visualization colors
    vec3 flowColor = mix(velColor, pressColor, 0.5);

    // Particle effect with animated noise
    vec2 noiseCoords = FragPos.xy * 0.1 + vec2(sin(uTime * 0.5), cos(uTime * 0.5));
    float noiseValue = texture(uNoiseTex, noiseCoords).r;
    flowColor += vec3(noiseValue * 0.3); // Add noise-based particle highlights

    // Final color with lighting
    vec3 finalColor = flowColor * lighting;

    // Dynamic transparency based on flow properties
    float alpha = clamp((velocityMagnitude + pressure) * uAlphaTransparency, 0.1, 0.9);

    FragColor = vec4(finalColor, alpha);
}
