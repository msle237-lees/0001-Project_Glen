import pyvisa
from dataclasses import dataclass
import numpy


class dev_connect:
    def __init__(self):
        self.rm = pyvisa.ResourceManager('@py')


    def find_all_devices(self):
        ld = self.rm.list_resources()
        return ld


    def find_device_data(self):
        dd = self.dev.query("*IDN?")
        return dd


    def open_device(self, dev):
        self.dev = self.rm.open_resource(dev)


    def send_data(self, d):
        pass


    def recv_data(self):
        pass
