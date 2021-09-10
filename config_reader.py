import configparser


class ConfigReader:
    def __init__(self, config_file):
        self.config_file = config_file
        self.destination_email = None
        self.sender_email = None
        self.server = None
        self.port = None
        self.password = None
        self.log_path = None

    def read_configs(self):
        config = configparser.RawConfigParser()
        config.read(self.config_file)
        self.destination_email = config.get('Snapraid Alert Configs', 'destination_email')
        self.sender_email = config.get('Snapraid Alert Configs', 'sender_email')
        self.server = config.get('Snapraid Alert Configs', 'server')
        self.port = int(config.get('Snapraid Alert Configs', 'port'))
        self.password = config.get('Snapraid Alert Configs', 'password')
        self.log_path = config.get('Snapraid Alert Configs', 'log_path')

    @property
    def destination_email(self):
        return self._destination_email

    @destination_email.setter
    def destination_email(self, value):
        self._destination_email = value

    @property
    def sender_email(self):
        return self._sender_email

    @sender_email.setter
    def sender_email(self, value):
        self._sender_email = value

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, value):
        self._server = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def log_path(self):
        return self._log_path

    @log_path.setter
    def log_path(self, value):
        self._log_path = value
