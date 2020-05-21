import glfw

# initialize GLFW lib
if not glfw.init():
    raise Exception("GLFW couldn't be initialized!")

# use modern OpenGL
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)

# 4 MSAA is a good default with wide support
glfw.window_hint(glfw.SAMPLES, 4)

# create the window
window = glfw.create_window(1280, 720, "My OpenGL Window", None, None)

# check if window is created
if not window:
    glfw.terminate()
    raise Exception("GLFW window could not be created!")

frame_buffer_size = glfw.get_framebuffer_size(window)

# set window's position
glfw.set_window_pos(window, 400, 200)

# make context current -- whatever that is
glfw.make_context_current(window)   # stores all the data that is related to rendering allowing the program to free
                                    # the resources

# Main application's while loop
while not glfw.window_should_close(window):
    # check for mouse or keyboard input
    glfw.poll_events()

    # draw shit

    # swap buffers to load the recent ones
    glfw.swap_buffers(window)

# terminate glfw and free the resources
glfw.terminate()
