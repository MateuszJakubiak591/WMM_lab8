#version 330

in vec3 in_position;
in vec3 in_normal;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

out vec3 v_position;
out vec3 v_normal;

void main()
{
    // Pass world-space position and a normal corrected for non-uniform scaling.
    v_position = (model * vec4(in_position, 1.0)).xyz;
    v_normal = mat3(transpose(inverse(model))) * in_normal;

    gl_Position = projection * view * model * vec4(in_position, 1.0);
}
