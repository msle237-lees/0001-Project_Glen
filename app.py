# TO-DO List
# 1. Using the images that glen sent, create the necessary commands for later
# 2. On each confirm button press, the commands should be sent to their cooresponding machines
# 3. Upload to github for glen to test
# 4. Fix the errors that will pop up

import os
import sys

import numpy as np
import pandas as pd
import PySimpleGUI as sg
import pyvisa as visa

# define the resource manager
global rm
rm = visa.ResourceManager()

class hid_device:
    def __init__(self):
        self.dev = None
        self.dev_list = None
        self.dev_name = None
        self.dev_serial = None
    
    def Detect(self):
        self.dev_list = visa.ResourceManager().list_resources()
        return self.dev_list

    def Connect(self, dev_name):
        self.HWID = dev_name
        self.dev = self.rm.open_resource(self.HWID, write_termination = '\n', read_termination='\n')
        print(f"Connecting to {self.dev}")
    
    def Write_Command(self, command):
        self.dev.write(command)
        return

    def Read_command(self):
        x = self.dev.read()
        return x

    def Query_Command(self, command):
        x = self.dev.query(command) 
        return(x)


def calculate_Frequency(freq_min, freq_min_unit, freq_max, freq_max_unit, freq_step, freq_step_unit):
    freq_list = []
    if freq_min is not None and freq_max is not None and freq_step is not None:
        if freq_min_unit == 'Hz':
            freq_min = int(freq_min)
        elif freq_min_unit == 'kHz':
            freq_min = int(freq_min) * 1000
        elif freq_min_unit == 'MHz':
            freq_min = int(freq_min) * 1000000
        elif freq_min_unit == 'GHz':
            freq_min = int(freq_min) * 1000000000
        if freq_max_unit == 'Hz':
            freq_max = int(freq_max)
        elif freq_max_unit == 'kHz':
            freq_max = int(freq_max) * 1000
        elif freq_max_unit == 'MHz':
            freq_max = int(freq_max) * 1000000
        elif freq_max_unit == 'GHz':
            freq_max = int(freq_max) * 1000000000
        if freq_step_unit == 'Hz':
            freq_step = int(freq_step)
        elif freq_step_unit == 'kHz':
            freq_step = int(freq_step) * 1000
        elif freq_step_unit == 'MHz':
            freq_step = int(freq_step) * 1000000
        elif freq_step_unit == 'GHz':
            freq_step = int(freq_step) * 1000000000

        for i in range(freq_min, freq_max + freq_step, freq_step):
            freq_list.append(i)
    return freq_list

