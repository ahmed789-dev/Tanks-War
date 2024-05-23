from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
import sys
from math import *
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

INTERVAL = 12  # interval in milliseconds for Timer function
WIDTH, HEIGHT = screensize[0], screensize[1]
ASPECT_RATIO = WIDTH / HEIGHT
AXRNG = 10
GRAVITY = 25
texture_names = [0, 1, 2, 3, 4, 5]

def reposition_camera():
    gluLookAt(0, 0, 0, 0, 0, -1, 0, 1, 0)      # ===>(1)

def init():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    load_textures()

    glClearColor(0.0, 0.0, 0.0, 1.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    glOrtho(-AXRNG * ASPECT_RATIO, AXRNG * ASPECT_RATIO, -AXRNG, AXRNG, -AXRNG, AXRNG)  # by multiplying with the aspect ratio we solve the problem of stretching
    glMatrixMode(GL_MODELVIEW)

def texture_setup(texture_image_binary, texture_name, width, height):
    """  Assign texture attributes to specific images.
    """
    glBindTexture(GL_TEXTURE_2D, texture_name)  # texture init step [5]

    # texture init step [6]
    # affects the active selected texture which is identified by texture_name
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # END: texture init step [6]
    glTexImage2D(GL_TEXTURE_2D,
                 0,
                 4,
                 width, height,
                 0,  # Texture border
                 GL_RGBA,  # RGBA Exactly as in  pygame.image.tostring(image, "RGBA", True)
                 GL_UNSIGNED_BYTE,
                 texture_image_binary)  # texture init step [7]
    glBindTexture(GL_TEXTURE_2D, -1)


def load_textures():
    """  Open images and convert them to "raw" pixel maps and
             bind or associate each image with and integer reference number.
    """
    global texture_names
    glEnable(GL_TEXTURE_2D)  # texture init step [1]
    # Load images from file system
    images = []   # texture init step [2]
    images.append(pygame.image.load("pixelsky.jpg"))  # repeat this for more images
    images.append(pygame.image.load("pixelground.jpg"))
    images.append(pygame.image.load("end_game.jpg"))
    images.append(pygame.image.load("cloud.png"))



    # Convert images to the type needed for textures
    textures = [pygame.image.tostring(image, "RGBA", True)  # TODO change True to False
                for image in images]  # texture init step [3]

    # Generate textures names from array
    glGenTextures(len(images), texture_names[0])  # texture init step [4]

    # Add textures to openGL
    for i in range(len(images)):
        texture_setup(textures[i],  # binary images
                      texture_names[i],  # identifiers
                      images[i].get_width(),
                      images[i].get_height())

def ground(i_d,dx, dy, dz):
    global texture_names
    glLoadIdentity()
    reposition_camera()
    glColor3ub(50, 120, 250)
    glTranslate(dx, -AXRNG+dy/2, dz)
    # glScale(AXRNG * ASPECT_RATIO * 2, AXRNG * 2, 1)
    glBindTexture(GL_TEXTURE_2D, texture_names[i_d])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-AXRNG*ASPECT_RATIO, -dy/2, 0)

    glTexCoord2f(1, 0)
    glVertex3f(AXRNG*ASPECT_RATIO, -dy/2, 0)

    glTexCoord2f(1, 1)
    glVertex3f(AXRNG*ASPECT_RATIO, dy/2, 0)

    glTexCoord2f(0, 1)
    glVertex3f(-AXRNG*ASPECT_RATIO, dy/2, 0)

    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)

def background(i_d, dx, dy, dz):
    global texture_names
    glLoadIdentity()
    reposition_camera()
    glColor3ub(255, 255, 255)
    if i_d == 0:
        glColor3ub(100, 200, 200)
    glTranslate(dx, dy, dz)
    glBindTexture(GL_TEXTURE_2D, texture_names[i_d])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-AXRNG*ASPECT_RATIO, -AXRNG, 0)

    glTexCoord2f(1, 0)
    glVertex3f(AXRNG*ASPECT_RATIO, -AXRNG, 0)

    glTexCoord2f(1, 1)
    glVertex3f(AXRNG*ASPECT_RATIO, AXRNG, 0)

    glTexCoord2f(0, 1)
    glVertex3f(-AXRNG*ASPECT_RATIO, AXRNG, 0)

    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)

