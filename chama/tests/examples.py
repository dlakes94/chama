from __future__ import print_function
import chama
import chama.optimize
import chama.ray_cast as rc
import math
import pandas as pd

def empty_room():
    grid = rc.Grid(xu=11.0, yu=11.0, zu=5.0, nx=22, ny=22, nz=1)

    tspace_180, hspace_0 = rc.get_camera_angle_spaces(theta_fov=90.0, horizon_fov=0.0, n_theta=300, n_horizon=1)

    cam1 = rc.get_ray_intersections(grid, x=0.0, y=11.0, z=2.5, theta_deg=0.0, theta_deg_space=tspace_180,
                                    horizon_deg=0.0, horizon_deg_space=hspace_0, dist_step=0.1)
    
    ij_list = []
    for (i,j,k) in cam1:
        ij_list.append((i,j,'rgba(0, 128, 0, 0.7)'))

    grid.plotly_2d_grid(ij_list=ij_list)


if __name__ == '__main__':
    empty_room()

