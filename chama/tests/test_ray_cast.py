from nose.tools import *
from nose.plugins.skip import SkipTest
import chama.ray_cast as rc
import math
from pyutilib.misc import timing
import numpy as np



def test_ray_cast():
    grid = rc.Grid(xu=100.0, yu=100.0, zu=50.0, nx=5, ny=5, nz=2)
    print(grid._x)
    print(grid._y)
    print(grid._z)

    grid.add_obstacle(0,4,0)
    grid.add_obstacle(1,3,0)

    intersect = rc.get_ray_intersections(grid, 25.0, 25.0, 10.0, theta_deg = 0.0, horizon_deg = 0.0) # right deg
    intersect.update(rc.get_ray_intersections(grid, 25.0, 25.0, 10.0, theta_deg = 90.0, horizon_deg = 0.0)) # forward deg
    intersect.update(rc.get_ray_intersections(grid, 25.0, 25.0, 10.0, theta_deg = 180.0, horizon_deg = 0.0)) # left deg
    intersect.update(rc.get_ray_intersections(grid, 25.0, 25.0, 10.0, theta_deg = 270.0, horizon_deg = 0.0)) # backward deg
    intersect.update(rc.get_ray_intersections(grid, 25.0, 25.0, 10.0, theta_deg = 0.0, horizon_deg = 45.0)) # right and up slightly

    grid.print_grid(intersect)

    grid.plotly_plot_grid()

def test_ray_cast_small():
    grid = rc.Grid(xu=2, yu=2, zu=5, nx=1, ny=1, nz=1)
    grid.plotly_plot_grid()

def test_ray_cast_viz():
    ###
    # define the tank farm
    ###
    grid = rc.Grid(xu=14.0, yu=14.0, zu=5.0, nx=14, ny=14, nz=5)
    # define tanks at 30, and 70 and 110 with a "radius" of 10 blocks
    for xc in [3.0, 7.0, 11.0]:
        for yc in [3.0, 7.0, 11.0]:
            for xcd in range(-1,2):
                for ycd in range(-1,2):
                    for zd in range(0,4):
                        grid.add_obstacle(xc+xcd, yc+ycd, zd)

#    grid.plotly_plot_grid()
#    quit()
    #grid.print_grid([])

    timing.tic()
    camera_intersect = dict()
    for xc in np.linspace(0,14,num=14):
        for yc in np.linspace(0, 14, num=14):
            for ang in [0.0, 90.0, 180.0, 270.0]:
                camera_intersect[(xc,yc,ang)] = \
                    rc.get_camera_intersections(grid, xc, yc, 1.0, ang, 0.0, 60.0, 30.0, n_theta=30, n_horizon=1, dist_step=0.25)

    timing.toc()
#    print(camera_intersect[25,0,0])

def test_ray_cast_performance():
    ###
    # define the tank farm
    ###
    grid = rc.Grid(xu=140.0, yu=140.0, zu=50.0, nx=140, ny=140, nz=50)
    # define tanks at 30, and 70 and 110 with a "radius" of 10 blocks
    for xc in [30.0, 70.0, 110.0]:
        for yc in [30.0, 70.0, 110.0]:
            for xcd in range(-10,11):
                for ycd in range(-10,11):
                    for zd in range(0,31):
                        grid.add_obstacle(xc+xcd, yc+ycd, zd)

    grid.plotly_plot_grid()
    quit()
    #grid.print_grid([])

    timing.tic()
    camera_intersect = dict()
    for xc in np.linspace(0,140,num=14):
        for yc in np.linspace(0, 140, num=14):
            for ang in [0.0, 90.0, 180.0, 270.0]:
                camera_intersect[(xc,yc,ang)] = \
                    rc.get_camera_intersections(grid, xc, yc, 10.0, ang, 0.0, 60.0, 30.0, n_theta=30, n_horizon=1, dist_step=0.25)

    timing.toc()
#    print(camera_intersect[25,0,0])

if __name__ == '__main__':
    test_ray_cast_viz()

