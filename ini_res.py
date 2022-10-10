from configparser import ConfigParser
import datetime as dt


class Ini:

    """ Get / Set section & param from specified ini file.
    With possible reading/writing errors logging to specified log-file."""

    def __init__(self):

        self.ini = ConfigParser()
        self.now = dt.datetime.now()
        self.log_name = 'logfile.log'
        self.ini_name = 'inifile.ini'

    def get(self, section: str, param: str):

        """ Get ini parameter meaning. Params: self.log_name: name of log if errors, self.ini_name: ini file name,
            section: ini section name, param: ini parameter name. """

        try:
            self.ini.read(self.ini_name)
            data = self.ini[section][param]

        except Exception as Argument:
            with open(self.log_name, "a") as log_file:
                log_file.write(f"\n{self.now}: {self.ini_name} read error. Message:{str(Argument)}")
        else:
            return data

    def set(self, section: str, param: str, data: str):

        """ Set ini section or parameter meaning. Params: log: name of log if errors, ini: ini file name,
            section: ini section name, param: ini parameter name, data: parameter meaning. """

        self.ini.read(self.ini_name)
        self.ini.set(section, param, data)

        with open(self.ini_name, 'w') as ini_file:
            self.ini.write(ini_file)
