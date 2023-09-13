# Standard Operating Procedure - Coherent Verdi V-5 Laser

For use in Stevenson 6517. Additional notes on reverse side.

## Turn-On (Cold Start)

1. Ensure the keyswitch is in the STANDBY position.
2. Set the power switch on the power supply rear panel to ON. The AC power and
   LASER EMISSION indicators will light. The power supply display will then
   indicate "System warming up".
3. Turn on the chiller. Verify there are no cooling line connection leaks at the
   Verdi riser/heat sink and at the chiller.
4. Verify the chiller water temperature is set to approximately 20ºC. Adjust 
   the temperature setpoint as required.
5. Set the output power to the desired level using the POWER ADJUST knob. The
   output power can be adjusted to 0.01 watts to facilitate beam alignment.
6. Allow 30 minutes for the heaters and thermo-electric coolers (TECs) to
   achieve operating temperature. The status of all servos can be viewed by
   scrolling to the Servo Status screen. Once this process is complete, the
   system is now ready for key on.
7. Ensure the laser output is blocked or directed at an intended target.
   **Ensure all personnel in the area are wearing laser safety glasses.** Turn the
   keyswitch on the power supply front panel to ON.
8. Open the shutter by pressing the SHUTTER OPEN pushbottn on the power supply
   front panel.
9. Laser light will emit from the laser head after the current ramp-up.

## Daily Turn-On (Warm Start)

A warm-start can be performed when the Verdi power supply rear panel power
switch has been on for more than 30 minutes (laser in standby).

1. Verify there are no cooling line leaks at the Verdi riser/heat sink and at
   the chiller. Verify the chiller water temperature is set to 20ºC. Adjust the
   setpoint temperature as required.
2. The LASER EMISSION indicator should be on. Ensure the laser output is blocked
   or directed at an intended target. Turn the keyswitch on the power supply
   front panel to ON.
3. Open the shutter by pressing the SHUTTER OPEN pushbottn on the power supply
   front panel.
4. Laser light will emit from the laser head after the current ramp-up.

## Daily Turn-Off (Standby)

When the Verdi is being used on a daily basis, turn-off consists of turning the
keyswitch to the STANDBY position. This shuts off the laser diodes and places
the Verdi in standby. This method avoids the heater ramp-up cycle described in
the "Turn-On (Cold Start)" section. The system water chiller should be left on
during short-term shut downs.

> Do not turn the power switch on the power supply rear pane to the OFF
> position.

## Complete Shut Down

1. Turn the keyswitch power supply front panel to STANDBY.
2. Access and select the LBO Settings submenu. Press the MENU SELECT pushbotton
   to start the LBO cool-down cycle.**This cycle takes approximately 30
   minutes.**
3. During the cool-down cycle, the LBO temperature can be monitored from the
   main screen or the LBO Settings submenu. When the LBO temperature decreases
   below 30ºC, tun the AC power switch on the power supply rear panel to the OFF
   position.
4. Turn off the chiller.

> These operating instructions are borrowed from a Verdi V-8 laser. An
> unofficial copy of the Verdi V-8/V-10 diode pumped laser manual can be found
> at
> <https://vdocuments.net/operators-manual-verdi-v-8v-10-diode-pumped-lasers.html>.

# Operating States

+---------+-------------------------------------+--------------------------------------------------------------+
| State   | Switch Position                     | Status                                                       |
+=========|=====================================|==============================================================+
| OFF     | - Power Switch (rear panel): ON     | All functions off except LBO CPU until cool-down is complete |
|         | - All other switches : Any position |                                                              |
+---------+-------------------------------------+--------------------------------------------------------------+
| STANDBY | - Power Switch (rear panel): ON     | - Laser diodes off                                           |
|         | - Keywitch: STANDBY                 | - Vanadate temperature servo off                             |
|         |                                     | - LBO temperature servo on                                   |
|         |                                     | - Etalon temperature servo on                                |
+---------+-------------------------------------+--------------------------------------------------------------+
| ON      | - Power Switch (rear panel): ON     | - Laser diodes on                                            |
|         | - Keywitch: ON                      | - Vanadate temperature servo on                              |
|         |                                     | - LBO temperature servo on                                   |
|         |                                     | - Etalon temperature servo on                                |
+---------+-------------------------------------+--------------------------------------------------------------+

## Other notes

- The water in the chiller should be changed out approximately every 6 months.
  Use distilled water.
- Maintain a weekly log of the diode current (read from the front screen on the
  power supply) vs. output power. If the diode current increases 10% or more 
  over the initial installation value (or current baseline value) to achieve the
  same output power, use the LBO Optimization menu as outlined in the manual.
- The digital version of this document lives in the accompanying WiTEC
  microscope computer under `Documents/Manuals/Verdi`
