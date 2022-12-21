import pyvisa as pyv
import asyncio as aio
from time import perf_counter

class CI_app:
    def __init__(self):
        # Initialize the pyvisa resource manager
        self.rm = pyv.ResourceManager()

        # List all the devices connected to the computer
        self.devices = self.rm.list_resources()
        dev_list = []
        for i in range(len(self.devices)):
            dev_list.append([i, self.devices[i]])
        print(dev_list)

        # Ask the user to select the oscilloscope and signal generator
        self.oscilloscope = int(input("Enter the oscilloscope number (0 or 1): "))
        self.signal_generator = int(input("Enter the signal generator number (0 or 1): "))

        # Connect to the oscilloscope and signal generator
        self.osc = self.rm.open_resource(dev_list[self.oscilloscope][1], write_termination = '\n', read_termination='\n')
        self.sig = self.rm.open_resource(dev_list[self.signal_generator][1], write_termination = '\n', read_termination='\n')

    def run(self):
        while True:
            # Ask user for command to send and to which device
            q = int(input("Quit? (0 or 1 == No or Yes): "))

            if q == 1:
                quit()

            self.cmd = input("Enter the command to send: ")
            self.dev = int(input("Enter the device number (0 for oscilloscope, 1 for signal generator): "))
            self.option = int(input("Query or Read (0 or 1): "))

            # Send the command to the device
            time_before = perf_counter()
            if self.dev == 0 and self.option == 0:
                self.resp = self.osc.query(self.cmd)
            elif self.dev == 1 and self.option == 0:
                self.resp = self.sig.query(self.cmd)
            elif self.dev == 0 and self.option == 1:
                self.resp = self.osc.write(self.cmd)
            elif self.dev == 1 and self.option == 1:
                self.resp = self.osc.write(self.cmd)
            print(f"Response: {self.resp} in {perf_counter() - time_before} seconds")

ci = CI_app()
if __name__ == "__main__":
    ci.run()

