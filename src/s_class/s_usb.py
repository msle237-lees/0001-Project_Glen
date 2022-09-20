import pyvisa
import numpy


'''
Sig Gen:
    Chan 1:
        Type: Sine wave
        Frequency: Sweep from 1kHz to 100kHz
        Amplitude: 200mVpp
        DC Offset 2.5V

    Chan 2:
        Type: Square
        Amplitude: 2.5V
        DC Offset: 1.25V
OSCOPE:
    Chan 1:
        Volts/Div: 200mV
        Horizontal time divisions: ????
        Measure: Vpp, Phase

    Chan 1:
        Volts/Div: 200mV
        Horizontal time divisions: ????
        Measure: Vpp, Phase
    Hor div: 5ms
    CHAN1 Volts/div: 2V (Chan 1 is output)
    CHAN2 Volts/div: 200mV (Chan 2 is input)
'''

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
