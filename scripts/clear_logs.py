import os

from config.settings.base import LOGS_DIR

if __name__ == '__main__':
    log_files = ['error.log', 'warning.log']

    for log_file in log_files:
        log_file = os.path.join(LOGS_DIR, log_file)

        with open(log_file, 'wt') as f:
            f.write('')
