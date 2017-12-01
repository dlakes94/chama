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

    cam1 = rc.get_camera_intersections(grid, x=1.0, y=75, z=2.5, theta_deg=0.0, theta_deg_space=tspace_120,
                                    horizon_deg=0.0, horizon_deg_space=hspace_0, dist_step=0.1)
    cam1_str = tuple_list_to_str_list(cam1)
    cam1_ij_list = []
    for (i,j,k) in cam1:
        cam1_ij_list.append((i,j,'rgba(255, 128, 0, 0.7)'))

    cam2 = rc.get_camera_intersections(grid, x=1.0, y=50, z=2.5, theta_deg=0.0, theta_deg_space=tspace_90,
                                    horizon_deg=0.0, horizon_deg_space=hspace_0, dist_step=0.1)
    cam2_str = tuple_list_to_str_list(cam2)
    cam2_ij_list = []
    for (i,j,k) in cam2:
        cam2_ij_list.append((i,j,'rgba(0, 128, 0, 0.7)'))


    cam3 = rc.get_camera_intersections(grid, x=1.0, y=25, z=2.5, theta_deg=0.0, theta_deg_space=tspace_60,
                                    horizon_deg=0.0, horizon_deg_space=hspace_0, dist_step=0.1)
    cam3_str = tuple_list_to_str_list(cam3)
    cam3_ij_list = []
    for (i,j,k) in cam3:
        cam3_ij_list.append((i,j,'rgba(0, 0, 128, 0.7)'))

    cam3_ij_list_trunc = []
    for (i,j,k) in cam3:
        if i**2 + j**2 + k**2 < 1200:
            cam3_ij_list_trunc.append((i,j,'rgba(0, 0, 128, 0.7)'))

    grid.plotly_2d_grid('cam1', ij_list=cam1_ij_list)
    grid.plotly_2d_grid('cam2', ij_list=cam2_ij_list)
    grid.plotly_2d_grid('cam3', ij_list=cam3_ij_list)
    grid.plotly_2d_grid('cam1_cam2', ij_list=cam2_ij_list+cam1_ij_list)
    grid.plotly_2d_grid('all_cams', ij_list=cam2_ij_list+cam1_ij_list+cam3_ij_list)
    grid.plotly_2d_grid('all_cams_trunc', ij_list=cam2_ij_list+cam1_ij_list+cam3_ij_list_trunc)

    coverage_dict = {'Sensor':['cam1', 'cam2', 'cam3'], 'Coverage': [cam1_str, cam2_str, cam3_str]}
    coverage=pd.DataFrame(coverage_dict)

    entity_dict = {'Entity': [], 'Weight': [], 'Tuple': []}
    all_grids = grid.get_all_grid_ijk()
    print(len(all_grids))
    for (i,j,k) in all_grids:
        grid_str = tuple_to_str((i,j,k))
        weight = 1.0
        if j > 45 and i < 10:
            weight = 5000.0
        entity_dict['Entity'].append(grid_str)
        entity_dict['Weight'].append(weight)
        entity_dict['Tuple'].append((i,j,k))
    entities = pd.DataFrame(entity_dict)

    cov_opt = chama.optimize.CoverageSolver()
    results = cov_opt.solve(coverage=coverage, entities=entities, sensor_budget=1, redundancy=0)
    print(results['FractionDetected'], results['Sensors'])

    # test sensor cost
    sensor_dict = {'Sensor': ['cam1', 'cam2', 'cam3'], 'Cost': [5, 3, 1]}
    sensor = pd.DataFrame(sensor_dict)

    results = cov_opt.solve(coverage=coverage, entities=entities, sensor=sensor, sensor_budget=2, redundancy=0)
    print(results['FractionDetected'], results['Sensors'])
#    print(results['EntityAssessment'])

    results = cov_opt.solve(coverage=coverage, entities=entities, sensor=sensor, sensor_budget=2, redundancy=0, use_sensor_cost=True)
    print(results['FractionDetected'], results['Sensors'])

    # test priority grids
    results = cov_opt.solve(coverage=coverage, entities=entities, sensor_budget=1, redundancy=0, use_entity_weights=True)
    print(results['FractionDetected'], results['Sensors'])
#    print(results['EntityAssessment'])
#    print(results['Objective'])

    priority_ij_list = []
    for (idx, t) in enumerate(entity_dict['Tuple']):
        if entity_dict['Weight'][idx] > 10:
            priority_ij_list.append((t[0], t[1],'rgba(128, 0, 0, 0.7)'))
    grid.plotly_2d_grid('cam2_wieght', ij_list=cam2_ij_list+priority_ij_list)
    grid.plotly_2d_grid('cam1_wieght', ij_list=cam1_ij_list+priority_ij_list)

    quit()



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

