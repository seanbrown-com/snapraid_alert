# using time module
import time

UNIX_TIME_PREFIX = 'unixtime:'
COMMAND_PREFIX = 'command:'
SUCCESS_INDICATOR = 'msg:status: Everything OK'


class SnapraidCheck:
    def __init__(self, log_path):
        self.log_path = log_path

    def check(self, command):
        # current time in seconds
        ts = time.time()
        # time 24 hours ago
        ts_one_day_ago = ts - (60 * 60 * 24)
        runtime_found = False
        command_found = False

        with open(self.log_path, 'r+') as f:
            lines = f.readlines()
            for line in lines:
                if UNIX_TIME_PREFIX in line:
                    exec_time_str = line[len(UNIX_TIME_PREFIX):]
                    exec_time_str = exec_time_str.strip(' \t\n\r')
                    exec_time = int(exec_time_str)
                    if exec_time > ts_one_day_ago:
                        runtime_found = True
                if COMMAND_PREFIX in line:
                    command_run = line[len(COMMAND_PREFIX):]
                    command_run = command_run.strip(' \t\n\r')
                    if command_run == command:
                        command_found = True
                if SUCCESS_INDICATOR in line:
                    if runtime_found and command_found:
                        stripped = line.strip(' \t\n\r')
                        return True, stripped
                    runtime_found = False
                    command_found = False
        if not runtime_found:
            return False, 'No run time for time range found in log'
        if command_found:
            return False, 'No success for time range found in log'
        else:
            return False, 'No command for time range found in log'

    def sync_check(self):
        return self.check('sync')

    def scrub_check(self):
        return self.check('scrub')


def test():
    checker = SnapraidCheck('snapraid.log')
    print(checker.sync_check()[1])


if __name__ == '__main__':
    test()
