# main program
from src.s_class.s_usb import dev_connect


def run():
	d = dev_connect()
	print(d.find_all_devices())
	dev = input("Enter device to connect to: ")
	print(d.find_device_data(dev))
