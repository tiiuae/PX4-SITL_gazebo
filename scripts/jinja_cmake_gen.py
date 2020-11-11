#!/usr/bin/env python3
import jinja2
import argparse
import os
import fnmatch
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="file that the sdf file should be generated from")
    parser.add_argument('env_dir')
    args = parser.parse_args()
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(args.env_dir))
    template = env.get_template(os.path.relpath(args.filename, args.env_dir))

    try:
        import rospkg
        rospack = rospkg.RosPack()
    except ImportError:
        pass
        rospack = None

    d = {'np': np, 'rospack': rospack, \
         'sdf_version': "NotSet", \
         'mavlink_tcp_port': 4560, \
         'mavlink_udp_port': 14560, \
         'serial_enabled': 0, \
         'serial_device': "/dev/ttyACM0", \
         'serial_baudrate': 921600, \
         'enable_lockstep': 1, \
         'model_name': "NotSet", \
         'hil_mode': 0}

    result = template.render(d)
    filename_out = args.filename.replace('.sdf.jinja', '.sdf')

    with open(filename_out, 'w') as f_out:
        print(('{:s} -> {:s}'.format(args.filename, filename_out)))
        f_out.write(result)
