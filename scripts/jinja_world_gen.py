#!/usr/bin/env python3

"""
Generate Worlds

@author: Benjamin Perseghetti
"""

import jinja2
import argparse
import os
import fnmatch
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', help="file that the sdf file should be generated from")
    parser.add_argument('--env_dir')
    parser.add_argument('--sun_model', default="sun_2", help="Select sun model [sun, sun_2, NoSun]")
    parser.add_argument('--cloud_speed', default="NoClouds", help="Turn on clouds with given speed")
    parser.add_argument('--shadows', default=1, help="Shadows on [1] or off [0]")
    parser.add_argument('--video_widget', default="NotSet", help="GUI video widget on [1] or off [0]")
    parser.add_argument('--update_rate', default=250, help="Real time update rate.")
    parser.add_argument('--wind_speed', default="NotSet", help="Turn on wind with given mean speed.")
    parser.add_argument('--realtime_factor', default=1.0, help="Real time factor.")
    parser.add_argument('--world_name', default="empty", help="Name of world [empty, mcmillan, ksql, irlock, boat, baylands, yosemite, windy, warehouse, typhoon, raceway]")
    parser.add_argument('--ambient_light', default=0.95, help="Value for ambient light [0.0..1.0]")
    parser.add_argument('--background_light', default=0.3, help="Value for background light [0.0..1.0]")
    parser.add_argument('--spherical_coords', default="NotSet", help="Enable or disable spherical coordinates on [1] or off [0]")
    parser.add_argument('--latitude', default=39.8039, help="Latitude for spherical coordinates")
    parser.add_argument('--longitude', default=-84.0606, help="Longitude for spherical coordinates")
    parser.add_argument('--altitude', default=244, help="Altitude for spherical coordinates")
    parser.add_argument('--model_name', default="NotSet", help="Model to be used in jinja files")
    parser.add_argument('--output-file', help="sdf output file")
    parser.add_argument('--ode_threads', default=2, help="Number of island threads to use for ODE.")
    args = parser.parse_args()
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(args.env_dir))
    template = env.get_template(os.path.relpath(args.filename, args.env_dir))

    # create dictionary with useful modules etc.
    try:
        import rospkg
        rospack = rospkg.RosPack()
    except ImportError:
        pass
        rospack = None

    d = {'np': np, 'rospack': rospack, \
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
         'world_name': args.world_name, \
         'model_name': args.model_name, \
         'ode_threads': args.ode_threads}

    result = template.render(d)
    if args.output_file:
        filename_out = args.output_file
    else:
        filename_out = args.filename.replace('.sdf.jinja', '.sdf')

    with open(filename_out, 'w') as f_out:
        print(('{:s} -> {:s}'.format(args.filename, filename_out)))
        f_out.write(result)
