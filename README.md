# Project Number: 0000 #
# Project Name: Project Glen #
### This project is on the request of a buddy. ###

## What he wants ##
### Software needs to be able to read and write VISA inquires to set a signal generator to output at various frequencies along a spectrum. At each of these frequencies the software should read and record the peak to peak voltage of both the input and output signals (channel 1 and channel 2 of the oscilloscope). Once the sweep is completed, a bode plot should be generated showing the gain of the circuit across a frequency sweep. ###
### Two devices are connected to the software over the VISA protocol ###
### Device 1 is UNI-T UTG962 Signal Generator and Device 2 is a Rigol DS1054Z Oscilloscope. ###
### Configurable arguments: ###
* Frequency start and stop
* Frequency Incrementation value
* Signal to generate (sine, square, ramp, etc)
* Output location
* plot output type
