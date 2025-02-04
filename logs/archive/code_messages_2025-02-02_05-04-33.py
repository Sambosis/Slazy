C:\mygit\BLazy\repo\3dsim\shaders\vertex_shader.glsl
Language detected: glsl
#version 330 core

// Input variables
layout(location = 0) in vec3 a_Position; // Particle position
layout(location = 1) in vec3 a_Velocity; // Particle velocity
layout(location = 2) in vec4 a_Color;    // Particle color

// Uniform variables
uniform mat4 u_ModelMatrix;              // Model matrix
uniform mat4 u_ViewMatrix;               // View matrix
uniform mat4 u_ProjectionMatrix;         // Projection matrix
uniform float u_Time;                    // Time variable

// Output variables passed to the fragment shader
out vec3 v_Velocity;
out vec4 v_Color;

void main()
{
    // Calculate the final world position
    vec4 worldPosition = u_ModelMatrix * vec4(a_Position, 1.0);
    
    // Apply velocity over time
    worldPosition.xyz += a_Velocity * u_Time;
   
    // Transform to view and projection
    gl_Position = u_ProjectionMatrix * u_ViewMatrix * worldPosition;

    // Pass velocity and color to the fragment shader
    v_Velocity = a_Velocity;
    v_Color = a_Color;
}
