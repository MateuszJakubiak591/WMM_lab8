import moderngl_window

from robot_window import RobotWindow


if __name__ == "__main__":
    moderngl_window.run_window_config(
        RobotWindow,
        args=[
            "--shaders_dir_path=./resources/shaders/robot",
            "--shader_name=robot",
        ],
    )
