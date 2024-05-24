# Tanks War Game

This project is a simple tank war game created with Python, utilizing Pygame and OpenGL. It was developed for a Computer Graphics course at the university.
## Description

In this game, two tanks battle against each other. The game includes features like shooting, moving, and tracking the mouse for aiming. The game also includes a health bar for each tank and ends when one of the tanks runs out of health.

## Installation

To run this game, you need to have Python installed on your system.

After installing Python, you need to install the required libraries(OpenGL). You can do this by running the following commands in your terminal:

```bash
pip install pygame
pip install PyOpenGL
```

## Controls
- Tank 1:
  - Move Left: a
  - Move Right: d
  - Shoot: Left Mouse Button


- Tank 2:
  - Move Left: Left j
  - Move Right: Right l
  - Shoot: Left Mouse Button


- Quit: q


## Challenges

The main challenges in developing this game were:

1. Implementing the physics for the tank movements and bullet trajectories.
2. Handling the collision detection between the tanks, bullets, and the environment.
3. Managing the game state, including the health of the tanks and the end of the game.

## Collision Detection

The game uses simple bounding box collision detection for the tanks and the environment. For the bullets, it uses point-to-rectangle collision detection. When a collision is detected, appropriate actions are taken, such as reducing the health of a tank or stopping a bullet.

## Converting Screen Coordinates to World Coordinates

The game uses the OpenGL library, which works in world coordinates, not screen coordinates. However, the mouse events provide coordinates in screen space. Therefore, we had to convert the screen coordinates to world coordinates. This was done using the aspect ratio of the screen and the defined world size.