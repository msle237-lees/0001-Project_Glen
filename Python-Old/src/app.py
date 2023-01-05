# Custom module imports
from src.s_class.s_usb import device


def run():
    d1 = device()
    d2 = device()
    # 0. Detect Test Equipment
    dev_list = d1.Detect()
    # print(dev_list)

    # 1. Connect to Test Equipment
    devices = []
    for i in range(len(dev_list)):
        devices.append([i, dev_list[i]])
    print(devices)
    dev1 = int(input("Enter device 1 (Signal Gen) UUID (0 or 1): "))
    d1.Connect(devices[dev1][1])
    dev2 = int(input("Enter device 2 (Oscilloscope) UUID (0 or 1): "))
    d2.Connect(devices[dev2][1])

    # 2. Configure Channels on Signal Generator
    channel_num_signal_gen = int(input("Enter number of channels used on signal generator (1 or 2): "))
    if channel_num_signal_gen == 1:
        d1.Send_command("CHAN1:OUTPUT\s1")
        d1.Send_command("CHAN2:OUTPUT\s0")
    else:
        d1.Send_command("CHAN1:OUTPUT\s1")
        d1.Send_command("CHAN2:OUTPUT\s1")

    # 3. Configure Channels on Oscilloscope
    channel_num_osc = int(input("Enter number of channels used on oscilloscope (1 or 2): "))
    if channel_num_osc == 1:
        d2.Send_command("CHAN1:OUTPUT\s1")
        d2.Send_command("CHAN2:OUTPUT\s0")
    else:
        d2.Send_command("CHAN1:OUTPUT\s1")
        d2.Send_command("CHAN2:OUTPUT\s1")

    # 4. Collect user input:
    print("Signal Generator Settings: ")
    print("\tChannel 1: ")
    sig_channel_1_wave_type = input("\t\tEnter wave type (SIN, SQU, RAMP, PULS, NOIS, ARB, DC): ")
    sig_channel_1_freq_start = float(input("\t\tEnter starting frequency (Hz): "))
    sig_channel_1_freq_stop = float(input("\t\tEnter ending frequency (Hz): "))
    sig_channel_1_freq_step = int(input("\t\tEnter number of data points (int): "))
    sig_channel_1_amp = float(input("\t\tEnter amplitude (Vpp): "))
    sig_channel_1_dc_offset = float(input("\t\tEnter DC offset (V): "))

    print("Oscilloscope Settings: ")
    print("\tChannel 1: ")
    osc_channel_1_volts = float(input("\t\tEnter Volts (V): "))
    osc_channel_1_v_div = float(input("\t\tEnter Volts per division (V): "))
    osc_channel_1_measure = input("\t\tEnter measurement parameters seperated by a comma (Vpp, Phase, ...): ")
    if channel_num_osc == 1:
        pass
    else:
        print("\tChannel 2: ")
        osc_channel_2_volts = float(input("\t\tEnter Volts (V): "))
        osc_channel_2_v_div = float(input("\t\tEnter Volts per division (V): "))
        osc_channel_2_measure = input("\t\tEnter measurement parameters seperated by a comma (Vpp, Phase, ...): ")

    # 5. Run src.app.calculate_frequency_list() function
    
    # 5.1 Run src.app.determine_wave_type() function with b_wave as argument

    # 6. Send SPCI Commands to machines
    # 6.1 Call for s_usb.wave_type_set() function
    # :CHANnel<n>:BASE:WAVe { SINe | SQUare | PULSe | RAMP | ARB | NOISe | DC }


    # 6.2 Call for s_usb.frequency_set() function
    # :CHANnel<n>:BASE:FREQuency {<freq>}

    # 6.3 Call for s_usb.Vpp_set() function
    # :CHANnel<n>:BASE:AMPLitude { <amp>}

    # 6.4 Call for s_usb.DcOffset_set() function

    # 6.5 Call for s_usb.phase_set() function

    # 6.6 Call for s_usb.V_div_set() function

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
