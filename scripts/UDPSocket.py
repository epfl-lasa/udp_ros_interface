#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Class file for UDPSocket
# license removed for brevity
# Maintainers:
#   - Soheil Gholami (soheiil.gholamii@gmail.com)
#   - Louis Munier (lmunier@protonmail.com)
# Update: 2023-09-25

import socket
from dependencies import *


import socket
import time
from threading import Thread

class UDPSocket(Thread):
    """
    A class representing a UDP socket.

    Attributes:
    -----------
    role_ (str): The role of the socket.
    udp_socket_ (socket.socket): The UDP socket object.
    ip_address_ (str): The IP address of the socket.
    port_number_ (int): The port number of the socket.
    buffer_size_ (int): The buffer size of the socket.
    received_packet_ (str): The last received packet.
    update_rate_ (float): The update rate of the socket.
    is_log_enabled_ (bool): Whether logging is enabled or not.
    q_ (queue.Queue): The queue to put received packets in.
    """

    def __init__(self, role=None,
                 ip_address="127.0.0.1", port_number=20001, buffer_size=1024,
                 update_rate=0.05, is_log_enabled=False, q=None):
        """
        Initializes a new instance of the UDPSocket class.

        Args:
            role (str, optional): The role of the socket.
            ip_address (str, optional): The IP address of the socket.
            port_number (int, optional): The port number of the socket.
            buffer_size (int, optional):  The buffer size of the socket.
            update_rate (float, optional): The update rate of the socket.
            is_log_enabled (bool, optional): Whether logging is enabled or not.
            q (queue.Queue, optional): The queue to put received packets in.
        """
        Thread.__init__(self)
        self.role_ = role
        self.udp_socket_ = None
        self.ip_address_ = ip_address
        self.port_number_ = port_number
        self.buffer_size_ = buffer_size
        self.received_packet_ = None
        self.update_rate_ = update_rate
        self.is_log_enabled_ = is_log_enabled
        self.q_ = q
        self.init_udp_socket()

    def init_udp_socket(self):
        """
        Initializes the UDP socket.
        """
        self.ip_address_and_port_number_ = (self.ip_address_,
                                            self.port_number_)
        self.udp_socket_ = socket.socket(family=socket.AF_INET,
                                         type=socket.SOCK_DGRAM)

    def bind(self):
        """
        Binds the UDP socket to the IP address and port number.
        """
        try:
            self.udp_socket_.bind(self.ip_address_and_port_number_)
            print("[OK] UDPSocket - bounded!")
        except:
            print("[EXCEPTION] UDPSocket - bind()")

    def connect(self):
        """
        Connects the UDP socket to the IP address and port number.
        """
        try:
            self.udp_socket_.connect(self.ip_address_and_port_number_)
            print("[OK] UDPSocket - connected!")
        except:
            print("[EXCEPTION] UDPSocket - connect()")

    def send_udp_packet(self, msg):
        """
        Sends a UDP packet.

        Args:
            msg (str): The message to send.
        """
        try:
            if (self.is_log_enabled_):
                print(
                    f"[{self.role_}] sending ({msg}) to {self.ip_address_and_port_number_}")
            self.udp_socket_.sendto(str.encode(msg),
                                    self.ip_address_and_port_number_)
        except:
            print("[EXCEPTION] UDPSocket - send_udp_packet()")

    def receive_udp_packet(self):
        """
        Receives a UDP packet.

        Returns:
            bool: True if a packet was received, False otherwise.
        """
        try:
            bytes_address_pair = self.udp_socket_.recvfrom(self.buffer_size_)
            message = ""
            message = bytes_address_pair[0]
            address = ""
            address = bytes_address_pair[1]
            if (message):
                self.received_packet_ = message.decode()
                if (self.is_log_enabled_):
                    print(
                        f"[{self.role_}] received message from: {address} is\n>> {message}")
                return True
            else:
                return False
        except:
            print("[EXCEPTION] UDPSocket - receive_udp_packet()")

    def get_received_packet(self):
        """
        Gets the last received packet.

        Returns:
            str: The last received packet.
        """
        return self.received_packet_

    def run(self):
        """
        The main loop of the thread.
        """
        while True:
            if (self.receive_udp_packet()):
                self.q_.put(self.get_received_packet())
            time.sleep(self.update_rate_)
