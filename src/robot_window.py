from math import radians

import moderngl
from pyrr import Matrix44, Vector3

import models
from base_window import BaseWindow


STUDENT_INDEX = 318661
HEAD_COLORS = (
    (1.0, 0.0, 0.0),
    (1.0, 0.5, 0.0),
    (1.0, 1.0, 0.0),
    (0.0, 0.8, 0.2),
    (0.0, 0.8, 1.0),
    (0.0, 0.2, 1.0),
    (0.6, 0.0, 1.0),
    (1.0, 0.0, 0.6),
)


class RobotWindow(BaseWindow):

    def __init__(self, **kwargs):
        super(RobotWindow, self).__init__(**kwargs)

    def load_models(self):
        # Zaladowane sa wszystkie bryly, aby wybor dodatkowego elementu zalezal
        # tylko od wyniku STUDENT_INDEX modulo 3.
        self.models = {
            "cube": models.load_cube(self.program),
            "pyramid": models.load_pyramid(self.program),
            "sphere": models.load_sphere(self.program),
            "torus": models.load_torus(self.program),
        }

    def init_shaders_variables(self):
        # Pobranie lokacji zmiennych uniform uzywanych przez shadery robota.
        self.projection_uniform = self.program["projection"]
        self.view_uniform = self.program["view"]
        self.model_uniform = self.program["model"]
        self.color_uniform = self.program["color"]

    @staticmethod
    def create_model_matrix(translation, scale, z_rotation=0.0):
        """Zloz macierz modelu z translacji, obrotu wokol Z i skalowania."""
        return (
            Matrix44.from_translation(Vector3(translation))
            * Matrix44.from_z_rotation(z_rotation)
            * Matrix44.from_scale(Vector3(scale))
        )

    def create_robot_parts(self):
        """Przygotuj nazwe modelu, macierz i kolor dla kazdej czesci robota."""
        color_id = STUDENT_INDEX % 8
        element_id = STUDENT_INDEX % 3
        head_color = HEAD_COLORS[color_id]
        body_color = (0.15, 0.45, 0.95)
        limb_color = (0.85, 0.85, 0.9)

        parts = [
            ("cube", self.create_model_matrix((0.0, 5.0, 0.0), (1.5, 1.5, 1.5)), head_color),
            ("cube", self.create_model_matrix((0.0, 2.0, 0.0), (2.0, 4.0, 2.0)), body_color),
            ("cube", self.create_model_matrix((-2.5, 4.0, 0.0), (0.75, 2.5, 0.75), radians(45)), limb_color),
            ("cube", self.create_model_matrix((2.5, 4.0, 0.0), (0.75, 2.5, 0.75), radians(-45)), limb_color),
            ("cube", self.create_model_matrix((-2.0, -2.0, 0.0), (1.0, 3.0, 1.0), radians(-30)), limb_color),
            ("cube", self.create_model_matrix((2.0, -2.0, 0.0), (1.0, 3.0, 1.0), radians(30)), limb_color),
        ]

        # Dodatkowa bryla jest wybierana zgodnie z wymaganiem element_id.
        if element_id == 0:
            parts.append(
                ("pyramid", self.create_model_matrix((0.0, 6.75, 0.0), (1.8, 1.5, 1.8)), head_color)
            )
        elif element_id == 1:
            parts.append(
                ("sphere", self.create_model_matrix((3.5, 2.75, 0.0), (1.0, 1.0, 1.0)), head_color)
            )
        else:
            torus_model = (
                Matrix44.from_translation(Vector3((0.0, 1.0, 0.0)))
                * Matrix44.from_x_rotation(radians(90))
                * Matrix44.from_scale(Vector3((3.0, 3.0, 3.0)))
            )
            parts.append(("torus", torus_model, head_color))

        return parts

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

        # Kazda czesc otrzymuje osobna macierz modelu oraz jednolity kolor.
        for model_name, model_matrix, color in self.create_robot_parts():
            self.model_uniform.write(model_matrix.astype("f4"))
            self.color_uniform.value = color
            self.models[model_name].render(moderngl.TRIANGLES)