def play_song():
    pygame.mixer.init()  # Format the sound library
    pygame.mixer.music.load("sound_game.mp3")    # Download audio file
    pygame.mixer.music.play(-1)   # Play the audio file

class clouds():
    def __init__(self, x, y, z, width, height, radius, speed, number_of_clouds):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.radius = radius
        self.speed = speed
        self.number_of_clouds = number_of_clouds
    
    def render(self):
        glColor3d(1, 1, 1)
        glLoadIdentity()
        reposition_camera()

        glBindTexture(GL_TEXTURE_2D, texture_names[3])

        glTranslate(self.x, self.y, self.z)
        glBegin(GL_POLYGON)
        glTexCoord2f(0, 0)
        glVertex2f(-self.width/2, -self.height/2)

        glTexCoord2f(0, 1)
        glVertex2f(-self.width/2, self.height/2)

        glTexCoord2f(1, 1)
        glVertex2f(self.width/2, self.height/2)

        glTexCoord2f(1, 0)
        glVertex2f(self.width/2, -self.height/2)
        glEnd()

        glBindTexture(GL_TEXTURE_2D, -1)
        glLoadIdentity()

    def update(self):

        self.x += self.speed
        if self.x < -AXRNG * ASPECT_RATIO - self.width/2:
            self.x = AXRNG * ASPECT_RATIO + self.width/2
        elif self.x > AXRNG * ASPECT_RATIO + self.width/2:
            self.x = -AXRNG * ASPECT_RATIO - self.width/2


