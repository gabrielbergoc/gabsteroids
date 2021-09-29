import os
from math import *
import pygame
from pygame.locals import *

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]


def load_image(name, colorkey=None):
    """loads image from "images" folder and returns Surface and Rect objects"""

    full_name = os.path.join(MAIN_DIR, name)

    try:
        image = pygame.image.load(full_name)
        image.convert_alpha(image)
    except pygame.error as error:
        print(f"Cannot load image '{name}'")
        raise SystemExit(error)

    # image = image.convert()   # if converted, image gets weirdly resized

    # if colorkey is provided, sets it
    if colorkey is not None:

        # if colorkey argument is -1, gets value from top-left pixel
        if colorkey == -1:
            colorkey = image.get_at((0, 0))

        image.set_colorkey(colorkey, RLEACCEL)

    return image, image.get_rect()

def matrix_mult(matrixA, matrixB):
    """multiplies two matrices"""

    if len(matrixA[0]) != len(matrixB):
        raise ValueError("matrixA row size must be equal to matrixB column size")

    matrixC = [[0 for _ in range(len(matrixB[0]))] for _ in range(len(matrixA))]

    for i in range(len(matrixC)):
        for j in range(len(matrixC[0])):
            for k in range(len(matrixB)):
                matrixC[i][j] += matrixA[i][k] * matrixB[k][j]

    return matrixC

def rotate_vector(vector, angle):
    """rotate vector by given angle (degrees)"""

    angle = radians(angle)
    vector = [[vector[0]], [vector[1]]]

    rotation_matrix = [[cos(angle), -sin(angle)],
                       [sin(angle), cos(angle)]]

    return matrix_mult(rotation_matrix, vector)


# --------- TESTS --------- #

if __name__ == '__main__':

    matrixA = [[1, 0],
               [-2, 3],
               [5, 4],
               [0, 1]]

    matrixB = [[0, 6, 1],
               [3, 8, -2]]

    print(matrix_mult(matrixA, matrixB))

    matrixA = [[1, -1, 1],
               [-3, 2, -1],
               [-2, 1, 0]]

    matrixB = [[1, 2, 3],
               [2, 4, 6],
               [1, 2, 3]]

    print(matrix_mult(matrixA, matrixB))
    print(matrix_mult(matrixB, matrixA))

    vectors = [
        [1, 1],
        [1, 2],
        [1, 3],
        [2, 1],
        [2, 2],
        [2, 3],
        [3, 1],
        [3, 2],
        [3, 3]
    ]

    for vector in vectors:
        print(rotate_vector(vector, 45))
        print(rotate_vector(vector, -45))
