import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
from pyrr import matrix44, Vector3
import TextureLoader
from Camera import Camera
from math import sin, cos


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


def main():
    # initialize glfw
    if not glfw.init():
        return

    w_width, w_height = 1280, 720
    aspect_ratio = w_width / w_height

    window = glfw.create_window(w_width, w_height, "My OpenGL window", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)

    #        positions        texture_coords
    cube = [-0.5, -0.5, 0.5, 0.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            -0.5, 0.5, -0.5, 0.0, 1.0,

            0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            0.5, -0.5, 0.5, 0.0, 1.0,

            -0.5, 0.5, -0.5, 0.0, 0.0,
            -0.5, -0.5, -0.5, 1.0, 0.0,
            -0.5, -0.5, 0.5, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 1.0,
            -0.5, -0.5, 0.5, 0.0, 1.0,

            0.5, 0.5, -0.5, 0.0, 0.0,
            -0.5, 0.5, -0.5, 1.0, 0.0,
            -0.5, 0.5, 0.5, 1.0, 1.0,
            0.5, 0.5, 0.5, 0.0, 1.0]

    cube = numpy.array(cube, dtype=numpy.float32)

    indices = [0, 1, 2, 2, 3, 0,
               4, 5, 6, 6, 7, 4,
               8, 9, 10, 10, 11, 8,
               12, 13, 14, 14, 15, 12,
               16, 17, 18, 18, 19, 16,
               20, 21, 22, 22, 23, 20]

    indices = numpy.array(indices, dtype=numpy.uint32)

    vertex_shader = """
    #version 330
    in layout(location = 0) vec3 position;
    in layout(location = 1) vec2 texture_cords;
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 proj;
    out vec2 textures;
    void main()
    {
        gl_Position =  proj * view * model * vec4(position, 1.0f);
        textures = texture_cords;
    }
    """

    fragment_shader = """
    #version 330
    in vec2 textures;
    out vec4 color;
    uniform sampler2D tex_sampler;
    void main()
    {
        color = texture(tex_sampler, textures);
    }
    """
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, cube.itemsize * len(cube), cube, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)

    # position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube.itemsize * 5, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # textures
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube.itemsize * 5, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    crate = TextureLoader.load_texture("resources/images/planks_brown_10_diff_1k.jpg")
    metal = TextureLoader.load_texture("resources/images/green_metal_rust_diff_1k.jpg")
    brick = TextureLoader.load_texture("resources/images/castle_brick_07_diff_1k.jpg")

    glUseProgram(shader)

    glClearColor(0.2, 0.3, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)

    projection = matrix44.create_perspective_projection_matrix(45.0, aspect_ratio, 0.1, 100.0)

    model_loc = glGetUniformLocation(shader, "model")
    view_loc = glGetUniformLocation(shader, "view")
    proj_loc = glGetUniformLocation(shader, "proj")

    cube_positions = [(0.0, 0.0, 0.0), (2.0, 2.0, -5.0), (1.5, -1.2, -2.5), (8.8, -2.0, -12.3), (-2.0, 2.0, -5.5),
                      (-4.0, 2.0, -3.0)]

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

    cam = Camera()

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        camX = sin(glfw.get_time()) * 10
        camZ = cos(glfw.get_time()) * 10

        view = cam.look_at(Vector3([camX, 5.0, camZ]), Vector3([0.0, 0.0, 0.0]), Vector3([0.0, 1.0, 0.0]))
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

        for i in range(len(cube_positions)):
            model = matrix44.create_from_translation(cube_positions[i])
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
            if i < 2:
                glBindTexture(GL_TEXTURE_2D, crate)
            elif i == 2 or i == 3:
                glBindTexture(GL_TEXTURE_2D, metal)
            else:
                glBindTexture(GL_TEXTURE_2D, brick)

            glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()