from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *


# install Pilllow package, then you can use PIL
from PIL import Image
import numpy as np

class Background :
    def __init__(self):
        self.img = None
        self.img_data = None
        self.tex = 0

    def loadImage(self, filename):
        self.img = Image.open(filename)
        self.img_data = np.array(list(self.img.getdata()), np.uint8)

        self.tex = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.tex)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.img.size[0], self.img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, self.img_data)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)



    def draw(self):
        if self.img is None :
            return

        glEnable(GL_TEXTURE_2D)
        glDisable(GL_LIGHTING)
        glColor3f(1,1,1)
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glBegin(GL_QUADS)
        glTexCoord2fv([0, 1])
        glVertex2fv([-1, -1])
        glTexCoord2fv([1, 1])
        glVertex2fv([1, -1])
        glTexCoord2fv([1, 0])
        glVertex2fv([1, 1])
        glTexCoord2fv([0, 0])
        glVertex2fv([-1, 1])
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)
