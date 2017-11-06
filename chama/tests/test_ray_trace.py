import ray_trace as rt
import math

grid = rt.Grid(100.0,100.0,100.0, 5)
print(grid._x)
print(grid._y)
print(grid._z)

grid.add_obstacle(0,3,0)
print(grid._grid_open)

intersect = rt.get_grid_intersections(grid, 15.0, 15.0, 15.0, 0.0, math.pi/2.0) # 90 deg

print(intersect)
