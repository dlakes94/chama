from nose.tools import *
from nose.plugins.skip import SkipTest
import chama.ray_cast as rc
import math

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

if __name__ == '__main__':
    test_ray_cast()

