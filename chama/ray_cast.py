import math
import numpy as np
import itertools

class Grid(object):
    ''' Specifies a 3D geometry for use in ray-casting to determine what grid "cubes" cameras can and cannot see.

    A "grid" is specified in 3D space with a length in x, y, and z. The number of grid points in each of these
    directions is also specified. Once the grid is specified, individual grid "cubes" can be set to be an
    "obstacle" or open (by default).

    Args:
        xu (float) : length in the x direction (east-west)
        yu (float) : length in the y direction (north-south)
        zu (float) : length in the z direction (up-down)
        nx (int) : number of segments in the x direction
        ny (int) : number of segments in the y direction
        nz (int) : number of segments in the z direction
    '''
    def __init__(self, xu, yu, zu, nx, ny, nz):
        self._x = np.linspace(0.0, xu, nx+1)
        self._y = np.linspace(0.0, yu, ny+1)
        self._z = np.linspace(0.0, zu, nz+1)
        self._grid_open = dict()
        for (i,j,k) in np.ndindex(len(self._x), len(self._y), len(self._z)):
            self._grid_open[(i,j,k)] = True

    def add_obstacle(self, i, j, k):
        ''' Specify a particular grid "cube" to be an "obstacle" in terms of integer segment counts in x, y, and z.'''
        self._grid_open[i,j,k] = False

    def print_grid(self, mark_grid_list=None):
        ''' Print the grid, showing the obstacles and open grid "cubes", and well as any grid "cubes" in the mark_grid_list (only useful for testing small grids).

        Args:
             mark_grid_list (list of tuples) : a list of tuples identifying the (i, j, k) grid "cubes" that should be "marked"
        '''
        reverse_range_y = list()
        for j in range(len(self._y)-1):
            reverse_range_y.insert(0,j)

        for k in range(len(self._z)-1):
            print('*** z[{}] = {} -> {}'.format(k, self._z[k], self._z[k+1]))
            print('---------------------------j={}, y={}'.format(len(self._y)-1, self._y[-1]))
            for j in reverse_range_y:
                line = '|'
                for i in range(len(self._x)-1):
                    if self._grid_open[i,j,k]:
                        if mark_grid_list is not None and (i,j,k) in mark_grid_list:
                            line += '*|'
                        else:
                            line += ' |'
                    else:
                        line += 'X|'
                print(line)
                print('---------------------------j={}, y={}'.format(j, self._y[j]))


    def get_current_grid(self, x, y, z):
        ''' Return the grid corresponding to the passed in x, y, z or "None" if no grid exists at the point given.'''
        xi = np.searchsorted(self._x, x, side='right')-1
        if xi < 0 or xi >= len(self._x)-1:
            return None
        yi = np.searchsorted(self._y, y, side='right')-1
        if yi < 0 or yi >= len(self._y)-1:
            return None
        zi = np.searchsorted(self._z, z, side='right')-1
        if zi < 0 or zi >= len(self._z)-1:
            return None

        if self._grid_open[xi, yi, zi]:
            return (xi, yi, zi)

        return None


def get_ray_intersections(grid, x, y, z, theta_deg, horizon_deg, step=0.1):
    ''' Return the grid locations for all grids that are seen by a given ray.

    The grid is assumed to be dimensioned in x (east-west), y (north-south), and z (up-down).
    Given an (x,y,z) for the camera, and angles (specified by theta_deg and horizon_deg) the
    code will determine the grid locations that are "seen" by the camera.

    Args:
        x (float) : x-location for the camera (east-west)
        y (float) : y-location for the camera (north-south)
        z (float) : z-location for the camera (up-down)
        theta_deg (float) : the angle of the camera in the x-y plane (from the x+ axis)
                            E.g., 0 deg is straight east, 90 degrees is straight north
        horizon_deg (float) : the angle of the camera up and down (measured from the x-y plane).
                              E.g., 0 deg is horizontal, 90 deg is vertical.
        step (float) : integration step size (in distance units) used for the ray casting
    '''
    deg_to_rad = math.pi/180.0
    theta_rad = theta_deg*deg_to_rad
    z_phi_rad = (90.0-horizon_deg)*deg_to_rad

    xstep = step*math.sin(z_phi_rad)*math.cos(theta_rad)
    ystep = step*math.sin(z_phi_rad)*math.sin(theta_rad)
    zstep = step*math.cos(z_phi_rad)

    grid_intersections = set()

    k = 0
    (xk, yk, zk) = (x, y, z)
    current_grid = grid.get_current_grid(xk, yk, zk)
    while current_grid:
        # in a grid cube, add it to our intersections set
        grid_intersections.add(current_grid)

        # advance our point
        k += 1
        xk = x + k*xstep
        yk = y + k*ystep
        zk = z + k*zstep

        current_grid = grid.get_current_grid(xk, yk, zk)

    return grid_intersections


def get_camera_intersections(grid, x, y, z, theta_deg, horizon_deg, theta_fov, horizon_fov, n_theta=10, n_horizon=10, dist_step=0.1):
    print('... computing intersections for camera at ({}, {}, {}) with angles = ({},{})'.format(x, y, z, theta_deg, horizon_deg))
    camera_intersect = set()
    for theta_deg_i in np.linspace(theta_deg - theta_fov / 2.0, theta_deg + theta_fov / 2.0, num=n_theta):
        for horizon_deg_i in np.linspace(horizon_deg - horizon_fov / 2.0, horizon_deg + horizon_fov / 2.0, num=n_horizon):
            intersect = get_ray_intersections(grid, x, y, z, theta_deg=theta_deg_i, horizon_deg=horizon_deg_i, step=dist_step)
            camera_intersect.update(intersect) 

        
