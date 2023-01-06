# TO-DO List
# 1. Error Checking
# 2. Plotting data and updating table
# 3. Saving data to csv file dependent on the user input
# 4. Adding the formulas to csv file
# 5. Adding Acquistion mode
# 6. Adding the Option for short delay between each measurement cycle

import math
import os
import sys
import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import PySimpleGUI as sg
import pyvisa as visa

matplotlib.use('TkAgg')

# define the resource manager
global resource_manager
resource_manager = visa.ResourceManager()

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
        self.dev = resource_manager.open_resource(self.HWID, write_termination = '\n', read_termination='\n')
        print(f"Connecting to {self.dev}")
    
    def Send_Command(self, command):
        self.dev.write(command)
        return

    def Read_command(self):
        x = self.dev.read()
        return x

    def Query_Command(self, command):
        x = self.dev.query(command) 
        return(x)

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def calculate_Frequency(freq, unit):
    if unit == 'Hz':
        return int(freq)
    elif unit == 'kHz':
        return int(freq) * 1000
    elif unit == 'MHz':
        return int(freq) * 1000000

def calculate_Frequency_List(freq_min, freq_min_unit, freq_max, freq_max_unit, freq_step, freq_step_unit):
    freq_list = []
    freq_min_out = 0
    freq_max_out = 0
    freq_step_out = 0
    if freq_min_unit == 'Hz':
        freq_min_out = int(freq_min)
    elif freq_min_unit == 'kHz':
        freq_min_out = int(freq_min) * 1000
    elif freq_min_unit == 'MHz':
        freq_min_out = int(freq_min) * 1000000
    if freq_max_unit == 'Hz':
        freq_max_out = int(freq_max)
    elif freq_max_unit == 'kHz':
        freq_max_out = int(freq_max) * 1000
    elif freq_max_unit == 'MHz':
        freq_max_out = int(freq_max) * 1000000
    if freq_step_unit == 'Hz':
        freq_step_out = int(freq_step)
    elif freq_step_unit == 'kHz':
        freq_step_out = int(freq_step) * 1000
    elif freq_step_unit == 'MHz':
        freq_step_out = int(freq_step) * 1000000
    for i in range(freq_min_out, freq_max_out + freq_step_out, freq_step_out):
        freq_list.append(i)
    return freq_list

def calculate_Voltage(volt_min, volt_min_unit, volt_max, volt_max_unit, volt_step, volt_step_unit):
    if volt_min_unit == 'V':
        volt_min = float(volt_min)
    elif volt_min_unit == 'mV':
        volt_min = float(volt_min) / 1000
    elif volt_min_unit == 'uV':
        volt_min = float(volt_min) / 1000000
    if volt_max_unit == 'V':
        volt_max = float(volt_max)
    elif volt_max_unit == 'mV':
        volt_max = float(volt_max) / 1000
    elif volt_max_unit == 'uV':
        volt_max = float(volt_max) / 1000000
    if volt_step_unit == 'V':
        volt_step = float(volt_step)
    elif volt_step_unit == 'mV':
        volt_step = float(volt_step) / 1000
    elif volt_step_unit == 'uV':
        volt_step = float(volt_step) / 1000000
    return volt_min, volt_max, volt_step

def calculate_AMP(amp_in, amp_unit):
    amp_out = 0
    if amp_unit == 'mVpp':
        amp_out = float(amp_in) / 1000
    elif amp_unit == 'Vpp':
        amp_out = float(amp_in)
    return amp_out

