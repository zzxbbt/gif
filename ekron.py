#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import glob
import os
import sys

import envoy
# sh changes -ss arg to -ss=arg:
# Unrecognized option '-ss=00:02:10.0'
# Failed to set value '-s' for option '-ss=00:02:10.0'
#import sh


def main():
    parser = argparse.ArgumentParser(description='Create a gif!')
    parser.add_argument('-i', '--file-input', help='Input file',
        required=True)
    parser.add_argument('-o', '--file-output', help='Output file')
    parser.add_argument('-s', '--pos-start', help='Start position',
        required=True)
    parser.add_argument('-e', '--pos-end', help='End position',
        required=True)
    parser.add_argument('-t', '--trim', help='Trim borders?',
        action='store_true', default=True)
    args = vars(parser.parse_args())
    gif(**args)


def remove_frame_files():
    files = glob.glob('/tmp/ekron*.jpg')
    for frame in files:
        os.remove(frame)
    if len(files) > 0:
        remove_frame_files()


def gif(file_input, pos_start, pos_end, file_output=None, fps=12,
        size='hd480', qscale=1, trim=True):
    # In case program was aborted.
    remove_frame_files()

    duration = __calculate_duration(pos_start, pos_end)
    ffmpeg = run('ffmpeg -i %(i)s -r %(r)d -s %(s)s -qscale ' \
        '%(qscale)d -ss %(ss)s -t %(t)s /tmp/ekron%%4d.jpg' \
        % dict(i=file_input, r=fps, s=size, qscale=qscale,
            ss=pos_start, t=str(duration)))

    if trim:
        for frame in glob.glob('/tmp/ekron*.jpg'):
            convert = run('convert %(frame)s -fuzz 15%% -trim ' \
                '+repage %(frame)s' % dict(frame=frame))

    if file_output is None:
        file_output = 'ekron-%(file_input)s-%(pos_start)s-' \
            '%(pos_end)s.gif' % dict(file_input=file_input,
            pos_start=pos_start, pos_end=pos_end)
    convert = run('convert -delay 0 -loop 0 /tmp/ekron*.jpg %s' \
        % file_output)

    remove_frame_files()

    return True


def __calculate_duration(pos_start, pos_end):
    """Calculates duration relative to given start and end positions."""
    date_start = __get_date(pos_start)
    date_end = __get_date(pos_end)
    delta_seconds = (date_end - date_start).total_seconds()
    if delta_seconds <= 0:
        raise ValueError('End position must be after start position!')
    return datetime.datetime.strptime(str(delta_seconds),
        '%S.%f').strftime('%H:%M:%S.%f')


def __get_date(timestring):
    """Timestring would be something like '00:02:25.4'."""
    return datetime.datetime.strptime(timestring, '%H:%M:%S.%f')


def run(commandstring, verbose=False):
    if verbose:
        print commandstring
    command = envoy.run(commandstring)
    if verbose:
        print command.std_out
    if command.status_code is not 0:
        raise Exception('%s failed!\n%s' % \
            (command.command[0], command.std_err))
    return command


if __name__ == '__main__':
    main()

