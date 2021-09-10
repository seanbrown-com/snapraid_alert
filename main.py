from snapraid_check import SnapraidCheck
from smtp_email import SmtpEmail
from config_reader import ConfigReader
import sys


def run(config_file, command='sync'):
    config_reader = ConfigReader(config_file)
    config_reader.read_configs()
    email = SmtpEmail(config_reader.sender_email, config_reader.destination_email, config_reader.server,
                      config_reader.port, config_reader.password, command, config_reader.log_path)
    checker = SnapraidCheck(config_reader.log_path)
    result, message = checker.sync_check()
    if not result:
        email.send_email(message)
        print('email sent')
    else:
        print('snapraid did its thing')


if __name__ == '__main__':
    args = sys.argv
    cfg = None
    cmd = None
    if len(args) > 1:
        cfg = args[1]
    else:
        print('no config file found')
        exit(1)
    if len(args) > 2:
        cmd = args[2]
        run(cfg, cmd)
    else:
        run(cfg)
    exit(0)

