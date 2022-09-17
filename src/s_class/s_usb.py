import pyvisa
from dataclasses import dataclass
import numpy


class dev_find:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()


    def find_all_devices(self):
        ld = self.rm.list_resources()
        return ld


class dev_command:
    def __init__(self, dev):
        rm = pyvisa.ResourceManager()
        self.dev = rm.open_resource(dev)
        self.dd = self.dev.query("*IDN?")
        print(f"Connecting to {self.dd}")

    def send_data(self, d):
        pass

    def recv_data(self):
        pass
