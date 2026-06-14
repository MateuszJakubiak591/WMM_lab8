import moderngl
from pyrr import Matrix44, Vector3

from base_window import BaseWindow
from robot_scene import create_robot_parts, load_robot_models

class AnimWindow(BaseWindow):

    def __init__(self, **kwargs):
        super(AnimWindow, self).__init__(**kwargs)

    def load_models(self):
        self.models = load_robot_models(self.program)

    def init_shaders_variables(self):
        self.projection_uniform = self.program["projection"]
        self.view_uniform = self.program["view"]
        self.model_uniform = self.program["model"]
        self.color_uniform = self.program["color"]

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

        # Time changes both shoulder rotations in opposite phases.
        for part in create_robot_parts(animation_time=time):
            self.model_uniform.write(part.model_matrix.astype("f4"))
            self.color_uniform.value = part.color
            self.models[part.model_name].render(moderngl.TRIANGLES)
