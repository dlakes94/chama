from __future__ import print_function
from nose.tools import *
from nose.plugins.skip import SkipTest
import chama.ray_cast as rc
import math
from pyutilib.misc import timing
import numpy as np
import pandas as pd

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

    ij_list = [(1, 1, 'rgba(0, 128, 0, 0.7)'),
               (2, 2, 'rgba(0, 128, 0, 0.7)')]

    grid.plotly_2d_grid(ij_list=ij_list)

#    grid.print_grid(intersect)

def test_ray_cast_cam():
    ###
    # define the tank farm
    ###
    grid = rc.Grid(xu=140.0, yu=140.0, zu=50.0, nx=140, ny=140, nz=1)
    # define tanks at 30, and 70 and 110 with a "radius" of 10 blocks
    for xc in [30.0, 70.0, 110.0]:
        for yc in [30.0, 70.0, 110.0]:
            for xcd in range(-10,11):
                for ycd in range(-10,11):
                    grid.add_obstacle(xc+xcd, yc+ycd, 0)

    theta_space, horizon_space = rc.get_camera_angle_spaces(theta_fov=60.0, horizon_fov=0.0, n_theta=150, n_horizon=10)

    camera_intersect = \
        rc.get_camera_intersections(grid=grid, x=1.0, y=1.0, z=1.0, theta_deg=45.0, theta_deg_space=theta_space,
                                    horizon_deg=0.0, horizon_deg_space=horizon_space, dist_step=0.25)

    ij_list = []
    for (i,j,k) in camera_intersect:
        ij_list.append((i,j,'rgba(0, 128, 0, 0.7)'))
#    print(camera_intersect)
    grid.plotly_2d_grid(ij_list=ij_list)


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

    grid.plotly_2d_grid()
    return

    # print(type(grid._grid_open))
    df_grid = pd.DataFrame(columns=['Grid','Open'])
    df_grid['Grid'] = grid._grid_open.keys()
    df_grid['Open'] = grid._grid_open.values()
    print(df_grid)

    timing.tic()
    camera_intersect = dict()
    z = 10.0
    theta_space, horizon_space = rc.get_camera_angle_spaces(theta_fov=60.0, horizon_fov=30.0, n_theta=10, n_horizon=10)
    for xc in np.linspace(0,1,num=2):
        for yc in np.linspace(0, 1, num=2):
            camera_intersect[(xc,yc,z)] = {}
            for ang in [0.0, 90.0, 180.0, 270.0]:
                camera_intersect[(xc,yc,z)][ang] = \
                    rc.get_camera_intersections(grid=grid, x=xc, y=yc, z=z, theta_deg=ang, theta_deg_space=theta_space, horizon_deg=0.0, horizon_deg_space=horizon_space, dist_step=0.25)



    """
    df = pd.DataFrame(camera_intersect,columns=camera_intersect.keys()).T
    set_grid = [(x,y,z) for x in range(0,140) for y in range(0,140) for z in range(0,50)]
    set_locations = df.index
    set_angles = df.columns
    # print(df)
    # print(df.columns)
    # print(df.index)

    out_loc = []
    out_dir = []
    out_obs = []
    # for loc in set_locations:
    #     d = set_angles
    #     v = [loc] * len(d)
    #     out_loc+=v
    #     out_dir+=d
    #     out_obs+=camera_intersect[loc].values()
    # for i in camera_intersect[(0,1,10)][0]:
    #     print(i)
    for loc in set_locations:
        for ang in set_angles:
            for val in camera_intersect[loc][ang]:
                out_loc.append(loc)
                out_dir.append(ang)
                out_obs.append(val)

    df2 = pd.DataFrame(columns=['Location','Direction','Observed'])
    df2['Location'] = out_loc
    df2['Direction'] = out_dir
    df2['Observed'] = out_obs
    print(df2)


    # file = 'test_ray_cast_data.py'
    # with open(file,'w+') as outfile:
    #     print('set_grid = ',set_grid, file=outfile)
    #     print('set_locations = ',set_locations, file=outfile)
    #     print('set_angles = ',set_angles, file=outfile)
    #     print('camera_intersect = ',camera_intersect, file=outfile)
    df_grid.to_csv('~/repositories/lairdrepo/users/tzhen/FireDetector/grid_data.csv')
    df2.to_csv('~/repositories/lairdrepo/users/tzhen/FireDetector/test_ray_cast_data.csv')
    timing.toc()
#    print(camera_intersect[25,0,0])
    """

if __name__ == '__main__':
    test_ray_cast_performance()

