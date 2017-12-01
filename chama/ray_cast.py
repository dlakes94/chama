import math
import numpy as np
import itertools

import plotly
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout, Scatter3d, Mesh3d
import plotly.plotly as py

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
        self._dx = xu/float(nx)
        self._dy = yu/float(ny)
        self._dz = zu/float(nz)
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
        if x > self._x[-1] or y > self._y[-1] or z > self._z[-1]:
            return None
        xi = math.floor(x/self._dx)
        yi = math.floor(y/self._dy)
        zi = math.floor(z/self._dz)
        if xi < 0 or yi < 0 or zi < 0:
            return None

        if self._grid_open[xi, yi, zi]:
            return (xi, yi, zi)

        return None

    def old_get_current_grid(self, x, y, z):
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

    def plotly_2d_grid(self, ij_list=None):
        shapes = list()

        for (i, j) in np.ndindex(len(self._x) - 1, len(self._y) - 1):
            color = 'rgba(204, 204, 204, 0.3)'
            if self._grid_open[(i, j, 0)] == False:
                color = 'rgba(51, 51, 51, 1.0)'
            shape = {
                        'type': 'rect',
                        'x0': self._x[i],
                        'y0': self._y[j],
                        'x1': self._x[i]+self._dx,
                        'y1': self._y[j]+self._dy,
                        'fillcolor': color,
                        'line': {
                            'width': 0
                        }
                        #'color': 'rgba(128, 0, 128, 1)',
                        #}
            }
            shapes.append(shape)

        if ij_list is not None:
            for (i, j, color) in ij_list:
                shape = {
                        'type': 'rect',
                        'x0': self._x[i],
                        'y0': self._y[j],
                        'x1': self._x[i]+self._dx,
                        'y1': self._y[j]+self._dy,
                        'fillcolor': color,
                        'line': {
                            'width': 0
                        }
                        #'color': 'rgba(128, 0, 128, 1)',
                        #}
                }
                shapes.append(shape)

#            objs = _plotly_cube_mesh(self._x[i], self._y[j], self._z[k],
#                                     self._dx, self._dy, self._dz,
#                                     include_mesh=include_mesh,
#                                     opacity=opacity,
#                                     include_lines=True)

        trace0 = go.Scatter(
            x=[1.5, 3],
            y=[2.5, 2.5],
            text=[''],
            mode='text',
        )
        layout = {
            'shapes': shapes
        }
        plt = plotly.offline.plot({
            "data": [trace0],
            "layout": layout,
            })




    def plotly_plot_grid(self):
        cubes=list()
        for (i,j,k) in np.ndindex(len(self._x)-1, len(self._y)-1, len(self._z)-1):
            if j == 0 and k == 0:
                print('***', i, j, k)
            opacity = 1.0
            include_mesh=False
            if self._grid_open[(i,j,k)] == False:
                include_mesh=True
            objs = _plotly_cube_mesh(self._x[i], self._y[j], self._z[k],
                                     self._dx, self._dy, self._dz,
                                     include_mesh=include_mesh,
                                     opacity=opacity,
                                     include_lines=True)
            cube_faces = _plotly_cube_objects(i, j, k, style='faces', opacity=opacity)
            cubes.extend(objs)
#            cubes.extend(cube_faces)

        layout = dict(
#            length=len(self._x),
#            width=len(self._y)+2,
#            height=len(self._z)+2,
            autosize=True,
            title='grid',
            scene=dict(
                xaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)'
                ),
                yaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)'
                ),
                zaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)'
                ),
                camera=dict(
                    up=dict(
                        x=0,
                        y=0,
                        z=1
                    ),
                    eye=dict(
                        x=-1.7428,
                        y=1.0707,
                        z=0.7100,
                    )
                ),
                aspectratio=dict(x=1, y=1, z=1.0),
                aspectmode='manual'
            ),
        )

        #plt = plotly.offline.plot({
        #    "data": cubes,
        #    "layout": layout,
        #    })

        py.image.save_as({
            "data": cubes,
            "layout": layout,
            }, filename='a-simple-plot.png')
        #print(plt)

def _plotly_cube_faces():
    p = [(0,0,0), (1,0,0), (1,1,0), (0,1,0), (0,0,1), (1,0,1), (1,1,1), (0,1,1)]
    faces = list()
    faces.append([p[0], p[1], p[5], p[4], p[0]])
    faces.append([p[1], p[2], p[6], p[5], p[1]])
    return faces

