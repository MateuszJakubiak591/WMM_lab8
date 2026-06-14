#version 330

uniform vec3 color;

out vec4 f_color;

void main()
{
    // A uniform gives every fragment of a robot part the same colour.
    f_color = vec4(color, 1.0);
}
