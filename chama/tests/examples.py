from __future__ import print_function
import chama
import chama.optimize
import chama.ray_cast as rc
import math
import pandas as pd

def tuple_to_str(tuple):
    items = list()
    for t in tuple:
        items.append(str(t))
    return '-'.join(items)

def tuple_list_to_str_list(tuple_list):
    str_list = list()
    for t in tuple_list:
        str_list.append(tuple_to_str(t))
    return str_list

def empty_room():
    grid = rc.Grid(xu=100.0, yu=100.0, zu=5.0, nx=50, ny=50, nz=1)

    tspace_120, hspace_0 = rc.get_camera_angle_spaces(theta_fov=120.0, horizon_fov=0.0, n_theta=300, n_horizon=1)
    tspace_90, hspace_0 = rc.get_camera_angle_spaces(theta_fov=90.0, horizon_fov=0.0, n_theta=300, n_horizon=1)
    tspace_60, hspace_0 = rc.get_camera_angle_spaces(theta_fov=60.0, horizon_fov=0.0, n_theta=300, n_horizon=1)

    cam1 = rc.get_camera_intersections(grid, x=55.0, y=55.0, z=2.5, theta_deg=270.0, theta_deg_space=tspace_120,
                                    horizon_deg=0.0, horizon_deg_space=hspace_0, dist_step=0.1)
    cam1_str = tuple_list_to_str_list(cam1)

    cam2 = rc.get_camera_intersections(grid, x=0.0, y=50, z=2.5, theta_deg=0.0, theta_deg_space=tspace_90,
                                    horizon_deg=0.0, horizon_deg_space=hspace_0, dist_step=0.1)
    cam2_str = tuple_list_to_str_list(cam2)

    cam3 = rc.get_camera_intersections(grid, x=0.0, y=50, z=2.5, theta_deg=0.0, theta_deg_space=tspace_60,
                                    horizon_deg=0.0, horizon_deg_space=hspace_0, dist_step=0.1)
    cam3_str = tuple_list_to_str_list(cam3)

    coverage_dict = {'Sensor':['cam1', 'cam2', 'cam3'], 'Coverage': [cam1_str, cam2_str, cam2_str]}
    coverage=pd.DataFrame(coverage_dict)

    cov_opt = chama.optimize.CoverageSolver()
    results = cov_opt.solve(coverage=coverage, sensor_budget=1, redundancy=0)
    print(results)

    print(coverage.head())
    quit()

    ij_list = []
    for (i,j,k) in cam1:
        ij_list.append((i,j,'rgba(0, 128, 0, 0.7)'))

    grid.plotly_2d_grid('cam1', ij_list=ij_list, range={'x': [0,100], 'y':[0,100]})

    ij_list = []
    for (i,j,k) in cam2:
        ij_list.append((i,j,'rgba(128, 0, 0, 0.7)'))

    grid.plotly_2d_grid('cam2', ij_list=ij_list, range={'x': [0,100], 'y':[0,100]})

    ij_list = []
    for (i,j,k) in cam3:
        ij_list.append((i,j,'rgba(0, 0, 128, 0.7)'))

    grid.plotly_2d_grid('cam3', ij_list=ij_list, range={'x': [0,100], 'y':[0,100]})





if __name__ == '__main__':
    empty_room()

