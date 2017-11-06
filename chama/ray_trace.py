import math
import numpy as np
import itertools

class Grid(object):
    def __init__(self, xu, yu, zu, n):
        self._x = np.linspace(0.0, xu, n+1)
        self._y = np.linspace(0.0, yu, n+1)
        self._z = np.linspace(0.0, zu, n+1)
        self._grid_open = dict()
        for (i,j,k) in np.ndindex(len(self._x), len(self._y), len(self._z)):
            self._grid_open[(i,j,k)] = True

    def add_obstacle(self, i, j, k):
        self._grid_open[i,j,k] = False


    def get_current_grid(self, xk, yk, zk):
        xi = np.searchsorted(self._x, xk, side='right')-1
        if xi < 0 or xi >= len(self._x)-1:
            return None
        yi = np.searchsorted(self._y, yk, side='right')-1
        if yi < 0 or yi >= len(self._y)-1:
            return None
        zi = np.searchsorted(self._z, zk, side='right')-1
        if zi < 0 or zi >= len(self._z)-1:
            return None

        if self._grid_open[xi, yi, zi]:
            return (xi, yi, zi)

        return None
        
def get_ray_intersections(grid, x, y, z, phi, theta, step=0.1):
    grid_intersections = set()

    k = 0
    (xk, yk, zk) = (x, y, z)
    current_grid = grid.get_current_grid(xk, yk, zk)
    while current_grid:
        # in a grid cube, add it to our intersections set
        grid_intersections.add(current_grid)

        # advance our point
        k += 1
        xk = x + k*step*math.sin(theta)*math.cos(phi)
        yk = y + k*step*math.sin(theta)*math.sin(phi)
        zk = z + k*step*math.cos(theta)

        print('checking:', xk, yk, zk)
        current_grid = grid.get_current_grid(xk, yk, zk)
        print(current_grid)
        
def get_camera_intersections(grid, x, y, z, phi, theta, phi_fov, theta_fov, step=0.1):
    pass
        
