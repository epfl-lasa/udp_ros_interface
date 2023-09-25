from threading import Thread
from enum import Enum
from colorama import Fore, Style, Back
import queue
import signal
import os
import sys
import time
import yaml

from OptiTrackHandler import OptiTrackHandler
from StorageHandler import *

MAIN_LOOP_UPDATE_RATE = 1.0 / 100.0

# OptiTrack
OPTI_TRACK_CLIENT_IP = "127.0.0.1"
OPTI_TRACK_SERVER_IP = "127.0.0.1"
OPTI_TRACK_MULTI_CAST = True
OPTI_TRACK_LOG_ENABLED = True


def read_yaml_config_file():
    # read parameters from the config file
    with open("config.yaml", "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
        print("[YAML]: config file is read successful")

    subject_number = data[0]['Subject']['subject_number']
    experiment_trial = data[0]['Subject']['experiment_trial']
    rel_parent_dir = data[1]['Storage']['rel_parent_dir']
    data_transmission_mode = data[2]['DataTransmission']['mode']

    print(f"[YAML]: parameters are:\n subject_number: {subject_number}\n experiment_trial: {experiment_trial}\n data_transmission_mode: {data_transmission_mode}\n rel_parent_dir: {rel_parent_dir}")

    return (subject_number, experiment_trial, data_transmission_mode, rel_parent_dir)
