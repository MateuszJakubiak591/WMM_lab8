#version 330

in vec3 v_position;
in vec3 v_normal;

uniform vec3 light_position;
uniform vec3 light_ambient;
uniform vec3 light_diffuse;
uniform vec3 light_specular;
uniform vec3 material_ambient;
uniform vec3 material_diffuse;
uniform vec3 material_specular;
uniform float material_shininess;
uniform vec3 camera_position;

out vec4 f_color;

void main()
{
    vec3 N = normalize(v_normal);
    // L and V are combined into the Blinn-Phong halfway vector.
    vec3 L = normalize(light_position - v_position);
    vec3 V = normalize(camera_position - v_position);
    vec3 H = normalize(L + V);

    float cosNL = max(dot(N, L), 0.0);
    vec3 ambient = light_ambient * material_ambient;
    vec3 diffuse = light_diffuse * material_diffuse * cosNL;

    // Blinn-Phong compares the normal with the halfway vector.
    float specular_factor = cosNL > 0.0
        ? pow(max(dot(N, H), 0.0), material_shininess)
        : 0.0;
    vec3 specular = light_specular * material_specular * specular_factor;

    vec3 phong_color = clamp(ambient + diffuse + specular, 0.0, 1.0);
    f_color = vec4(phong_color, 1.0);
}
