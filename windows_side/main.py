from dependencies import *


def signal_handler(sig, frame):
    # what to do when 'ctrl+c' is pressed
    print(Fore.RED + ">> You pressed Ctrl+C!" + Style.RESET_ALL)
    os._exit(0)


if __name__ == "__main__":

    # how to end the program, triggered by "ctrl+c"
    signal.signal(signal.SIGINT, signal_handler)

    tmp = read_yaml_config_file()
    subject_number = tmp[0]
    experiment_trial = tmp[1]
    data_transmission_mode = tmp[2]
    rel_parent_dir = tmp[3]

    storage_pars = (data_transmission_mode, rel_parent_dir, subject_number, experiment_trial)

    # create the OptiTrack handler to get data from its software
    q_opti_track = queue.Queue()
    thrd_opti_track_handler = OptiTrackHandler(OPTI_TRACK_CLIENT_IP, OPTI_TRACK_SERVER_IP,
                                               OPTI_TRACK_MULTI_CAST, OPTI_TRACK_LOG_ENABLED,
                                               q_opti_track, storage_pars)
    # thrd_opti_track_handler.setDaemon(True)

    # start the threads
    thrd_opti_track_handler.start()

    # start the main loop
    print(Fore.GREEN + "[STARTED] The main loop!" + Style.RESET_ALL)

    while True:
        time.sleep(MAIN_LOOP_UPDATE_RATE)
