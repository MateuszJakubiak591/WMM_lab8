from dataclasses import dataclass
from math import radians, sin

from pyrr import Matrix44, Vector3

import models


STUDENT_INDEX = 318661
COLOR_ID = STUDENT_INDEX % 8
ELEMENT_ID = STUDENT_INDEX % 3

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


@dataclass
class RobotPart:
    model_name: str
    model_matrix: Matrix44
    color: tuple[float, float, float]


def _transform(translation, scale, z_rotation=0.0):
    """Build a model matrix from translation, rotation and scale."""
    return (
        Matrix44.from_translation(Vector3(translation))
        * Matrix44.from_z_rotation(z_rotation)
        * Matrix44.from_scale(Vector3(scale))
    )


def _arm_transform(shoulder, angle):
    """Rotate an arm around its shoulder instead of around the cube centre."""
    return (
        Matrix44.from_translation(Vector3(shoulder))
        * Matrix44.from_z_rotation(angle)
        * Matrix44.from_translation(Vector3((0.0, -1.25, 0.0)))
        * Matrix44.from_scale(Vector3((0.75, 2.5, 0.75)))
    )


def create_robot_parts(animation_time=None):
    """Create all model matrices for one frame of the robot scene."""
    head_color = HEAD_COLORS[COLOR_ID]
    body_color = (0.15, 0.45, 0.95)
    limb_color = (0.85, 0.85, 0.9)

    if animation_time is None:
        left_arm = _transform((-2.5, 4.0, 0.0), (0.75, 2.5, 0.75), radians(45.0))
        right_arm = _transform((2.5, 4.0, 0.0), (0.75, 2.5, 0.75), radians(-45.0))
    else:
        # Harmonic motion: A = 45 degrees, omega = 2.0 rad/s.
        angle = radians(45.0) * sin(2.0 * animation_time)
        left_arm = _arm_transform((-1.4, 4.0, 0.0), angle)
        right_arm = _arm_transform((1.4, 4.0, 0.0), -angle)

    parts = [
        RobotPart("cube", _transform((0.0, 5.0, 0.0), (1.5, 1.5, 1.5)), head_color),
        RobotPart("cube", _transform((0.0, 2.0, 0.0), (2.0, 4.0, 2.0)), body_color),
        RobotPart("cube", left_arm, limb_color),
        RobotPart("cube", right_arm, limb_color),
        RobotPart("cube", _transform((-2.0, -2.0, 0.0), (1.0, 3.0, 1.0), radians(-30.0)), limb_color),
        RobotPart("cube", _transform((2.0, -2.0, 0.0), (1.0, 3.0, 1.0), radians(30.0)), limb_color),
    ]

    # The additional solid is selected using STUDENT_INDEX modulo 3.
    if ELEMENT_ID == 0:
        parts.append(RobotPart("pyramid", _transform((0.0, 6.75, 0.0), (1.8, 1.5, 1.8)), head_color))
    elif ELEMENT_ID == 1:
        # Attach the index-selected sphere to the robot's right hand.
        parts.append(RobotPart("sphere", _transform((3.5, 2.75, 0.0), (1.0, 1.0, 1.0)), head_color))
    else:
        parts.append(
            RobotPart(
                "torus",
                Matrix44.from_translation(Vector3((0.0, 1.0, 0.0)))
                * Matrix44.from_x_rotation(radians(90.0))
                * Matrix44.from_scale(Vector3((3.0, 3.0, 3.0))),
                head_color,
            )
        )

    return parts


def load_robot_models(program):
    """Load every geometry variant so another index can be used without code changes."""
    return {
        "cube": models.load_cube(program),
        "pyramid": models.load_pyramid(program),
        "sphere": models.load_sphere(program),
        "torus": models.load_torus(program),
    }
