"""Helper Utility module"""
import os
import fnmatch
import re
import datetime


def get_all_log_files(path):
    """
    Get all files with extension .log from the supplied
    directory

    Returns:
        [list] -- [list of all .log files]
    """
    log_files = []
    pattern = '*.log'
    for dirpath, dirnames, filenames in os.walk(path):
        if not filenames:
            continue
        files = fnmatch.filter(filenames, pattern)
        if files:
            for file in files:
                log_files.append('{}/{}'.format(dirpath, file))

    return log_files


def get_not_cached_url(url):
    """
    Get the non-cached version of the url

    Returns:
        [str] -- [non-cached url or return as-is]
    """
    cache_ver_regex_1 = r'(v\d{2,}\/)'
    cache_ver_regex_2 = r'(dw\w+\/)'

    pattern_1 = re.compile(cache_ver_regex_1)
    if pattern_1.search(url):
        url = re.sub(cache_ver_regex_1, '', url)
        return url

    pattern_2 = re.compile(cache_ver_regex_2)
    if pattern_2.search(url):
        url = re.sub(cache_ver_regex_2, '', url)
        return url

    return url

def get_data_from_cdn_logs(record, strip):
    """Collect E-CDN log data in an array

    Returns:
        [list] -- [relevant log data]
    """
    lines = []
    edge_start_timestamp = record['EdgeStartTimestamp']
    # nanoseconds to seconds
    timestamp_in_seconds = edge_start_timestamp / 1000000000
    date_from_timestamp = datetime.datetime.utcfromtimestamp(timestamp_in_seconds)

    formatted_date = date_from_timestamp.strftime("%Y-%m-%d")
    lines.append(formatted_date)

    formatted_time = date_from_timestamp.strftime("%H:%M:%S")
    lines.append(formatted_time)

    client_req_uri = record['ClientRequestURI']

    # if option specified strip the cache fingerprint from the urls
    if strip:
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

    return lines

def get_output_log_file_path(output_path, input_file_path, log_prefix):
    """Get output path where transformed log files will be written

    Arguments:
        output_path {[str]} -- [output path]
        input_file_path {[str]} -- [input path]
        log_prefix {[str]} -- [prefix to append to transformed file like w3c-log-filename.log]

    Returns:
        [str] -- [final output path]
    """
    file_name = os.path.split(input_file_path)[1]
    w3c_log_file_path = '{}/{}'.format(output_path, log_prefix + file_name)

    # if file already exists with this name remove it
    if os.path.isfile(w3c_log_file_path):
        os.remove(w3c_log_file_path)
    return w3c_log_file_path
