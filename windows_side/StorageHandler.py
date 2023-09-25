from pathlib import Path
from datetime import datetime
import os

LOG_ENABLED = False

def parse_file_name(subject_number, experiment_mode, trial_number):
    current_date_time = datetime.now()
    n = str()
    n = n + subject_number + "_"
    n = n + experiment_mode + "_"
    n = n + trial_number + "_"

    n = n + modify_date_time_vars(current_date_time.year) + "_"
    n = n + modify_date_time_vars(current_date_time.month) + "_"
    n = n + modify_date_time_vars(current_date_time.day) + "__"
    n = n + modify_date_time_vars(current_date_time.hour) + "_"
    n = n + modify_date_time_vars(current_date_time.minute) + "_"
    n = n + modify_date_time_vars(current_date_time.second)
    return n


def modify_date_time_vars(var):
    '''
    to force all variables have 2 digits (for names of the logged files)
    '''
    if (var < 10):
        return str(0) + str(var)
    else:
        return str(var)


class StorageHandler():
    def __init__(self, rel_parent_dir, subject_number, trial_number) -> None:
        self.rel_parent_dir_ = rel_parent_dir
        self.subject_number_ = subject_number
        self.trial_number_ = trial_number
        self.absolute_log_path_ = ""
        self.fn_ = parse_file_name(self.subject_number_,
                                   self.experiment_mode_, self.trial_number_)
        self.create_the_log_directory()

    def create_the_log_directory(self):
        path = str(Path.home())
        tmp = self.rel_parent_dir_.split("\\")
        for word in range(len(tmp)):
            path = os.path.join(path, str(tmp[word]))
        try:
            if (not os.path.exists(path)):
                os.makedirs(path)
            print(f"[OK] Directory {path} is created")
            self.absolute_log_path_ = path
        except:
            print(f"[EXCEPTION]: directory {path} cannot be created (or already exists)!")
            os._exit(0)
