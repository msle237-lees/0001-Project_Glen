import pyvisa
import numpy


class device:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()

    def detect(self):
        self.ld = self.rm.list_resources()
        return self.ld

    def connect(self, HWID):
        self.HWID = HWID
        self.dev = self.rm.open_resource(self.HWID)
        print(f"Connecting to {self.dev}")

    def send_command(self, cmd):
        self.ret = self.dev.query(cmd)
        return self.ret
