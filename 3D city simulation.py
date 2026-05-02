from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

eyeX, eyeY, eyeZ = 0, 8, 20
lookX, lookY, lookZ = 0, 0, 0

buildings = []
grid = 4

def makeCity():
    global buildings

    for i in range(-20, 20, grid):
        for j in range(-20, 20, grid):
            h = random.uniform(2, 8)
            buildings.append((i + grid/2, h, j + grid/2))

def init():
    glEnable(GL_DEPTH_TEST)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)

    glLightfv(GL_LIGHT0, GL_POSITION, [10, 20, 10, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glEnable(GL_FOG)
    glFogfv(GL_FOG_COLOR, [0.6, 0.6, 0.7, 1])
    glFogf(GL_FOG_MODE, GL_EXP)
    glFogf(GL_FOG_DENSITY, 0.04)

    glClearColor(0.7, 0.8, 1, 1)

    makeCity()

def shadow(x, z):
    glDisable(GL_LIGHTING)

    glColor4f(0, 0, 0, 0.3)

    glPushMatrix()
    glTranslatef(x, 0.03, z)
    glScalef(1.2, 0.01, 1.2)
    glutSolidCube(1)
    glPopMatrix()

    glEnable(GL_LIGHTING)


def windows(h, seedVal):
    random.seed(seedVal)

    floors = int(h * 2)
    cols = 3

    if floors == 0:
        return

    step = h / floors

    for i in range(floors):
        y = -h/2 + i * step + 0.2

        for j in range(cols):
            if random.random() > 0.3:
                glColor4f(1, 0.9, 0.3, 0.7)
            else:
                glColor4f(0.1, 0.1, 0.1, 0.8)

            x = -0.3 + j * 0.3

            glBegin(GL_QUADS)
            glVertex3f(x, y, 0.51)
            glVertex3f(x + 0.15, y, 0.51)
            glVertex3f(x + 0.15, y + 0.15, 0.51)
            glVertex3f(x, y + 0.15, 0.51)
            glEnd()

            glBegin(GL_QUADS)
            glVertex3f(x, y, -0.51)
            glVertex3f(x + 0.15, y, -0.51)
            glVertex3f(x + 0.15, y + 0.15, -0.51)
            glVertex3f(x, y + 0.15, -0.51)
            glEnd()


def drawBuilding(x, h, z):
    shadow(x, z)

    glPushMatrix()
    glTranslatef(x, h/2, z)

    c = h / 8
    glColor4f(0.2 + c, 0.4 + c, 0.9, 0.85)

    glPushMatrix()
    glScalef(1, h, 1)
    glutSolidCube(1)
    glPopMatrix()

    windows(h, x*1000 + z)

    glPopMatrix()


def drawCity():
    for b in buildings:
        drawBuilding(b[0], b[1], b[2])


def roads():
    glDisable(GL_LIGHTING)

    glColor3f(0.1, 0.1, 0.1)

    y = 0.05
    road_half = 0.6

    for x in range(-20, 20, grid):
        for z in range(-20, 20, grid):

            glBegin(GL_QUADS)
            glVertex3f(x - road_half, y, z)
            glVertex3f(x + road_half, y, z)
            glVertex3f(x + road_half, y, z + grid)
            glVertex3f(x - road_half, y, z + grid)
            glEnd()

            glBegin(GL_QUADS)
            glVertex3f(x, y, z - road_half)
            glVertex3f(x + grid, y, z - road_half)
            glVertex3f(x + grid, y, z + road_half)
            glVertex3f(x, y, z + road_half)
            glEnd()

    glEnable(GL_LIGHTING)


def ground():
    glDisable(GL_DEPTH_TEST) 

    glColor3f(0.2, 0.6, 0.2)

    glBegin(GL_QUADS)
    glVertex3f(-50, 0, -50)
    glVertex3f(50, 0, -50)
    glVertex3f(50, 0, 50)
    glVertex3f(-50, 0, 50)
    glEnd()

    glEnable(GL_DEPTH_TEST)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(eyeX, eyeY, eyeZ,
              lookX, lookY, lookZ,
              0, 1, 0)

    ground()
    roads()
    drawCity()

    glutSwapBuffers()

def keys(k, x, y):
    global eyeX, eyeY, eyeZ

    if k == b'w': eyeZ -= 1
    elif k == b's': eyeZ += 1
    elif k == b'a': eyeX -= 1
    elif k == b'd': eyeX += 1
    elif k == b'q': eyeY += 1
    elif k == b'e': eyeY -= 1

    glutPostRedisplay()

def reshape(w, h):
    if h == 0:
        h = 1

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w/h, 2, 80)

    glMatrixMode(GL_MODELVIEW)


def update(v):
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow(b"3D city simulation")

init()

glutDisplayFunc(display)
glutKeyboardFunc(keys)
glutReshapeFunc(reshape)
glutTimerFunc(0, update, 0)

glutMainLoop()