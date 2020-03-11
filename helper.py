"""Helper Utility module"""
import os
import fnmatch
import re


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
