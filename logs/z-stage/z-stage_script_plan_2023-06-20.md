6.20.23 z-stage script

Tuesday, June 20, 2023

2:55 PM

The auto-approach function works by lowering the z-stage until the cantilever makes contact with the sample. At that point, the T-B signal spikes (to setpoint voltage?) and the z-stage stops moving. Since the new z-stage is not connected to ScanCtrl, we have to stop the z-stage from moving through a different means.

 

The sigma output on the Beam Deflection Module, which outputs a voltage proportional to the sum of the light intensities in all 4 quadrants of the photodetector, is unused during NSOM mode. <s>If we can connect a probe from that output to a microcontroller that monitors the voltage, it can send a signal to via USB to PIMikroMove to stop the descent of the z-stage.</s> The sigma output should theoretically remain the same throughout descend/scan/contact, because the total light on the photodetector remains the same. Therefore, not a viable output to monitor contact.

 

Therefore, the only way to accurately determine whether tip contact has been made would be to monitor the T-B output voltage. The problem is, the T-B output in the Beam Deflection module is connected to the IN port of the Feedback Controller Module.

 

For this to work, the Arduino must be able to communicate with PIMikroMove.

 

<u>PIMikroMove</u>

-   "If you start PIMikroMove from a command line or via batch processing, you can choose the following options:

    -   "--nowaitautoconnect" suppresses the count-down window if the AutoConnect functionality is activated. AutoConnect is then executed immediately upon the start of PIMikroMove

    -   '-m' or '--macro' with filename as argument will start a host macro after PIMikroMove has been started. This works only if AutoConnect has been performed successfully, and if all controllers affected by this host macro are connected"

-   **3.6 Scan 1D Window**

    -   "With the Scan 1D window you can measure an input source while moving an axis. Input source can be analog inputs or responses to query commands sent by PIMikroMove."

 

 

Maybe we can bypass the auto-approach functionality altogether…

 

Steps for auto-approach

1.  Move the microscope down until cantilever is close to but not touching the sample

2.  Press **Auto Approach**

    1.  The microscope will move down until the cantilever contacts the sample, at which point the display will read: Tip is in contact. The T-B signal will jump to the setpoint value.

    2.  The microscope will then move further down until the Z-positi bon display of the piezo-stage shows approx 15 um.

3.  After a successful approach, move the microscope slowly up, until the cantilever snaps out of contact

    1.  Setpoint value changes back to roughly 0.100 and Z-stage shows 1--.--

4.  Reset the position reading and move up an additional 20 um.

5.  …

6.  Press the **Auto Approach Start** button and wait until the stage stops at a z-position of about 15 um. *The image of the transmitted light should stay in focus, because the upper and the lower objective move down parallel (only in SNOM auto approach mode).*
