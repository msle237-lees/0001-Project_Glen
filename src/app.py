# Custom module imports
from src.s_class.s_usb import device


def calculate_frequency_list(f_max, f_max_unit, f_min, f_min_unit, f_incr, f_incr_unit):
    # 5.1 f_list = empty list
    f_list = []

    # 5.2 determine how many zeros to add to f_max, f_min, f_incr_val
    # mV, V, kHz, degrees
    if 'k' in f_max_unit:
        f_max = f_max * 1000
    if 'k' in f_min_unit:
        f_min = f_min * 1000
    if 'k' in f_incr_unit:
        f_incr = f_incr * 1000

    # 5.3 f_num_of_runs = (f_max - f_min) / f_incr_val
    f_num_of_runs = (f_max - f_min) / f_incr

    # 5.4 for i in range(0, f_num_of_runs):
    for i in range(0, f_num_of_runs):
        # 5.4.1 f_list.append(f_min + f_incr_val)
        f_list.append(f_min + f_incr_val)

    # 5.5 return f_list
    return f_list

def run():
    d1 = device()
    d2 = device()
    # 0. Detect Test Equipment
    dev_list = d1.Detect()
    print(dev_list)

    # 1. Connect to Test Equipment
    dev1 = input("Enter device 1 (Signal Gen) UUID: ")
    d1.Connect(dev1)
    dev2 = input("Enter device 2 (Oscilloscope) UUID: ")
    d2.Connect(dev2)

    # 2. Configure Channels on Signal Generator
    channel_num_signal_gen = int(input("Enter number of channels used on signal generator (1 or 2): "))
    if channel_num_signal_gen == 1:
        d1.Send_command(":CHANnel<1>:OUTPut {1}")
        d1.Send_command(":CHANnel<2>:OUTPut {0}")
    else:
        d1.Send_command(":CHANnel<1>:OUTPut {1}")
        d1.Send_command(":CHANnel<2>:OUTPut {1}")

    # 3. Configure Channels on Oscilloscope

    # 4. Collect user input:
    print("Enter answers for the questions that show up: ")

    # 4.1 Ask for Starting Frequency
    f_start = int(input("Enter starting frequency: "))

    # 4.2 Ask for Starting Frequency Unit of Measure
    f_start_unit = input("Enter starting frequency unit of measure: ")

    # 4.3 Ask for Ending Frequency
    f_end = int(input("Enter ending frequency: "))

    # 4.4 Ask for Ending Frequency Unit of Measure
    f_end_unit = input("Enter ending frequency unit of measure: ")

    # 4.5 Ask for Frequency Incrementation Value
    f_incr = int(input("Enter frequency increment value: "))
    f_incr_unit = input("Enter frequency increment value unit of measure: ")

    # 4.6 Ask for Vpp Value
    vpp_val = int(input("Enter Vpp value: "))
    vpp_unit = input("Enter Vpp value unit of measure: ")

    # 4.7 Ask for Offset Value
    offset_val = int(input("Enter offset value: "))
    offset_unit = input("Enter offset value unit of measure: ")

    # 4.8 Ask for Phase Value
    dcphase_val = int(input("Enter DC Phase value: "))
    dcphase_unit = input("Enter DC Phase value unit of measure: ")

    # 4.9 Ask for Oscilloscope Channel 1 V/div
    chann_1_v_div_val = int(input("Enter V/Div value for channel 1: "))
    chann_1_v_div_unit = input("Enter V/Div value unit of measure for channel 1: ")

    # 4.10 Ask for Oscilloscope Channel 2 V/div
    chann_2_v_div_val = int(input("Enter V/Div value for channel 2: "))
    chann_2_v_div_unit = input("Enter V/Div value unit of measure for channel 2: ")

    # 5. Run src.app.calculate_frequency_list() function
    print(calculate_frequency_list(f_end, f_end_unit, f_start, f_start_unit, f_incr, f_incr_unit))
    
    # 6. Send SPCI Commands to machines

    # 6.1 Call for s_usb.dev_command.frequency_set() function

    # 6.2 Call for s_usb.dev_command.Vpp_set() function

    # 6.3 Call for s_usb.dev_command.DcOffset_set() function

    # 6.4 Call for s_usb.dev_command.phase_set() function

    # 6.5 Call for s_usb.dev_command.V_div_set() function

    # 7. Call for src.app.run_data_gather() function

    # 7.1 data_list = empty list

    # 7.2 for i in range(0, f_num_of_runs):

    # 7.2.1 data_point = [0, 0]

    # 7.2.1 write signal generator to send f_list[i]

    # 7.2.2 data_point[0] = read oscilloscope channel 1 to recv data

    # 7.2.3 data_point[1] = read oscilloscope channel 2 to recv data

    # 7.2.4 data_list.append(data_point)

    # 7.3 return data_list

    # 8. Call for src.app.calc_data_points() function

    # 8.1 take in data_list

    # 8.2 plot_data = empty list

    # 8.3 for i in range(len(data_list)):

    # 8.3.1 plot_data.append(data_list[i][0]/data_list[i][1])

    # 8.4 return plot_data

    # 9. Call for src.app.cvt_log_scale() function

    # 9.1

    # 10. Call for src.app.plot_data_points() function

    # 10.1

    # 11. Call export plot_graph() function

    # 11.1