def main():
    sg.theme('Dark')   # Add a touch of color

    # All the stuff inside your window.
    Oscilloscope_Channel_1_Tab = [  [sg.Text('Oscilloscope Channel 1 Settings', size=(30, 1), font=("Helvetica", 20)), sg.Graph(canvas_size=(30, 30), graph_bottom_left=(0, 0), graph_top_right=(30, 30), background_color='yellow', key='-OSC_CH1_GRAPH-')],
                                    [sg.Checkbox('Enable', default=False, size=(25,1), font=("Helvetica", 20), key='-OSC_CH1_ENABLE-')],
                                    [sg.Text('Volts:', size=(15, 1)), sg.InputText(key='-OSC_CH1_VOLTS_IN-'), sg.DropDown(['V', 'mV', 'uV'], size=(5, 1), key='-OSC_CH1_VOLTS_UNIT-')],
                                    [sg.Text('Horizontal Time Division: ', size=(15, 1)), sg.InputText(key='-OSC_CH1_HORZ_TIME_DIV_IN-'), sg.DropDown(['s', 'ms', 'us', 'ns'], size=(5, 1), key='-OSC_CH1_HORZ_TIME_DIV_UNIT-')],
                                    [sg.Text('Measure: ', size=(15, 1)), sg.Checkbox('Vpp', default=False, size=(15,1), key='-OSC_CH1_MEAS_VPP-'), sg.Checkbox('Phase', default=False, size=(15,1), key='-OSC_CH1_MEAS_PHASE-'), sg.Checkbox('Frequency', default=False, size=(15,1), key='-OSC_CH1_MEAS_FREQ-')],
                                    [sg.Text('Acquistion Mode:', size=(15, 1)), sg.DropDown(['Normal', 'Averages', 'Peak', 'Hresolution'], size=(5, 1), key='-OSC_CH1_ACQ_MODE-')],
                                    [sg.Button('Confirm', key='-OSC_CH1_CONFIRM-')]
                                ]
    Oscilloscope_Channel_2_Tab = [  [sg.Text('Oscilloscope Channel 2 Settings', size=(30, 1), font=("Helvetica", 20)), sg.Graph(canvas_size=(30, 30), graph_bottom_left=(0, 0), graph_top_right=(30, 30), background_color='lightblue', key='-OSC_CH2_GRAPH-')],
                                    [sg.Checkbox('Enable', default=False, size=(25,1), font=("Helvetica", 20), key='-OSC_CH2_ENABLE-')],
                                    [sg.Text('Volts:', size=(15, 1)), sg.InputText(key='-OSC_CH2_VOLTS_IN-'), sg.DropDown(['V', 'mV', 'uV'], size=(5, 1), key='-OSC_CH2_VOLTS_UNIT-')],
                                    [sg.Text('Horizontal Time Division: ', size=(15, 1)), sg.InputText(key='-OSC_CH2_HORZ_TIME_DIV_IN-'), sg.DropDown(['s', 'ms', 'us', 'ns'], size=(5, 1), key='-OSC_CH2_HORZ_TIME_DIV_UNIT-')],
                                    [sg.Text('Measure: ', size=(15, 1)), sg.Checkbox('Vpp', default=False, size=(15,1), key='-OSC_CH2_MEAS_VPP-'), sg.Checkbox('Phase', default=False, size=(15,1), key='-OSC_CH2_MEAS_PHASE-'), sg.Checkbox('Frequency', default=False, size=(15,1), key='-OSC_CH2_MEAS_FREQ-')],
                                    [sg.Text('Acquistion Mode:', size=(15, 1)), sg.DropDown(['Normal', 'Averages', 'Peak', 'Hresolution'], size=(5, 1), key='-OSC_CH2_ACQ_MODE-')],
                                    [sg.Button('Confirm', key='-OSC_CH2_CONFIRM-')]
                                ]

    Oscilloscope_Tab = [    [sg.Text('Oscilloscope Settings', justification='left', font=("Helvetica", 20))],
                            [sg.Text('Oscilloscope ID Address: '), sg.DropDown(rm.list_resources(), size=(30, 1), key='-OSC_ID-')],
                            [sg.TabGroup([[sg.Tab('Channel 1', Oscilloscope_Channel_1_Tab, expand_x=True), sg.Tab('Channel 2', Oscilloscope_Channel_2_Tab, expand_x=True)]], size=(1280, 720), key='-OSC_TABGROUP-')]
                        ]

    Signal_Generator_Channel_1_Tab = [  [sg.Text('Signal Generator Channel 1 Settings', size=(30, 1), font=("Helvetica", 20)), sg.Graph(canvas_size=(30, 30), graph_bottom_left=(0, 0), graph_top_right=(30, 30), background_color='red', key='-SG_CH1_GRAPH-')],
                                        [sg.Checkbox('Enable', default=False, size=(25,1), font=("Helvetica", 20), key='-SG_CHAN_1_ENABLE-')],
                                        [sg.Text('Signal Type: '), sg.DropDown(['Sine', 'Square', 'Triangle', 'Ramp', 'Pulse', 'Noise', 'DC'], size=(10, 1), key='-SG_CHAN_1_SIGNAL_TYPE-')],
                                        [sg.Text('Frequency Min: '), sg.InputText(key='-SG_CHAN_1_FREQ_MIN_IN-'), sg.DropDown(['Hz', 'kHz', 'MHz', 'GHz'], size=(10, 1), key='-SG_CHAN_1_FREQ_MIN_UNIT-')],
                                        [sg.Text('Frequency Max: '), sg.InputText(key='-SG_CHAN_1_FREQ_MAX_IN-'), sg.DropDown(['Hz', 'kHz', 'MHz', 'GHz'], size=(10, 1), key='-SG_CHAN_1_FREQ_MAX_UNIT-')],
                                        [sg.Text('Frequency Step: '), sg.InputText(key='-SG_CHAN_1_FREQ_STEP_IN-'), sg.DropDown(['Hz', 'kHz', 'MHz', 'GHz'], size=(10, 1), key='-SG_CHAN_1_FREQ_STEP_UNIT-')],
                                        [sg.Text('Amplitude: '), sg.InputText(key='-SG_CHAN_1_AMPLITUDE_IN-'), sg.DropDown(['V', 'mV', 'uV'], size=(10, 1), key='-SG_CHAN_1_AMPLITUDE_UNIT-')],
                                        [sg.Text('DC Offset: '), sg.InputText(key='-SG_CHAN_1_OFFSET_IN-'), sg.DropDown(['V', 'mV', 'uV'], size=(10, 1), key='-SG_CHAN_1_OFFSET_UNIT-')],
                                        [sg.Button('Confirm', key='-SG_CHAN_1_CONFIRM-')]
                                    ]

    Signal_Generator_Channel_2_Tab = [  [sg.Text('Signal Generator Channel 2 Settings', size=(30, 1), font=("Helvetica", 20)), sg.Graph(canvas_size=(30, 30), graph_bottom_left=(0, 0), graph_top_right=(30, 30), background_color='blue', key='-SG_CH2_GRAPH-')],
                                        [sg.Checkbox('Enable', default=False, size=(25,1), font=("Helvetica", 20), key='SG_CHAN_2_ENABLE')],
                                        [sg.Text('Signal Type: '), sg.DropDown(['Sine', 'Square', 'Triangle', 'Ramp', 'Pulse', 'Noise', 'DC'], size=(10, 1), key='-SG_CHAN_2_SIGNAL_TYPE-')],
                                        [sg.Text('Frequency Min: '), sg.InputText(key='-SG_CHAN_2_FREQ_MIN_IN-'), sg.DropDown(['Hz', 'kHz', 'MHz', 'GHz'], size=(10, 1), key='-SG_CHAN_2_FREQ_MIN_UNIT-')],
                                        [sg.Text('Frequency Max: '), sg.InputText(key='-SG_CHAN_2_FREQ_MAX_IN-'), sg.DropDown(['Hz', 'kHz', 'MHz', 'GHz'], size=(10, 1), key='-SG_CHAN_2_FREQ_MAX_UNIT-')],
                                        [sg.Text('Frequency Step: '), sg.InputText(key='-SG_CHAN_2_FREQ_STEP_IN-'), sg.DropDown(['Hz', 'kHz', 'MHz', 'GHz'], size=(10, 1), key='-SG_CHAN_2_FREQ_STEP_UNIT-')],
                                        [sg.Text('Amplitude: '), sg.InputText(key='-SG_CHAN_2_AMPLITUDE_IN-'), sg.DropDown(['V', 'mV', 'uV'], size=(10, 1), key='-SG_CHAN_2_AMPLITUDE_UNIT-')],
                                        [sg.Text('DC Offset: '), sg.InputText(key='-SG_CHAN_2_OFFSET_IN-'), sg.DropDown(['V', 'mV', 'uV'], size=(10, 1), key='-SG_CHAN_2_OFFSET_UNIT-')],
                                        [sg.Button('Confirm', key='-SG_CHAN_2_CONFIRM-')]
                                    ]

    Signal_Generator_Tab = [    [sg.Text('Signal Generator', font=("Helvetica", 20))],
                                [sg.Text('Signal Generator ID Address: '), sg.DropDown(rm.list_resources(), size=(30, 1), key='-SG_ID-')],
                                [sg.TabGroup([[sg.Tab('Channel 1', Signal_Generator_Channel_1_Tab, expand_x=True)], [sg.Tab('Channel 2', Signal_Generator_Channel_2_Tab, expand_x=True)]], size=(1280, 720), key='-SG_TABGROUP-')]
                            ]

    Output_Tab = [     [sg.Text('Output Settings', font=("Helvetica", 20))],
                        [sg.Text('Output File Name: '), sg.InputText(key='-OUTPUT_FILE_NAME-')],    
                        [sg.Text('Output File Location: '), sg.InputText(key='-OUTPUT_FILE_LOCATION-'), sg.FolderBrowse()],
                        [sg.Text('Output File Format: '), sg.DropDown(['.csv', '.txt'], size=(20, 1), key='-OUTPUT_FILE_FORMAT-')],
                        [sg.Button('Confirm', key='-OUTPUT_CONFIRM-')]
                 ]

    Execution_Tab = [   [sg.Text('Execution', font=("Helvetica", 20))],
                        [sg.Button('Execute', key='-EXECUTE-'), sg.Button('Stop', key='-STOP-')],
                        [sg.Graph(canvas_size=(1000, 720), graph_bottom_left=(0, 0), graph_top_right=(1000, 720), background_color='darkgray', key='-OUTPUT_GRAPH-'), sg.Table([], headings=['Frequency', 'Amplitude'], key='-OUTPUT_TABLE-', size=(320, 720))]
                    ]

    layout = [  [sg.Text('0001-Project_Glen', font=("Helvetica", 25))],
                [sg.TabGroup([[sg.Tab('Oscilloscope Settings', Oscilloscope_Tab), sg.Tab('Signal Generator Settings', Signal_Generator_Tab), sg.Tab('Output Settings', Output_Tab), sg.Tab('Execution and Output', Execution_Tab)]], size=(1280, 720), key='-TABGROUP-')]
            ]

    # Create the Window
    window = sg.Window('Window Title', layout, size=(1280, 720), resizable=True)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == '-OSC_CH1_CONFIRM-':
            OSC_CHANN_1_SETT = [values['-OSC_ID-'],                                 # 0
                                values['-OSC_CH1_ENABLE-'],                         # 1
                                values['-OSC_CH1_VOLTS_IN-'],                       # 2
                                values['-OSC_CH1_VOLTS_UNIT-'],                     # 3
                                values['-OSC_CH1_HORZ_TIME_DIV_IN-'],               # 4
                                values['-OSC_CH1_HORZ_TIME_DIV_UNIT-'],             # 5
                                values['-OSC_CH1_MEAS_VPP-'],                       # 6
                                values['-OSC_CH1_MEAS_PHASE-'],                     # 7
                                values['-OSC_CH1_MEAS_FREQ-'],                      # 8
                                values['-OSC_CH1_ACQ_MODE-']]                       # 9

            # Bind the hid_device class object to the oscilloscope ID address
            oscilloscope_object = hid_device()
            oscilloscope_object.Connect(OSC_CHANN_1_SETT[0])

        elif event == '-OSC_CH2_CONFIRM-':
            OSC_CHANN_2_SETT = [values['-OSC_ID-'],                                 # 0
                                values['-OSC_CH2_ENABLE-'],                         # 1
                                values['-OSC_CH2_VOLTS_IN-'],                       # 2
                                values['-OSC_CH2_VOLTS_UNIT-'],                     # 3
                                values['-OSC_CH2_HORZ_TIME_DIV_IN-'],               # 4
                                values['-OSC_CH2_HORZ_TIME_DIV_UNIT-'],             # 5
                                values['-OSC_CH2_MEAS_VPP-'],                       # 6
                                values['-OSC_CH2_MEAS_PHASE-'],                     # 7
                                values['-OSC_CH2_MEAS_FREQ-'],                      # 8
                                values['-OSC_CH2_ACQ_MODE-']]                       # 9

        elif event == '-SG_CHAN_1_CONFIRM-':
            SG_CHANN_1_SETT = [values['-SG_ID-'],                                   # 0
                                values['-SG_CHAN_1_ENABLE-'],                       # 1
                                values['-SG_CHAN_1_FREQ_MIN_IN-'],                  # 2
                                values['-SG_CHAN_1_FREQ_MIN_UNIT-'],                # 3
                                values['-SG_CHAN_1_FREQ_MAX_IN-'],                  # 4
                                values['-SG_CHAN_1_FREQ_MAX_UNIT-'],                # 5
                                values['-SG_CHAN_1_FREQ_STEP_IN-'],                 # 6
                                values['-SG_CHAN_1_FREQ_STEP_UNIT-'],               # 7
                                values['-SG_CHAN_1_AMPLITUDE_IN-'],                 # 8
                                values['-SG_CHAN_1_AMPLITUDE_UNIT-'],               # 9
                                values['-SG_CHAN_1_OFFSET_IN-'],                    # 10
                                values['-SG_CHAN_1_OFFSET_UNIT-'],                  # 11
                                values['-SG_CHAN_1_SIGNAL_TYPE-']]                  # 12

            # Create the signal generator object and bind it to the signal generator ID address
            signal_generator_object = hid_device()
            signal_generator_object.Connect(SG_CHANN_1_SETT[0])

            # Add the calculate frequency function here with proper arguments to calculate the frequency for channel 1
            SG_CHANN_1_FREQ = calculate_Frequency(SG_CHANN_1_SETT[1], SG_CHANN_1_SETT[2], SG_CHANN_1_SETT[3], SG_CHANN_1_SETT[4], SG_CHANN_1_SETT[5], SG_CHANN_1_SETT[6])

        elif event == '-SG_CHAN_2_CONFIRM-':
            SG_CHANN_2_SETT = [values['-SG_ID-'],                                   # 0
                                values['-SG_CHAN_1_ENABLE-'],                       # 1
                                values['-SG_CHAN_2_FREQ_MIN_IN-'],                  # 2
                                values['-SG_CHAN_2_FREQ_MIN_UNIT-'],                # 3
                                values['-SG_CHAN_2_FREQ_MAX_IN-'],                  # 4
                                values['-SG_CHAN_2_FREQ_MAX_UNIT-'],                # 5
                                values['-SG_CHAN_2_FREQ_STEP_IN-'],                 # 6
                                values['-SG_CHAN_2_FREQ_STEP_UNIT-'],               # 7
                                values['-SG_CHAN_2_AMPLITUDE_IN-'],                 # 8
                                values['-SG_CHAN_2_AMPLITUDE_UNIT-'],               # 9
                                values['-SG_CHAN_2_OFFSET_IN-'],                    # 10
                                values['-SG_CHAN_2_OFFSET_UNIT-'],                  # 11
                                values['-SG_CHAN_2_SIGNAL_TYPE-']]                  # 12

            # Add the calculate frequency function here with proper arguments to calculate the frequency for channel 2
            SG_CHANN_2_FREQ = calculate_Frequency(SG_CHANN_2_SETT[1], SG_CHANN_2_SETT[2], SG_CHANN_2_SETT[3], SG_CHANN_2_SETT[4], SG_CHANN_2_SETT[5], SG_CHANN_2_SETT[6])

        elif event == '-OUTPUT_CONFIRM-':
            OUTPUT_SETT = [ values['-OUTPUT_FILE_NAME-'],                           # 0
                            values['-OUTPUT_FILE_FORMAT-'],                         # 1
                            values['-OUTPUT_FILE_LOCATION-'] ]                      # 2

        elif event == '-EXECUTE-':
            # Add the send command function here with proper arguments to send the settings to the signal generator and oscilloscope to start the measurement
            # Configure the Oscilloscope first
            # 0.1 Enable Channel 1 and 2 dependent on user input
            if OSC_CHANN_1_SETT[1]:
                # Add the send command function here with proper arguments to enable Channel 1
                oscilloscope_object.Send_Command('CHAN1:DISP ON')

            if OSC_CHANN_2_SETT[1]:
                # Add the send command function here with proper arguments to enable Channel 2
                pass
        
            # 0.2 Configure Oscilloscope parameters for each channel
            if OSC_CHANN_1_SETT[1]:
                # Add the send command function here with proper arguments to configure Channel 1
                pass
            if OSC_CHANN_2_SETT[1]:
                # Add the send command function here with proper arguments to configure Channel 2
                pass

            # Configure the Signal Generator second
            # 0.1 Enable Channel 1 and 2 dependent on user input
            if SG_CHANN_1_SETT[1]:
                # Add the send command function here with proper arguments to enable Channel 1
                pass
            if SG_CHANN_2_SETT[1]:
                # Add the send command function here with proper arguments to enable Channel 2
                pass

            # 0.2 Configure the Signal Generator parameters for each channel
            if SG_CHANN_1_SETT[1]:
                # Add the send command function here with proper arguments to configure Channel 1
                pass
            if SG_CHANN_2_SETT[1]:
                # Add the send command function here with proper arguments to configure Channel 2
                pass

            # Create a 2D array with two inner arrays
            # The first inner array will store the data from Channel 1
            # The second inner array will store the data from Channel 2
            temp = [[],[]]

            # for loop in range(0, SG_CHANN_1_FREQ)
            for i in range(0, SG_CHANN_1_FREQ):
                # Instruct the Signal Generator to send the wavelength on Channel 1
                if SG_CHANN_1_SETT[1]:
                    # Add the send command function here with proper arguments to send the wavelength to Channel 1
                    pass

                # Instruct the Oscilloscope to read the data and store in first array of temp 2D array
                if OSC_CHANN_1_SETT[1]:
                    # Add the send command function here with proper arguments to read the data from Channel 1
                    pass
            
            # for loop in range(0, SG_CHANN_2_FREQ)
            for i in range(0, SG_CHANN_2_FREQ):
                # Instruct the Signal Generator to send the wavelength on Channel 2
                if SG_CHANN_2_SETT[1]:
                    # Add the send command function here with proper arguments to send the wavelength to Channel 2
                    pass
                # Instruct the Oscilloscope to read the data and store in second array of temp 2D array
                if OSC_CHANN_2_SETT[1]:
                    # Add the send command function here with proper arguments to read the data from Channel 2
                    pass

            # Compile the results into a single 2D array and update the results table in the results window
            # Create the bode plot and update the results window

            pass

        elif event == '-STOP-':
            # Add the send command function here with proper arguments to send the settings to the signal generator and oscilloscope to stop the measurement
            pass

        elif event == sg.WIN_CLOSED: # if user closes window
            break
    window.close()

if __name__ == '__main__':
    main()