def calculate_OFFSET(offset_in, offset_unit):
    offset_out = 0
    if offset_unit == 'mV':
        offset_out = float(offset_in) / 1000
    elif offset_unit == 'V':
        offset_out = float(offset_in)
    return offset_out

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
                            [sg.Text('Oscilloscope ID Address: '), sg.DropDown(resource_manager.list_resources(), size=(30, 1), key='-OSC_ID-')],
                            [sg.TabGroup([[sg.Tab('Channel 1', Oscilloscope_Channel_1_Tab, expand_x=True), sg.Tab('Channel 2', Oscilloscope_Channel_2_Tab, expand_x=True)]], size=(1280, 720), key='-OSC_TABGROUP-')]
                        ]

    Signal_Generator_Channel_1_Tab = [  [sg.Text('Signal Generator Channel 1 Settings', size=(30, 1), font=("Helvetica", 20)), sg.Graph(canvas_size=(30, 30), graph_bottom_left=(0, 0), graph_top_right=(30, 30), background_color='red', key='-SG_CH1_GRAPH-')],
                                        [sg.Checkbox('Enable', default=False, size=(25,1), font=("Helvetica", 20), key='-SG_CHAN_1_ENABLE-')],
                                        [sg.Text('Signal Type: '), sg.DropDown(['SINe', 'SQUare', 'RAMP', 'PULSe'], size=(10, 1), key='-SG_CHAN_1_SIGNAL_TYPE-')],
                                        [sg.Text('Frequency Min: '), sg.InputText(key='-SG_CHAN_1_FREQ_MIN_IN-'), sg.DropDown(['Hz', 'kHz', 'MHz'], size=(10, 1), key='-SG_CHAN_1_FREQ_MIN_UNIT-')],
                                        [sg.Text('Frequency Max: '), sg.InputText(key='-SG_CHAN_1_FREQ_MAX_IN-'), sg.DropDown(['Hz', 'kHz', 'MHz'], size=(10, 1), key='-SG_CHAN_1_FREQ_MAX_UNIT-')],
                                        [sg.Text('Frequency Step: '), sg.InputText(key='-SG_CHAN_1_FREQ_STEP_IN-'), sg.DropDown(['Hz', 'kHz', 'MHz'], size=(10, 1), key='-SG_CHAN_1_FREQ_STEP_UNIT-')],
                                        [sg.Text('Amplitude: '), sg.InputText(key='-SG_CHAN_1_AMPLITUDE_IN-'), sg.DropDown(['Vpp', 'mVpp'], size=(10, 1), key='-SG_CHAN_1_AMPLITUDE_UNIT-')],
                                        [sg.Text('DC Offset: '), sg.InputText(key='-SG_CHAN_1_OFFSET_IN-'), sg.DropDown(['V', 'mV'], size=(10, 1), key='-SG_CHAN_1_OFFSET_UNIT-')],
                                        [sg.Button('Confirm', key='-SG_CHAN_1_CONFIRM-')]
                                    ]

    Signal_Generator_Channel_2_Tab = [  [sg.Text('Signal Generator Channel 2 Settings', size=(30, 1), font=("Helvetica", 20)), sg.Graph(canvas_size=(30, 30), graph_bottom_left=(0, 0), graph_top_right=(30, 30), background_color='blue', key='-SG_CH2_GRAPH-')],
                                        [sg.Checkbox('Enable', default=False, size=(25,1), font=("Helvetica", 20), key='SG_CHAN_2_ENABLE')],
                                        [sg.Text('Signal Type: '), sg.DropDown(['SINe', 'SQUare', 'RAMP', 'PULSe'], size=(10, 1), key='-SG_CHAN_2_SIGNAL_TYPE-')],
                                        [sg.Text('Frequency: '), sg.InputText(key='-SG_CHAN_2_FREQ_IN-'), sg.DropDown(['Hz', 'kHz', 'MHz'], size=(10, 1), key='-SG_CHAN_2_FREQ_UNIT-')],
                                        [sg.Text('Amplitude: '), sg.InputText(key='-SG_CHAN_2_AMPLITUDE_IN-'), sg.DropDown(['Vpp', 'mVpp'], size=(10, 1), key='-SG_CHAN_2_AMPLITUDE_UNIT-')],
                                        [sg.Text('DC Offset: '), sg.InputText(key='-SG_CHAN_2_OFFSET_IN-'), sg.DropDown(['V', 'mV'], size=(10, 1), key='-SG_CHAN_2_OFFSET_UNIT-')],
                                        [sg.Button('Confirm', key='-SG_CHAN_2_CONFIRM-')]
                                    ]

    Signal_Generator_Tab = [    [sg.Text('Signal Generator', font=("Helvetica", 20))],
                                [sg.Text('Signal Generator ID Address: '), sg.DropDown(resource_manager.list_resources(), size=(30, 1), key='-SG_ID-')],
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
                        [sg.Graph(canvas_size=(1000, 720), graph_bottom_left=(0, 0), graph_top_right=(1000, 720), background_color='darkgray', key='-OUTPUT_GRAPH-'), sg.Table([], headings=['Frequency', 'Decibel'], key='-OUTPUT_TABLE-', size=(320, 720))]
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
            SG_CHANN_1_FREQ = calculate_Frequency_List(SG_CHANN_1_SETT[2], SG_CHANN_1_SETT[3], SG_CHANN_1_SETT[4], SG_CHANN_1_SETT[5], SG_CHANN_1_SETT[6], SG_CHANN_1_SETT[7])

        elif event == '-SG_CHAN_2_CONFIRM-':
            SG_CHANN_2_SETT = [values['-SG_ID-'],                                   # 0
                                values['-SG_CHAN_1_ENABLE-'],                       # 1
                                values['-SG_CHAN_2_FREQ_IN-'],                      # 2
                                values['-SG_CHAN_2_FREQ_UNIT-'],                    # 3
                                values['-SG_CHAN_2_AMPLITUDE_IN-'],                 # 4
                                values['-SG_CHAN_2_AMPLITUDE_UNIT-'],               # 5
                                values['-SG_CHAN_2_OFFSET_IN-'],                    # 6
                                values['-SG_CHAN_2_OFFSET_UNIT-'],                  # 7
                                values['-SG_CHAN_2_SIGNAL_TYPE-']]                  # 8

        elif event == '-OUTPUT_CONFIRM-':
            OUTPUT_SETT = [ values['-OUTPUT_FILE_NAME-'],                           # 0
                            values['-OUTPUT_FILE_FORMAT-'],                         # 1
                            values['-OUTPUT_FILE_LOCATION-'] ]                      # 2
            Output_file = os.path.join(OUTPUT_SETT[2], OUTPUT_SETT[0])
            Output_type = OUTPUT_SETT[1]
            

        elif event == '-EXECUTE-':
            # Add the send command function here with proper arguments to send the settings to the signal generator and oscilloscope to start the measurement
            # Configure the Oscilloscope first
            # 0.1 Enable Channel 1 and 2 dependent on user input
            if OSC_CHANN_1_SETT[1]:
                # Add the send command function here with proper arguments to enable Channel 1
                oscilloscope_object.Send_Command(':CHAN1:DISP ON')
                oscilloscope_object.Send_Command('CHAN1:SCAL ' + str(calculate_OFFSET(OSC_CHANN_1_SETT[2], OSC_CHANN_1_SETT[3])))
                if OSC_CHANN_1_SETT[6]:
                    oscilloscope_object.Send_Command(':MEAS:STAT:ITEM VPP,CHAN1')
                if OSC_CHANN_1_SETT[8]:
                    oscilloscope_object.Send_Command(':MEAS:STAT:ITEM FREQ,CHAN1')

            if OSC_CHANN_2_SETT[1]:
                # Add the send command function here with proper arguments to enable Channel 2
                oscilloscope_object.Send_Command(':CHAN2:DISP ON')
                oscilloscope_object.Send_Command('CHAN1:SCAL ' + str(calculate_OFFSET(OSC_CHANN_1_SETT[2], OSC_CHANN_1_SETT[3])))
                if OSC_CHANN_2_SETT[6]:
                    oscilloscope_object.Send_Command(':MEAS:STAT:ITEM VPP,CHAN2')
                if OSC_CHANN_2_SETT[7]:
                    oscilloscope_object.Send_Command(':MEAS:STAT:ITEM RPH,CHAN2,CHAN1')
                if OSC_CHANN_2_SETT[8]:
                    oscilloscope_object.Send_Command(':MEAS:STAT:ITEM FREQ,CHAN2')

            # Configure the Signal Generator second
            # 0.1 Enable Channel 1 and 2 dependent on user input
            if SG_CHANN_1_SETT[1]:
                # Add the send command function here with proper arguments to enable Channel 1
                signal_generator_object.Send_Command(':CHAN1:OUTP 1')
                signal_generator_object.Send_Command(':CHAN1:BASE:WAV ' + SG_CHANN_1_SETT[12])
                signal_generator_object.Send_Command(':CHAN1:BASE:FREQ ' + str(SG_CHANN_1_FREQ[0]))
                signal_generator_object.Send_Command(':CHAN1:BASE:OFFS ' + str(calculate_OFFSET(SG_CHANN_1_SETT[10], SG_CHANN_1_SETT[11])))
                signal_generator_object.Send_Command(':CHAN1:BASE:AMPL ' + str(calculate_AMP(SG_CHANN_1_SETT[8], SG_CHANN_1_SETT[9])))

            if SG_CHANN_2_SETT[1]:
                # Add the send command function here with proper arguments to enable Channel 2
                signal_generator_object.Send_Command(':CHAN2:OUTP 1')
                signal_generator_object.Send_Command(':CHAN2:BASE:WAV ' + SG_CHANN_2_SETT[8])
                signal_generator_object.Send_Command(':CHAN2:BASE:FREQ ' + str(calculate_Frequency(SG_CHANN_2_SETT[2], SG_CHANN_2_SETT[3])))
                signal_generator_object.Send_Command(':CHAN2:BASE:OFFS ' + str(calculate_OFFSET(SG_CHANN_2_SETT[6], SG_CHANN_2_SETT[7])))
                signal_generator_object.Send_Command(':CHAN2:BASE:AMPL ' + str(calculate_AMP(SG_CHANN_2_SETT[4], SG_CHANN_2_SETT[5])))

            # Create a 2D array with two inner arrays
            # The first inner array will store the data from Channel 1
            # The second inner array will store the data from Channel 2
            chan_1_vpp = []
            chan_1_freq = []
            chan_2_vpp = []
            chan_2_freq = []
            chan_2_phase = []

            # for loop in range(0, SG_CHANN_1_FREQ)
            decibel = []
            for i in range(0, len(SG_CHANN_1_FREQ)):
                oscilloscope_object.Send_Command(':TIM:MAIN:SCAL ' + str(1/(6*SG_CHANN_1_FREQ[i])))

                # Instruct the Signal Generator to send the wavelength on Channel 1
                if SG_CHANN_1_SETT[1]:
                    # Add the send command function here with proper arguments to send the wavelength to Channel 1
                    signal_generator_object.Send_Command(':CHAN1:BASE:FREQ ' + str(SG_CHANN_1_FREQ[i]))
                    time.sleep(0.1)

                # Instruct the Oscilloscope to read the data and store in first array of temp 2D array
                if OSC_CHANN_1_SETT[1]:
                    # Add the send command function here with proper arguments to read the data from Channel 1
                    chan_1_vpp.append(oscilloscope_object.Query_Command(':MEAS:STAT:ITEM? CURR,VPP,CHAN1'))
                    chan_1_freq.append(oscilloscope_object.Query_Command(':MEAS:STAT:ITEM? CURR,FREQ,CHAN1'))

                if OSC_CHANN_2_SETT[1]:
                    # Add the send command function here with proper arguments to read the data from Channel 2
                    chan_2_freq.append(oscilloscope_object.Query_Command(':MEAS:STAT:ITEM? CURR,FREQ,CHAN2'))
                    chan_2_vpp.append(oscilloscope_object.Query_Command(':MEAS:STAT:ITEM? CURR,VPP,CHAN2'))
                    chan_2_phase.append(oscilloscope_object.Query_Command(':MEAS:STAT:ITEM? CURR,RPH,CHAN2,CHAN1'))

                decibel.append(20*math.log10(float(chan_2_vpp[i])/float(chan_1_vpp[i])))
                window['-OUTPUT_TABLE-'].update([SG_CHANN_1_FREQ[i], decibel[i]])

            # Compile the results into a single 2D array and update the results table in the results window
            vpp_ratio = [float(i)/float(j) for i, j in zip(chan_2_vpp, chan_1_vpp)]
            results = list(zip(chan_1_freq, chan_1_vpp, chan_2_vpp, chan_2_freq, chan_2_phase, vpp_ratio, decibel))
            df = pd.DataFrame(results, columns=['Channel 1 Frequency', 'Channel 1 Vpp', 'Channel 2 Vpp', 'Channel 2 Frequency', 'Channel 2 Phase', 'Vpp Ratio', 'Decibel'])
            df.to_csv(Output_file + Output_type, encoding='utf-8', index=False)
            plt.xscale('log')
            plt.plot(df['Channel 1 Frequency'], df['Decibel'])
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Decibel')
            plt.savefig(Output_file + '.png')
            window['-OUTPUT_GRAPH-'].update(Output_file + '.png')

            
        elif event == '-STOP-':
            # Add the send command function here with proper arguments to send the settings to the signal generator and oscilloscope to stop the measurement
            signal_generator_object.Send_Command(':SYST:LOCK 0')

        elif event == sg.WIN_CLOSED: # if user closes window
            break
    window.close()

if __name__ == '__main__':
    main()
