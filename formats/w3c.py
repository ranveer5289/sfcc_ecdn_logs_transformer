"""This class is responsible for transforming SFCC E-CDN log files to W3C standard format"""
import datetime
import json
from helper import get_data_from_cdn_logs
from helper import get_output_log_file_path

class W3C:
    """
    Transform SFCC E-CDN log files to W3C standard format
    """
    def __init__(self, output_path, strip):
        self.log_prefix = 'w3c-log-'
        self.output_path = output_path
        self.strip = strip

    def transform(self, log_files):
        """
        Transform all the log files to standard w3c format
        """
        for file in log_files:
            output_path = get_output_log_file_path(self.output_path, file, self.log_prefix)

            with open(file) as f_d:
                with open(output_path, 'w') as w3c_fd:
                    w3c_fd.write('#Software: Screaming Frog Log Generator\n')
                    w3c_fd.write('#Version: 1.0\n')
                    current_date_time = datetime.datetime.now()
                    formatted_current_date_time = current_date_time.strftime("%Y-%m-%d %H:%M:%S")
                    # #2020-03-11 12:38:00
                    w3c_fd.write('#{0}\n'.format(formatted_current_date_time))
                    w3c_fd.write('#Fields: date time cs-uri-stem cs-uri-query \
                        cs(User-Agent) sc-status cs-method c-ip cs-host cs-protocol\n')

                    for line in f_d:
                        record = json.loads(line)
                        lines = get_data_from_cdn_logs(record, self.strip)
                        # whitespace delimited line
                        final_line = " ".join(lines)
                        w3c_fd.write(final_line)
                        w3c_fd.write('\n')