class Tank:
    def __init__(self, state, SHELL_RADIUS, speed, angle, tank_x, tank_y, health):
        self.state = state
        self.shell_x = tank_x
        self.shell_y = tank_y
        self.SHELL_RADIUS = SHELL_RADIUS
        self.speed = speed
        self.angle = angle

        self.tank_x = tank_x
        self.tank_y = tank_y
        self.wheel_radius = 0.4
        self.body_x_right = 1.5
        self.body_x_left = -1.5
        self.body_y_top = 0.5
        self.body_y_bottom = -0.5
        self.shooting = False
        self.bullet_radius = 0.2
        self.health = health


    def render(self):
        #######################################################
        glColor3d(0.2, 0, 0)
        glLoadIdentity()  # Draw canon of tank
        reposition_camera()
        glTranslate(self.tank_x, self.tank_y, 0)
        glRotate(self.angle, 0, 0, 1)
        glBegin(GL_POLYGON)
        glVertex2f(self.body_x_left * 0.1, 0)
        glVertex2f(self.body_x_right * 0.1, 0)
        glVertex2f(self.body_x_right * 0.1, 2)
        glVertex2f(self.body_x_left * 0.1, 2)
        glEnd()

        #######################################################
        glColor3d(0.8, 0.5, 0)
        glLoadIdentity()  # Draw body of tank
        reposition_camera()
        glTranslate(self.tank_x, self.tank_y, 0)
        glBegin(GL_POLYGON)
        glVertex2f(self.body_x_left, self.body_y_bottom)
        glVertex2f(self.body_x_right, self.body_y_bottom)
        glVertex2f(self.body_x_right * 2/3, self.body_y_top)
        glVertex2f(self.body_x_left * 2/3, self.body_y_top)
        glEnd()
        #######################################################
        glColor3d(0.7, 0.3, 0)
        glLoadIdentity()  # Draw wheels of tank
        reposition_camera()
        glTranslate(self.tank_x, self.tank_y, 0)
        glTranslate(1.5, -0.5, 0)
        glutSolidSphere(self.wheel_radius, 50, 50)
        #######################################################
        glColor3d(0.7, 0.3, 0)
        glLoadIdentity()  # Draw wheels of tank
        reposition_camera()
        glTranslate(self.tank_x, self.tank_y, 0)
        glTranslate(-1.5, -0.5, 0)
        glutSolidSphere(self.wheel_radius, 50, 50)

        #######################################################
        glColor3d(0.7, 0.3, 0)  # Draw base of wheels
        glLoadIdentity()
        reposition_camera()
        glTranslate(self.tank_x, self.tank_y, 0)
        glBegin(GL_POLYGON)
        glVertex2f(self.body_x_left, self.body_y_bottom - self.wheel_radius)
        glVertex2f(self.body_x_right, self.body_y_bottom - self.wheel_radius)
        glVertex2f(self.body_x_right, self.body_y_bottom + self.wheel_radius)
        glVertex2f(self.body_x_left, self.body_y_bottom + self.wheel_radius)
        glEnd()

        #######################################################
        glLoadIdentity()
        reposition_camera()
    
    def render_health(self, right):
        glColor3d(1, 0, 0)
        glLoadIdentity()
        reposition_camera()
        if right:  # draw health bar on right side
            glTranslate(AXRNG * ASPECT_RATIO, AXRNG - 1, 0)
            glLineWidth(20)
            glBegin(GL_LINES)
            glVertex2f(0, 0)
            glVertex2f(-self.health, 0)  # when health is 0, the line will be drawn from 0 to 0
            glEnd()
        if not right:  # draw health bar on left side
            glTranslate(-AXRNG * ASPECT_RATIO, AXRNG - 1, 0)
            glLineWidth(20)
            glBegin(GL_LINES)
            glVertex2f(0, 0)
            glVertex2f(self.health, 0)  # when health is 0, the line will be drawn from 0 to 0
            glEnd()

    def move_left(self):
        self.tank_x -= self.speed
    def move_right(self):
        self.tank_x += self.speed
    
    def track_mouse(self, world_x, world_y):  # world_x and world_y are the mouse coordinates in world space (not in screen space)
        self.angle = 90 + atan2(self.tank_y-world_y, self.tank_x-world_x) * 180 / pi
        self.mouse_x = world_x
        self.mouse_y = world_y

    def shoot(self, x, y, screen_world_ratio, tank_x, tank_y):
        self.shooting = True
        self.shell_x = tank_x
        self.shell_y = tank_y
        self.shell_vx = (x - tank_x) / 2.5
        self.shell_vy = (y - tank_y) / 2.5

    def update_shoot(self):
        if self.shooting:
            glColor3d(0, 0, 0)  # black color
            glTranslate(self.shell_x, self.shell_y, 0) # Draw shell
            glutSolidSphere(self.bullet_radius, 50, 50)
            self.shell_x += self.shell_vx * 0.1
            self.shell_y += self.shell_vy * 0.1
            self.shell_vy -= GRAVITY * 0.01

        if self.shell_x > AXRNG*ASPECT_RATIO or self.shell_x < -AXRNG*ASPECT_RATIO or self.shell_y > AXRNG or self.shell_y < -AXRNG + 2.5:
            print("outside allowed area:")
            self.shell_x = self.tank_x
            self.shell_y = self.tank_y
            self.shooting = False

    def is_collided(self, tank2):  # check collision with other tank
        if self.shell_x > tank2.tank_x + tank2.body_x_left and self.shell_x < tank2.tank_x + tank2.body_x_right and self.shell_y > tank2.tank_y + tank2.body_y_bottom and self.shell_y < tank2.tank_y + tank2.body_y_top:
            self.shooting = False
            self.shell_x = self.tank_x
            self.shell_y = self.tank_y
            tank2.health -= 1
            return True
    def is_collided_wall(self, wall_x, wall_y, wall_width, wall_height):  # check collision of tank with wall
        if self.shell_x > wall_x - wall_width/2 and self.shell_x < wall_x + wall_width/2 and self.shell_y > wall_y - wall_height/2 and self.shell_y < wall_y + wall_height/2:
            self.shooting = False
            return True



