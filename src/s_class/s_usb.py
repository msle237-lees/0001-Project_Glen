import pyvisa
import numpy


class device:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()

    def Detect(self):
        self.ld = self.rm.list_resources()
        return self.ld

    def Connect(self, HWID):
        self.HWID = HWID
        self.dev = self.rm.open_resource(self.HWID)
        print(f"Connecting to {self.dev}")

    def Send_command(self, cmd):
        self.ret = self.dev.query(cmd)
        return self.ret

    def Frequency_set(self, freq):
        pass

    def Vpp_set(self, vpp_val):
        pass

    def DcOffset_set(self, dcoffset_val):
        pass

    def Phase_set(self, dcphase_val):
        pass

    def V_div_set(self, V_div_set):
        pass
