# main program
from src.s_class.s_usb import dev_find, dev_command


dev = []
num_of_dev = 0

def run():
	d = dev_find()
	ld = d.find_all_devices()
	print(ld)
	for i in ld:
		if "USB" in i:
			num_of_dev += 1
	if num_of_dev == 2:
		sig_gen_code = input("Enter device code to connect to Signal Generator: ")
		os_code = input("Enter device code to connect to Oscilloscope: ")
		dev.append(dev_command(sig_gen_code))
		dev.append(dev_command(os_code))
	elif num_of_dev == 1:
		sig_gen_code = input("Enter device code to connect to Signal Generator: ")
		dev.append(dev_command(sig_gen_code))
