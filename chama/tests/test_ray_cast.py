from nose.tools import *
from nose.plugins.skip import SkipTest
import chama.ray_cast as rc
import math
from pyutilib.misc import timing

def test_ray_cast():
    grid = rc.Grid(xu=100.0, yu=100.0, zu=50.0, nx=5, ny=5, nz=2)
    print(grid._x)
    print(grid._y)
    print(grid._z)

    grid.add_obstacle(0,3,0)
    grid.add_obstacle(1,2,0)

    intersect = rc.get_ray_intersections(grid, 10.0, 10.0, 10.0, math.pi/2.0, math.pi/2.0) # 90 deg
    intersect.update(rc.get_ray_intersections(grid, 10.0, 10.0, 10.0, math.pi/2.0, 0.0)) # 0 deg
    intersect.update(rc.get_ray_intersections(grid, 10.0, 10.0, 10.0, math.pi/2.0, math.pi/4.0)) # 0 deg)
    intersect.update(rc.get_ray_intersections(grid, 10.0, 10.0, 10.0, math.pi/4.0, 0.0)) # 0 deg)

    grid.print_grid(intersect)

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

    #grid.print_grid([])

    timing.tic()
    camera_intersect = dict()
    for cam_xc in range(0,141):
        print('... camera at ({}, {}, {})'.format(cam_xc, 0, 0))
        camera_intersect_i = set()
        for ang_deg in range(60,121):
            ang_rad = float(ang_deg)*math.pi/360.0
            intersect = rc.get_ray_intersections(grid, float(cam_xc), 0.0, 0.0, math.pi/2.0, ang_deg)
            camera_intersect_i.update(intersect)
        camera_intersect[(cam_xc, 0, 0)] = camera_intersect_i
    timing.toc()
    print(camera_intersect[25,0,0])

if __name__ == '__main__':
    test_ray_cast_performance()