class Game:
    def __init__(self):
        self.tank1 = Tank(1, 0.25, 0.25, 30, 12, -AXRNG + 2.8, 10)
        self.tank2 = Tank(0, 0.25, 0.25, -60, -12, -AXRNG + 2.8, 10)
        self.keystates = {'w': False, 'd': False, 'a': False, 's': False
                          , 'j': False, 'k': False, 'l': False, 'i': False}
        self.mousestates = {'RMB': False, 'LMB': False}
        self.clouds = []
        self.cloud1 = clouds(-AXRNG*ASPECT_RATIO + AXRNG    , AXRNG - 3, 0, 10, 10, 1, 0.1, 3)
        self.cloud2 = clouds(-AXRNG*ASPECT_RATIO + AXRNG + 5, AXRNG - 4, 0, 10, 10, 1, 0.12, 3)
        self.cloud3 = clouds(-AXRNG*ASPECT_RATIO + AXRNG - 5, AXRNG - 6, 0, 10, 10, 1, -0.05, 3)
        self.clouds.append(self.cloud1)
        self.clouds.append(self.cloud2)
        self.clouds.append(self.cloud3)
        self.wall_x = 0
        self.wall_y = -6
        self.wall_height = 8
        self.wall_width = 2
        

    def render(self):
        self.tank1.render()
        self.tank2.render()
        self.clouds.render()
    
    def render_wall(self, wall_x, wall_y, wall_width, wall_height):
        glColor3ub(30, 50, 70)
        glLoadIdentity()
        reposition_camera()
        glTranslate(wall_x, wall_y, 0)
        glBegin(GL_POLYGON)
        glVertex2f(-wall_width/2, -wall_height/2)
        glVertex2f(wall_width/2, -wall_height/2)
        glVertex2f(wall_width/2, wall_height/2)
        glVertex2f(-wall_width/2, wall_height/2)
        glEnd()

        # Add code to render other game objects

    def handle_keypress(self, key, x, y):
        if key == b"w":
            self.keystates['w'] = True
        elif key == b"d":
            self.keystates['d'] = True
        elif key == b"a":
            self.keystates['a'] = True
        elif key == b"s":
            self.keystates['s'] = True
        elif key == b"j":
            self.keystates['j'] = True
        elif key == b"k":
            self.keystates['k'] = True
        elif key == b"l":
            self.keystates['l'] = True
        elif key == b"i":
            self.keystates['i'] = True
        elif key == b"q":  # exit the game when press Q
            sys.exit()

    def handle_keyrelease(self, key, x, y):
        if key == b"w":
            self.keystates['w'] = False
        elif key == b"d":
            self.keystates['d'] = False
        elif key == b"a":
            self.keystates['a'] = False
        elif key == b"s":
            self.keystates['s'] = False
        elif key == b"j":
            self.keystates['j'] = False
        elif key == b"k":
            self.keystates['k'] = False
        elif key == b"l":
            self.keystates['l'] = False
        elif key == b"i":
            self.keystates['i'] = False
    
    def handle_mouse(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                self.mousestates['LMB'] = True
                # Convert mouse coordinates from screen space to world space
                world_x = (x / WIDTH) * (2 * AXRNG * ASPECT_RATIO) - AXRNG * ASPECT_RATIO
                world_y = ((HEIGHT - y) / HEIGHT) * (2 * AXRNG) - AXRNG
                screen_world_ratio = abs(self.tank1.tank_x) // (AXRNG * ASPECT_RATIO)  # which page is the tank in
                # print("screen word ration (which page ) : ", screen_world_ratio)
                if self.tank1.state:
                    self.tank1.shoot(world_x, world_y, screen_world_ratio, self.tank1.tank_x, self.tank1.tank_y)
                elif self.tank2.state:
                    self.tank2.shoot(world_x, world_y, screen_world_ratio, self.tank2.tank_x, self.tank2.tank_y)
                # handle left mouse button press
            elif state == GLUT_UP:
                self.mousestates['LMB'] = False
                self.tank1.state = not self.tank1.state  # switch between tanks
                self.tank2.state = not self.tank2.state  # switch between tanks
                # handle left mouse button release
        elif button == GLUT_RIGHT_BUTTON:
            if state == GLUT_DOWN:
                self.mousestates['RMB'] = True
                # handle right mouse button press
            elif state == GLUT_UP:
                self.mousestates['RMB'] = False
                # handle right mouse button release
    def handle_mouse_motion(self, x, y):
        # Convert mouse coordinates from screen space to world space
        world_x = (x / WIDTH) * (2 * AXRNG * ASPECT_RATIO) - AXRNG * ASPECT_RATIO
        world_y = ((HEIGHT - y) / HEIGHT) * (2 * AXRNG) - AXRNG
        if self.tank1.state:
            self.tank1.track_mouse(world_x, world_y)
        elif self.tank2.state:
            self.tank2.track_mouse(world_x, world_y)

    def update(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)
        background(0, 0, 0, 0)
        ground(1,0, 3, 0)

        # Add code to update game logic
        if self.keystates['d'] and self.tank1.state and self.tank1.tank_x + self.tank1.body_x_right + self.tank1.wheel_radius < AXRNG * ASPECT_RATIO:
            self.tank1.move_right()
        if self.keystates['a'] and self.tank1.state and self.tank1.tank_x - self.tank1.body_x_right - self.tank1.wheel_radius > self.wall_width/2:
            self.tank1.move_left()
        if self.keystates['j'] and self.tank2.state and self.tank2.tank_x - self.tank2.body_x_right - self.tank2.wheel_radius > -AXRNG * ASPECT_RATIO:
            self.tank2.move_left()
        if self.keystates['l'] and self.tank2.state and self.tank2.tank_x + self.tank2.body_x_right + self.tank2.wheel_radius < -self.wall_width/2:
            self.tank2.move_right()

        self.tank1.render_health(True) # True means draw right
        self.tank2.render_health(False) # false means draw left
        
        self.render_wall(self.wall_x, self.wall_y, self.wall_width, self.wall_height)  # Draw wall
        self.tank1.is_collided_wall(self.wall_x, self.wall_y, self.wall_width, self.wall_height)  # Check collision with wall for tank1
        self.tank2.is_collided_wall(self.wall_x, self.wall_y, self.wall_width, self.wall_height)  # check collision with wall for tank2

        for cloud in self.clouds:  # Draw clouds
            cloud.render()
            cloud.update()


        self.tank1.update_shoot()
        self.tank2.update_shoot()
        self.tank1.is_collided(self.tank2)
        self.tank2.is_collided(self.tank1)
        self.tank1.render()
        self.tank2.render()

        if self.tank1.health <= 0:
            background(2, 0, 0, 0)
        elif self.tank2.health <= 0:
            background(2, 0, 0, 0)

        glutSwapBuffers()

    def game_timer(self, v):
        self.update()
        glutTimerFunc(INTERVAL, self.game_timer, v)

def main():
    game = Game()
    glutInit()
    play_song()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowPosition(100, 100)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"Tank War")
    # glutFullScreen()
    init()
    glutDisplayFunc(game.update)
    glutKeyboardFunc(game.handle_keypress)
    glutKeyboardUpFunc(game.handle_keyrelease)
    glutMouseFunc(game.handle_mouse)
    glutPassiveMotionFunc(game.handle_mouse_motion)
    glutTimerFunc(INTERVAL, game.game_timer, 1)
    glutMainLoop()


if __name__ == "__main__":
    main()



