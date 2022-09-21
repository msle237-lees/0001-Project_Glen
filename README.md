# Project Number: 0000 #
# Project Name: Project Glen #
### This project is on the request of a buddy. ###

## What he wants ##
#### Software needs to be able to read and write VISA inquires to set a
#### signal generator to output at various frequencies along a spectrum.
#### At each of these frequencies the software should read and record the
#### peak to peak voltage of both the input and output signals (channel 1 and
#### channel 2 of the oscilloscope). Once the sweep is completed, a bode plot
#### should be generated showing the gain of the circuit across a frequency
#### sweep.
#### Two devices are connected to the software over the VISA protocol ###
#### Device 1 is UNI-T UTG962 Signal Generator and Device 2 is a Rigol DS1054Z
#### Oscilloscope. ####
### Configurable arguments: ###
* Frequency start and stop
* Frequency Incrementation value
* Signal to generate (sine, square, ramp, etc)
* Output location
* plot output type

### What he has given me ###
* Sig Gen:
  * Chan 1:
    * Type: Sine wave
      * Frequency: Sweep from 1kHz to 100kHz
      * Amplitude: 200mVpp
      * DC Offset 2.5V

  * Chan 2:
    * Type: Square
      * Amplitude: 2.5V
      * DC Offset: 1.25V
* OSCOPE:
  * Chan 1:
    * Volts/Div: 200mV
      * Horizontal time divisions: ????
      * Measure: Vpp, Phase

  * Chan 1:
    * Volts/Div: 200mV
    * Horizontal time divisions: ????
    * Measure: Vpp, Phase
  * Hor div: 5ms
  * CHAN1 Volts/div: 2V (Chan 1 is output)
  * CHAN2 Volts/div: 200mV (Chan 2 is input)

## Flowchart ##
#### 0. Detect Test Equipment ####
#### 1. Connect to Test Equipment ####
#### 2. Configure Channels on Signal Generator ####
#### 3. Define Channel 2 as Output Value on Signal Generator ####
#### 4. Collect user input: ####
#### ___ 4.1 Ask for Starting Frequency ####
#### ___ 4.2 Ask for Starting Frequency Unit of Measure ####
#### ___ 4.3 Ask for Ending Frequency ####
#### ___ 4.4 Ask for Ending Frequency Unit of Measure ####
#### ___ 4.5 Ask for Frequency Incrementation Value ####
#### ___ 4.6 Ask for Vpp Value ####
#### ___ 4.7 Ask for Offset Value ####
#### ___ 4.8 Ask for Phase Value ####
#### ___ 4.9 Ask for Oscilloscope Channel 1 V/div ####
#### ___ 4.10 Ask for Oscilloscope Channel 2 V/div ####
#### 5. Run src.app.calculate_frequency_list() function ####
#### ___ 5.1 f_list = empty list ####
#### ___ 5.2 determine how many zeros to add to f_max, f_min, f_incr_val
#### ___ 5.3 f_num_of_runs = (f_max - f_min) / f_incr_val ####
#### ___ 5.4 for i in range(0, f_num_of_runs):
#### _________ 5.4.1 f_list.append(f_min + f_incr_val)
#### ___ 5.5 return f_list
#### 6. Send SPCI Commands to machines ####
#### ___ 6.1 Call for s_usb.dev_command.frequency_set() function ####
#### _________ ####
#### ___ 6.2 Call for s_usb.dev_command.Vpp_set() function ####
#### _________ ####
#### ___ 6.3 Call for s_usb.dev_command.DcOffset_set() function ####
#### _________ ####
#### ___ 6.4 Call for s_usb.dev_command.phase_set() function ####
#### _________ ####
#### ___ 6.5 Call for s_usb.dev_command.V_div_set() function ####
#### _________ ####
#### 7. Call for src.app.run_data_gather() function  ####
#### ___ 7.1 data_list = empty list ####
#### ___ 7.2 for i in range(0, f_num_of_runs): ####
#### _________ 7.2.1 data_point = [0, 0]
#### _________ 7.2.1 write signal generator to send f_list[i] ####
#### _________ 7.2.2 data_point[0] = read oscilloscope channel 1 to recv data ####
#### _________ 7.2.3 data_point[1] = read oscilloscope channel 2 to recv data ####
#### _________ 7.2.4 data_list.append(data_point)
#### ___ 7.3 return data_list ###
#### 8. Call for src.app.calc_data_points() function ####
#### ___ 8.1 take in data_list ####
#### ___ 8.2 plot_data = empty list ####
#### ___ 8.3 for i in range(len(data_list)): ####
#### _________ 8.3.1 plot_data.append(data_list[i][0]/data_list[i][1]) ####
#### ___ 8.4 return plot_data ####
#### 9. Call for src.app.cvt_log_scale() function ####
#### ___ 9.1  ####
#### 10. Call for src.app.plot_data_points() function ####
#### ___ 10.1 ####
#### 11. Call export plot_graph() function ####
#### ___ 11.1 ####
