#version 330

in vec3 in_position;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

void main()
{
    // Transform a 3D model vertex into clip space displayed on screen.
    gl_Position = projection * view * model * vec4(in_position, 1.0);
}
