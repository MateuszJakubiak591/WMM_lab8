from math import cos, sin

import moderngl
from pyrr import Matrix44, Vector3

from base_window import BaseWindow
from robot_scene import create_robot_parts, load_robot_models

class BlinnPhongWindow(BaseWindow):

    def __init__(self, **kwargs):
        super(BlinnPhongWindow, self).__init__(**kwargs)

    def load_models(self):
        self.models = load_robot_models(self.program)

    def init_shaders_variables(self):
        self.projection_uniform = self.program["projection"]
        self.view_uniform = self.program["view"]
        self.model_uniform = self.program["model"]
        self.light_position_uniform = self.program["light_position"]
        self.material_diffuse_uniform = self.program["material_diffuse"]

        self.program["light_ambient"].value = (0.2, 0.2, 0.2)
        self.program["light_diffuse"].value = (0.8, 0.8, 0.8)
        self.program["light_specular"].value = (1.0, 1.0, 1.0)
        self.program["material_ambient"].value = (0.25, 0.25, 0.25)
        self.program["material_specular"].value = (1.0, 1.0, 1.0)
        self.program["material_shininess"].value = 50.0
        self.program["camera_position"].value = (-3.0, 5.0, 15.0)

    def on_render(self, time: float, frame_time: float):
        self.ctx.clear(0.1, 0.2, 0.3, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        projection = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        view = Matrix44.look_at(
            (-3.0, 5.0, 15.0),
            (0.0, 1.0, 0.0),
            (0.0, 1.0, 0.0),
        )

        self.projection_uniform.write(projection.astype("f4"))
        self.view_uniform.write(view.astype("f4"))

        # Use the same moving light as in PhongWindow for a fair comparison.
        self.light_position_uniform.value = (8.0 * sin(time), 8.0, 8.0 * cos(time))

        for part in create_robot_parts():
            self.model_uniform.write(part.model_matrix.astype("f4"))
            self.material_diffuse_uniform.value = part.color
            self.models[part.model_name].render(moderngl.TRIANGLES)
