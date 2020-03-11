#!/usr/bin/python3
"""This module is responsible for transforming SFCC E-CDN log files to W3C standard format"""
import json
import os
import sys
import datetime
import argparse

from helper import get_all_log_files
from helper import get_not_cached_url

def transform():
    """
    Transform SFCC E-CDN log files to W3C standard format
    """
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-i', dest='input', type=str,
                           help="Existing Input directory from which SFCC logs file will be read")
    my_parser.add_argument('-o', dest='output', type=str,
                           help="Existing Output directory to which \
                           transformed W3C logs will be written")
    my_parser.add_argument('-s', dest='strip', action='store_true',
                           help="SFCC cache fingerprint will be removed from URL")


    args = my_parser.parse_args()

    if not args.input:
        my_parser.error('Logs input directory not specified')
    if not args.output:
        my_parser.error('Logs output directory not specified')

    # Get all *.log files from the specified directory input path
    log_files = get_all_log_files(args.input)

    if len(log_files) <= 0:
        print('No log files found in the folder')
        sys.exit(0)

    for log_file in log_files:
        # get filename from the file
        filename = os.path.split(log_file)[1]
        w3c_log_file_path = '{}/{}'.format(args.output, 'w3c-log-' + filename)

        # if file already exists with this name remove it
        if os.path.isfile(w3c_log_file_path):
            os.remove(w3c_log_file_path)

        with open(log_file) as f_d:
            with open(w3c_log_file_path, 'w') as w3c_fd:
                w3c_fd.write('#Software: Screaming Frog Log Generator\n')
                w3c_fd.write('#Version: 1.0\n')

                current_date_time = datetime.datetime.now()
                formatted_current_date_time = current_date_time.strftime("%Y-%m-%d %H:%M:%S")
                # #2020-03-11 12:38:00
                w3c_fd.write('#{0}\n'.format(formatted_current_date_time))
                w3c_fd.write('#Fields: date time cs-uri-stem cs-uri-query \
                    cs(User-Agent) sc-status cs-method c-ip cs-host cs-protocol\n')
                for line in f_d:
                    lines = []
                    record = json.loads(line)

                    edge_start_timestamp = record['EdgeStartTimestamp']
                    # nanoseconds to milliseconds
                    timestamp_in_seconds = edge_start_timestamp / 1000000000
                    date_from_timestamp = datetime.datetime.utcfromtimestamp(timestamp_in_seconds)

                    formatted_date = date_from_timestamp.strftime("%Y-%m-%d")
                    lines.append(formatted_date)

                    formatted_time = date_from_timestamp.strftime("%H:%M:%S")
                    lines.append(formatted_time)

                    client_req_uri = record['ClientRequestURI']

                    # if option specified strip the cache fingerprint from the urls
                    if args.strip:
                        client_req_uri = get_not_cached_url(client_req_uri)

                    is_qs = client_req_uri.find('?')

                    uri_stem = client_req_uri
                    uri_query = '-'
                    if is_qs > 0:
                        url_parts = client_req_uri.split('?')
                        if len(url_parts) > 0:
                            uri_stem = url_parts[0]
                            uri_query = url_parts[1]

                    lines.append(uri_stem)
                    lines.append(uri_query)

                    user_agent = record['ClientRequestUserAgent']
                    lines.append('"' + user_agent + '"')

                    response_status = record['EdgeResponseStatus']
                    lines.append(str(response_status))

                    request_method = record['ClientRequestMethod']
                    lines.append(request_method)

                    client_ip = record['ClientIP']
                    lines.append(client_ip)

                    request_host = record['ClientRequestHost']
                    lines.append(request_host)

                    client_protocol = 'https'
                    lines.append(client_protocol)

                    # whitespace delimited line
                    final_line = " ".join(lines)
                    w3c_fd.write(final_line)
                    w3c_fd.write('\n')

if __name__ == '__main__':
    transform()