def _plotly_tri_cube_faces():
    p = [(0,0,0), (1,0,0), (1,1,0), (0,1,0), (0,0,1), (1,0,1), (1,1,1), (0,1,1)]
    faces = list()
    faces.append([p[0], p[6], p[7], p[0]])
    faces.append([p[0], p[6], p[1], p[0]])
    return faces

def _plotly_cube_mesh(x, y, z, dx, dy, dz, include_mesh=False, opacity=0.5, include_lines=True):
    xv0 = [0, 1, 1, 0, 0, 1, 1, 0]
    xv = [xvi*dx + x for xvi in xv0]
    yv0 = [0, 0, 1, 1, 0, 0, 1, 1]
    yv = [yvi*dy + y for yvi in yv0]
    zv0 = [0, 0, 0, 0, 1, 1, 1, 1]
    zv = [zvi*dz + z for zvi in zv0]
    objs = list()
    if include_mesh:
        i = [1, 4, 1, 3, 1, 2, 5, 7, 3, 4, 2, 7]
        j = [0, 5, 0, 2, 2, 6, 6, 4, 0, 7, 6, 3]
        k = [4, 1, 3, 1, 5, 5, 7, 5, 4, 3, 7, 2]
        mesh = go.Mesh3d(x=xv, y=yv, z=zv,
                         color='#1f77b4',
                         i=i, j=j, k=k,
                         lighting=dict(ambient=0.2),
                         opacity=opacity)
        objs.append(mesh)

    if include_lines:
        lines = [(0, 1), (1, 5), (5, 4), (4, 0), (4, 7), (7, 3), (3, 0), (3, 2), (2, 6), (6, 7), (5, 6), (1, 2)]
        for lv in lines:
            xl = [xv[lv[0]], xv[lv[1]]]
            yl = [yv[lv[0]], yv[lv[1]]]
            zl = [zv[lv[0]], zv[lv[1]]]

            line = Scatter3d(x=xl, y=yl, z=zl,
                           marker=dict(
                               size=4,
                               color='#1f77b4',
                           ),
                           line=dict(
                               color='#1f77b4',
                               width=3
                           )
                         )
            objs.append(line)

    return objs

def _plotly_cube_objects(x, y, z, style='line', color='#1f77b4', opacity=1.0):
    objs = list()
    for f in _plotly_cube_faces():
        xp = [pt[0]+x for pt in f]
        yp = [pt[1]+y for pt in f]
        zp = [pt[2]+z for pt in f]

#        print(x, y, x)

        surf = Scatter3d(x=xp, y=yp, z=zp,
                           marker=dict(
                               size=4,
                               color='#1f77b4',
                           ),
                           line=dict(
                               color='#1f77b4',
                               width=3
                           )
                         )

        objs.append(surf)
        surf = go.Mesh3d(x=xp, y=yp, z=zp,
                         color=color,
                         delaunayaxis='x',
                         opacity=0.5)
        objs.append(surf)
    return objs

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

def get_camera_angle_spaces(theta_fov, horizon_fov, n_theta=10, n_horizon=10):
    theta_deg_space = np.linspace(-theta_fov / 2.0, theta_fov / 2.0, num=n_theta)
    horizon_deg_space = np.linspace(-horizon_fov / 2.0, horizon_fov / 2.0, num=n_horizon)
    return (theta_deg_space, horizon_deg_space)

def get_camera_intersections(grid, x, y, z, theta_deg, theta_deg_space, horizon_deg, horizon_deg_space, dist_step=0.1):
    #    print('... computing intersections for camera at ({}, {}, {}) with angles = ({},{})'.format(x, y, z, theta_deg, horizon_deg))
    camera_intersect = set()
    theta_space = theta_deg_space + theta_deg
    horizon_space = horizon_deg_space + horizon_deg
    for theta_deg_i in theta_space: #np.linspace(theta_deg - theta_fov / 2.0, theta_deg + theta_fov / 2.0, num=n_theta):
        for horizon_deg_i in horizon_space: #np.linspace(horizon_deg - horizon_fov / 2.0, horizon_deg + horizon_fov / 2.0, num=n_horizon):
            intersect = get_ray_intersections(grid, x, y, z, theta_deg=theta_deg_i, horizon_deg=horizon_deg_i, step=dist_step)
            camera_intersect.update(intersect)

    return camera_intersect
