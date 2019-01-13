from datetime import datetime

"""
# Logger 
# :Author Daniel Svens
"""


class Logger:

    def __init__(self, logfile):
        self.file = logfile

    def debug(self, msg):
        date_now = datetime.today().strftime('%d-%m-%Y %H:%M:%S')

        with open(self.file, 'a') as f:
            f.write('DEBUG: {} | {}\n'.format(date_now, msg))

    def info(self, msg):
        date_now = datetime.today().strftime('%d-%m-%Y %H:%M:%S')

        with open(self.file, 'a') as f:
            f.write('INFO: {} | {}\n'.format(date_now, msg))

    def warn(self, msg):
        date_now = datetime.today().strftime('%d-%m-%Y %H:%M:%S')

        with open(self.file, 'a') as f:
            f.write('WARN: {} | {}\n'.format(date_now, msg))

    def critical(self, msg):
        date_now = datetime.today().strftime('%d-%m-%Y %H:%M:%S')

        with open(self.file, 'a') as f:
            f.write('CRITICAL: {} | {}\n'.format(date_now, msg))

    def console(self, msg):
        date_now = datetime.today().strftime('%H:%M:%S')

        with open(self.file, 'a') as f:
            f.write('{}: {}\n'.format(date_now, msg))
