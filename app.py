import PySimpleGUI as sg
import os
import sys
import numpy as np
import pandas as pd


def main():
    sg.theme('Dark')   # Add a touch of color
    # All the stuff inside your window.
    Oscilloscope_Channel_1_Tab = [  [sg.Text('Oscilloscope Channel 1 Settings', size=(20, 1))],
                                    [sg.Checkbox('Enable', default=False, size=(15,1), key='OSC_CH1_ENABLE')],
                                    [sg.Text('Volts:', size=(15, 1)), sg.InputText(key='-OSC_CH1_VOLTS_IN'), sg.DropDown(['V', 'mV', 'uV'], size=(5, 1), key='-OSC_CH1_VOLTS_UNIT-')],
                                    [sg.Text('Horizontal Time Division: ', size=(15, 1)), sg.InputText(key='-OSC_CH1_HORZ_TIME_DIV_IN'), sg.DropDown(['s', 'ms', 'us', 'ns'], size=(5, 1), key='-OSC_CH1_HORZ_TIME_DIV_UNIT-')],
                                    [sg.Text('Measure: ', size=(15, 1)), sg.Checkbox('Vpp', default=False, size=(15,1), key='OSC_CH1_MEAS_VPP'), sg.Checkbox('Phase', default=False, size=(15,1), key='OSC_CH1_MEAS_PHASE'), sg.Checkbox('Frequency', default=False, size=(15,1), key='OSC_CH1_MEAS_FREQ')],
                                    [sg.Button('Confirm', key='-OSC_CH1_CONFIRM-')]
                                ]
    Oscilloscope_Channel_2_Tab = [  [sg.Text('Oscilloscope Channel 2 Settings', size=(20, 1))],
                                    [sg.Checkbox('Enable', default=False, size=(15,1), key='OSC_CH2_ENABLE')],
                                    [sg.Text('Volts:', size=(15, 1)), sg.InputText(key='-OSC_CH2_VOLTS_IN'), sg.DropDown(['V', 'mV', 'uV'], size=(5, 1), key='-OSC_CH2_VOLTS_UNIT-')],
                                    [sg.Text('Horizontal Time Division: ', size=(15, 1)), sg.InputText(key='-OSC_CH2_HORZ_TIME_DIV_IN'), sg.DropDown(['s', 'ms', 'us', 'ns'], size=(5, 1), key='-OSC_CH2_HORZ_TIME_DIV_UNIT-')],
                                    [sg.Text('Measure: ', size=(15, 1)), sg.Checkbox('Vpp', default=False, size=(15,1), key='OSC_CH2_MEAS_VPP'), sg.Checkbox('Phase', default=False, size=(15,1), key='OSC_CH2_MEAS_PHASE'), sg.Checkbox('Frequency', default=False, size=(15,1), key='OSC_CH2_MEAS_FREQ')],
                                    [sg.Button('Confirm', key='-OSC_CH2_CONFIRM-')]
                                ]

    Oscilloscope_Tab = [    [sg.Text('Oscilloscope Settings', justification='left', font=("Helvetica", 20))],
                            [sg.Text('Oscilloscope ID Address: '), sg.DropDown([], size=(30, 1), key='-OSC_ID-')],
                            [sg.TabGroup([[sg.Tab('Channel 1', Oscilloscope_Channel_1_Tab), sg.Tab('Channel 2', Oscilloscope_Channel_2_Tab)]], size=(1280, 720), key='-OSC_TABGROUP-')]
                        ]

    Signal_Generator_Channel_1_Tab = [  [sg.Text('Signal Generator Channel 1 Settings', size=(20, 1))],
                                        [sg.Checkbox('Enable', default=False, size=(15,1), key='SG_CHAN_1_ENABLE')],
                                        [sg.Text('Signal Type: '), sg.DropDown(['Sine', 'Square', 'Triangle', 'Ramp', 'Pulse', 'Noise', 'DC'], size=(10, 1), key='-SG_CHAN_1_SIGNAL_TYPE-')],
                                        [sg.Text('Frequency Min: '), sg.InputText(key='-SG_CHAN_1_FREQ_MIN_IN-'), sg.DropDown(['Hz', 'kHz', 'MHz', 'GHz'], size=(10, 1), key='-SG_CHAN_1_FREQ_MIN_UNIT-')],
                                        [sg.Text('Frequency Max: '), sg.InputText(key='-SG_CHAN_1_FREQ_MAX_IN-'), sg.DropDown(['Hz', 'kHz', 'MHz', 'GHz'], size=(10, 1), key='-SG_CHAN_1_FREQ_MAX_UNIT-')],
                                        [sg.Text('Frequency Step: '), sg.InputText(key='-SG_CHAN_1_FREQ_STEP_IN-'), sg.DropDown(['Hz', 'kHz', 'MHz', 'GHz'], size=(10, 1), key='-SG_CHAN_1_FREQ_STEP_UNIT-')],
                                        [sg.Text('Amplitude: '), sg.InputText(key='-SG_CHAN_1_AMPLITUDE_IN-'), sg.DropDown(['V', 'mV', 'uV'], size=(10, 1), key='-SG_CHAN_1_AMPLITUDE_UNIT-')],
                                        [sg.Text('DC Offset: '), sg.InputText(key='-SG_CHAN_1_OFFSET_IN-'), sg.DropDown(['V', 'mV', 'uV'], size=(10, 1), key='-SG_CHAN_1_OFFSET_UNIT-')],
                                        [sg.Button('Confirm', key='-SG_CHAN_1_CONFIRM-')]
                                    ]

    Signal_Generator_Channel_2_Tab = [  [sg.Text('Signal Generator Channel 2 Settings', size=(20, 1))],
                                        [sg.Checkbox('Enable', default=False, size=(15,1), key='SG_CHAN_2_ENABLE')],
                                        [sg.Text('Signal Type: '), sg.DropDown(['Sine', 'Square', 'Triangle', 'Ramp', 'Pulse', 'Noise', 'DC'], size=(10, 1), key='-SG_CHAN_2_SIGNAL_TYPE-')],
                                        [sg.Text('Frequency Min: '), sg.InputText(key='-SG_CHAN_2_FREQ_MIN_IN-'), sg.DropDown(['Hz', 'kHz', 'MHz', 'GHz'], size=(10, 1), key='-SG_CHAN_2_FREQ_MIN_UNIT-')],
                                        [sg.Text('Frequency Max: '), sg.InputText(key='-SG_CHAN_2_FREQ_MAX_IN-'), sg.DropDown(['Hz', 'kHz', 'MHz', 'GHz'], size=(10, 1), key='-SG_CHAN_2_FREQ_MAX_UNIT-')],
                                        [sg.Text('Frequency Step: '), sg.InputText(key='-SG_CHAN_2_FREQ_STEP_IN-'), sg.DropDown(['Hz', 'kHz', 'MHz', 'GHz'], size=(10, 1), key='-SG_CHAN_2_FREQ_STEP_UNIT-')],
                                        [sg.Text('Amplitude: '), sg.InputText(key='-SG_CHAN_2_AMPLITUDE_IN-'), sg.DropDown(['V', 'mV', 'uV'], size=(10, 1), key='-SG_CHAN_2_AMPLITUDE_UNIT-')],
                                        [sg.Text('DC Offset: '), sg.InputText(key='-SG_CHAN_2_OFFSET_IN-'), sg.DropDown(['V', 'mV', 'uV'], size=(10, 1), key='-SG_CHAN_2_OFFSET_UNIT-')],
                                        [sg.Button('Confirm', key='-SG_CHAN_2_CONFIRM-')]
                                    ]

    Signal_Generator_Tab = [    [sg.Text('Signal Generator', font=("Helvetica", 20))],
                                [sg.Text('Signal Generator ID Address: '), sg.DropDown([], size=(30, 1), key='-SG_ID-')],
                                [sg.TabGroup([[sg.Tab('Channel 1', Signal_Generator_Channel_1_Tab)], [sg.Tab('Channel 2', Signal_Generator_Channel_2_Tab)]], size=(1280, 720), key='-SG_TABGROUP-')]
                            ]

    General_Tab = [     [sg.Text('General', font=("Helvetica", 20))]]

    Execution_Tab = [   [sg.Text('Execution', font=("Helvetica", 20))]]

    layout = [  [sg.Text('0001-Project_Glen', font=("Helvetica", 25))],
                [
                    sg.TabGroup([[sg.Tab('Oscilloscope Settings', Oscilloscope_Tab), sg.Tab('Signal Generator Settings', Signal_Generator_Tab), sg.Tab('Execution and Output', Execution_Tab), sg.Tab('General Settings', General_Tab)]], size=(1280, 720), key='-TABGROUP-')
                ]
            ]


    # Create the Window
    window = sg.Window('Window Title', layout, size=(1280, 720), resizable=True, finalize=True)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        print('You entered ', values[0])

    window.close()

if __name__ == '__main__':
    main()