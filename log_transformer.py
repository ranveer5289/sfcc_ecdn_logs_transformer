#!/usr/bin/python3
"""This module is responsible for transforming SFCC E-CDN log files to standard log formats"""
import sys
import argparse

from helper import get_all_log_files
from formats.w3c import W3C

def start():
    """
    Transform SFCC E-CDN log files to standard log formats
    """
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-i', dest='input', type=str,
                           help="Existing Input directory from which SFCC logs file will be read")
    my_parser.add_argument('-o', dest='output', type=str,
                           help="Existing Output directory to which \
                           transformed logs will be written")
    my_parser.add_argument('-f', dest='format', help="Output log format. Eg: apache, w3c")
    my_parser.add_argument('-s', dest='strip', action='store_true',
                           help="SFCC cache fingerprint will be removed from URL")


    args = my_parser.parse_args()

    if not args.input:
        my_parser.error('Logs input directory not specified')
    if not args.output:
        my_parser.error('Logs output directory not specified')
    if not args.format:
        my_parser.error('Format not specified')

    # Get all *.log files from the specified directory input path
    log_files = get_all_log_files(args.input)

    if len(log_files) <= 0:
        print('No log files found in the folder')
        sys.exit(0)

    transformer = None
    if args.format == 'w3c':
        transformer = W3C(args.output, args.strip)
    else:
        print('format not supported')
        sys.exit(0)

    transformer.transform(log_files)

if __name__ == '__main__':
    start()
