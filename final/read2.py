import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from ObjectLoader import Mesh
from PIL import Image
import numpy as np



vertex_src = open("../shaders/vertex.txt")
fragment_src = open("../shaders/fragment.txt")

# glfw callback functions
def window_resize(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(35, width / height, 50, 1000)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

if not glfw.init():
    raise Exception("glfw can not be initialized!")

window = glfw.create_window(1280, 720, "4K building Models", None, None)
if not window:
    glfw.terminate()

glfw.set_window_pos(window, 500, 200)

# set the callback function for window resize
glfw.set_window_size_callback(window, window_resize)

# make the context current
glfw.make_context_current(window)

# load here the 3d meshes
# freshman_indices, freshman_buffer = Mesh.load_model("freshman_final.obj")
museum_indices, museum_buffer = Mesh.load_model("fourth.obj")

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)


# museum VAO
glBindVertexArray(VAO)
# museum Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, museum_buffer.nbytes, museum_buffer, GL_STATIC_DRAW)

# # museum vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, museum_buffer.itemsize * 8, ctypes.c_void_p(0))
# museum textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, museum_buffer.itemsize * 8, ctypes.c_void_p(12))
# museum normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, museum_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)


textures = glGenTextures(1)


glBindTexture(GL_TEXTURE_2D, textures)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

image = Image.open("one.png")
image = image.transpose(Image.FLIP_TOP_BOTTOM)
img_data = image.convert("RGBA").tobytes()
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(80, 1280 / 720, 0.1,1000)
museum_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -5, -100]))

view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 100, 1000]), pyrr.Vector3([100, 0, 0]), pyrr.Vector3([0, 4, 0]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

# the main application loop
while glfw.window_should_close(window) == False:
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_y = pyrr.Matrix44.from_y_rotation(0.2 * glfw.get_time())
    model2 = pyrr.matrix44.multiply(rot_y, museum_pos)

    # draw the museum
    glBindVertexArray(VAO)
    glBindTexture(GL_TEXTURE_2D, textures)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model2)
    glDrawArrays(GL_TRIANGLES, 0, len(museum_indices))
    glfw.swap_buffers(window)

glfw.terminate()