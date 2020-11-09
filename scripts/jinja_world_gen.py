#!/usr/bin/env python3
"""
Generate Worlds
@author: Benjamin Perseghetti
@email: bperseghetti@rudislabs.com
"""
import jinja2
import argparse
import os
import fnmatch
import numpy as np

rel_px4_gazebo_path = ".."
rel_world_path ="../worlds"
script_path = os.path.realpath(__file__).replace("jinja_world_gen.py","")
default_env_path = os.path.relpath(os.path.join(script_path, rel_px4_gazebo_path))
default_world_path = os.path.relpath(os.path.join(script_path, rel_world_path))
default_filename = os.path.relpath(os.path.join(default_world_path, "gen.world.jinja"))
default_sdf_world_dict = {
    "empty": 1.5,
    "mcmillan": 1.5,
    "ksql": 1.5,
    "irlock": 1.5,
    "boat": 1.5,
    "baylands": 1.5,
    "yosemite": 1.5,
    "windy": 1.5,
    "warehouse": 1.5,
    "typhoon": 1.5,
    "raceway": 1.5
}
hitl_model_dict = {
    "plane": "0 0 0.25 0 0 0",
    "standard_vtol": "0 0 0.25 0 0 0",
    "iris": "0 0 0.25 0 0 0",
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdf_version', default="NotSet", help="SDF format version to use for interpreting world file")
    parser.add_argument('--sun_model', default="sun_2", help="Select sun model [sun, sun_2, NoSun]")
    parser.add_argument('--cloud_speed', default="NoClouds", help="Turn on clouds with given speed")
    parser.add_argument('--shadows', default=1, help="Shadows on [1] or off [0]")
    parser.add_argument('--video_widget', default="NotSet", help="GUI video widget on [1] or off [0]")
    parser.add_argument('--update_rate', default=250, help="Real time update rate.")
    parser.add_argument('--wind_speed', default="NotSet", help="Turn on wind with given mean speed.")
    parser.add_argument('--realtime_factor', default=1.0, help="Real time factor.")
    parser.add_argument('--world_name', default="empty", help="Name of world, see default_sdf_world_dict for options")
    parser.add_argument('--ambient_light', default=0.95, help="Value for ambient light [0.0..1.0]")
    parser.add_argument('--background_light', default=0.3, help="Value for background light [0.0..1.0]")
    parser.add_argument('--spherical_coords', default="NotSet", help="Enable or disable spherical coordinates on [1] or off [0]")
    parser.add_argument('--latitude', default=39.8039, help="Latitude for spherical coordinates")
    parser.add_argument('--longitude', default=-84.0606, help="Longitude for spherical coordinates")
    parser.add_argument('--altitude', default=244, help="Altitude for spherical coordinates")
    parser.add_argument('--model_name', default="NotSet", help="Model to be used for hitl case in jinja world file")
    parser.add_argument('--model_pose', default="NotSet", help="Pose: 'x y z r p y' of model")
    parser.add_argument('--irlock_beacon_pose', default="NotSet", help="Pose: 'x y z r p y' of irlock beacon")
    parser.add_argument('--output_file', help="world output file")
    parser.add_argument('--ode_threads', default=2, help="Number of island threads to use for ODE.")
    args = parser.parse_args()


    if args.world_name not in default_sdf_world_dict:
        print("\nERROR!!!")
        print('World name: "{:s}" DOES NOT MATCH any entries in default_sdf_world_dict.\nTry world name:'.format(args.world_name))
        for world_option in default_sdf_world_dict:
            print('\t{:s}'.format(world_option))
        print("\nEXITING jinja_world_gen.py...\n")
        exit(1)

    if args.sdf_version == "NotSet":
        args.sdf_version = default_sdf_world_dict.get(args.world_name)
        print('SDF version is NOT EXPLICITLY SET, world name: "{:s}" is using default SDF version: {:s}'.format(args.world_name, str(args.sdf_version)))
    
    if (args.model_name != "NotSet" ) and (args.model_name not in hitl_model_dict):
        print("\nERROR!!!")
        print('Model name: "{:s}" DOES NOT MATCH any entries for HITL in hitl_model_dict.\nTry HITL capable model name:'.format(args.model_name))
        for hitl_model_option in hitl_model_dict:
            print('\t{:s}'.format(hitl_model_option))
        print("\nEXITING jinja_world_gen.py...\n")
        exit(1)

    if (args.model_pose == "NotSet") and (args.model_name in hitl_model_dict):
        args.model_pose = hitl_model_dict.get(args.model_name)
        print('Model pose is NOT EXPLICITLY SET, setting to hitl_model_dict default pose: "{:s}"'.format(args.model_pose))

    args.model_name = 'temp_{:s}_hitl'.format(args.model_name)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(default_env_path))
    template = env.get_template(os.path.relpath(default_filename, default_env_path))

    # create dictionary with useful modules etc.
    try:
        import rospkg
        rospack = rospkg.RosPack()
    except ImportError:
        pass
        rospack = None

    d = {'np': np, 'rospack': rospack, \
         'sdf_version': args.sdf_version, \
         'sun_model': args.sun_model, \
         'cloud_speed': args.cloud_speed, \
         'shadows': args.shadows, \
         'video_widget': args.video_widget, \
         'wind_speed': args.wind_speed, \
         'update_rate': args.update_rate, \
         'realtime_factor': args.realtime_factor, \
         'ambient_light': args.ambient_light, \
         'background_light': args.background_light, \
         'spherical_coords': args.spherical_coords, \
         'latitude': args.latitude, \
         'altitude': args.altitude, \
         'longitude': args.longitude, \
         'irlock_beacon_pose': args.irlock_beacon_pose, \
         'world_name': args.world_name, \
         'model_pose': args.model_pose, \
         'model_name': args.model_name, \
         'ode_threads': args.ode_threads}

    result = template.render(d)
    if args.output_file:
        filename_out = args.output_file
    else:
        filename_out = '{:s}/temp_{:s}.world'.format(default_world_path,args.world_name)

    with open(filename_out, 'w') as f_out:
        print(('{:s} -> {:s}'.format(default_filename, filename_out)))
        f_out.write(result)
