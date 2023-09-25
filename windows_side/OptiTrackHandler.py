from NatNetPythonClient.NatNetClient import NatNetClient
from threading import Thread
import time
import os
from StorageHandler import *


class OptiTrackHandler(Thread):
    def __init__(self, client_ip_address="127.0.0.1", server_ip_address="127.0.0.1",
                 use_multicast=True, is_log_enabled=False, q=None, storage_pars=None):

        Thread.__init__(self)
        self.setup_opti_track(client_ip_address, server_ip_address, use_multicast)
        self.is_log_enabled_ = is_log_enabled
        self.time_stamp_ = 0
        self.rigid_body_count_ = 0
        self.new_frame_received_ = False
        self.previous_time_ = 0.0
        self.q_ = q

        self.counter_ = 0
        self.rigid_body_data_ = list()
        self.str_rigid_body_data_ = str()
        self.storage_pars_ = storage_pars

        if (storage_pars[0] == "record_data_locally"):
            self.storage_handler_ = StorageHandler(storage_pars[1], storage_pars[2], storage_pars[3])

    def shut_down(self):
        self.client_.shutdown()

    def setup_opti_track(self, client_ip_address, server_ip_address, use_multicast):
        options = dict()
        options["client_ip_address"] = client_ip_address
        options["server_ip_address"] = server_ip_address
        options["use_multicast"] = use_multicast
        self.client_ = NatNetClient()
        self.client_.set_print_level(0)
        self.client_.set_client_address(options["client_ip_address"])
        self.client_.set_server_address(options["server_ip_address"])
        self.client_.set_use_multicast(options["use_multicast"])
        self.client_.new_frame_listener = self.receive_new_frame
        self.client_.rigid_body_listener = self.receive_rigid_body_frame

    def run(self):
        is_running = self.client_.run()
        if not is_running:
            print("[ERROR] - OptiTrack: Could not start streaming client.")
            try:
                os._exit(0)
            except SystemExit:
                print("...")
            finally:
                print("[EXIT] - OptiTrackHandler")
        time.sleep(1.5)

        if self.client_.connected() is False:
            print("[ERROR] - OptiTrackHandler: Could not connect properly. Check that Motive streaming is on.")
            try:
                os._exit(0)
            except SystemExit:
                print("...")
            finally:
                print("[EXIT] - OptiTrackHandler")
        print("[OK] - OptiTrackHandler: Up and Running...")
        self.previous_time_ = time.time()

    def receive_new_frame(self, data_dict):
        self.time_stamp_ = data_dict['timestamp']
        self.rigid_body_count_ = data_dict['rigid_body_count']
        if (not self.new_frame_received_):
            self.new_frame_received_ = True
        self.log_print("data_dict", data_dict)

    def receive_rigid_body_frame(self, new_id, position, rotation):

        if (self.new_frame_received_):
            if (self.counter_ < self.rigid_body_count_):

                if (self.counter_ == 0):
                    self.rigid_body_data_.append(self.time_stamp_)
                    self.rigid_body_data_.append(self.rigid_body_count_)

                self.rigid_body_data_.append(new_id)
                self.rigid_body_data_.append(position[0])
                self.rigid_body_data_.append(position[1])
                self.rigid_body_data_.append(position[2])
                self.rigid_body_data_.append(rotation[0])
                self.rigid_body_data_.append(rotation[1])
                self.rigid_body_data_.append(rotation[2])
                self.rigid_body_data_.append(rotation[3])

                self.counter_ = self.counter_ + 1

            else:
                self.q_.put(str(self.rigid_body_data_))
                if (self.storage_pars_[0] == "record_data_locally"):
                    while (not self.q_.empty()):
                        row = self.q_.get()
                        # Send data to the storage handler
                        self.q_.task_done()

                self.log_print("queue", str(self.rigid_body_data_))
                self.rigid_body_data_.clear()
                self.counter_ = 0

    def log_print(self, msg, value):
        if (self.is_log_enabled_):
            print(f"{msg}:\n", value)
            print("\n")

