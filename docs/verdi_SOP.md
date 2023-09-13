---
title-meta: "Standard Operating Procedures for Stevenson 6517"
author-meta: David Curie
geometry:
- margin=1in
---

# SOP - Coherent Verdi V-5 Laser - Stevenson 6517

**The American National Standards Institute (ANSI) Standard for Safe Use of
Lasers requires that Standard Operating Procedures (SOP) be written and
approved for Class 3B and 4 lasers or laser systems.**

> This SOP pertains to one of two Verdi lasers located in Stevenson 6517. This
Verdi-V5 is located near the lab entrance and is enclosed in a shielded opaque
box under normal operation. Output light is coupled into a fiber that runs
directly to an upright confocal microscope. While the laser is classified as
a Class IV laser according to its manufacturer, the output light from the
microscope objective does not exceed 5 mW under typical operation with the
surrounding enclosure intact.

## System description

|                                          |                                                    |
|------------------------------------------|----------------------------------------------------|
| Type of laser                            | Diode-pumped, frequency-doubled Nd:YAG             |
| Manufacturer                             | Verdi                                              |
| Model                                    | Verdi-V5                                           |
| Serial Number                            | V5-G5403                                           |
| Classification                           | Class 4                                            |
| Wavelength                               | 532 nm                                             |
| Power                                    | variable, up to 5 W                                |
| Energy per pulse                         | N/A (continuous)                                   |
| Pulse duration                           | N/A (continuous)                                   |
| Repetition rate                          | N/A (continuous)                                   |
| Output beam diameter                     | 2.25 mm ± 10%                                      |
| Beam divergence                          | < 0.5 mrad                                         |
| Intended application                     | Excitation source for photoluminescence microscopy |
| Other system attributes not listed above | External water chiller required for use            |


## Hazards

### Beam hazards

None under typical use.

Alignment procedures dictate using low power (0.01 W) for beam
alignment---in which case no additional beam hazards are present.

### Non-beam hazards

#### Eye

Avoid eye exposure to direct or scattered radiation within the
enclosure box. Avoid eye exposure to the end of the output fiber. Do not
use optical aids to look at the illuminated sample in the microscope.

#### Skin

None under typical use.

#### Laser-generated air contaminants (LGAC)

None under typical use.

#### Scattered radiation

None under typical use.

#### Electrical

None under typical use.

#### Other

Potential for water leaks from coolant system.

Ensure that there is sufficient water in the external chiller and that there
are no leaks during chiller operation. Spilled water presents an electrical
hazard to nearby power supplies and a slip hazard to nearby operators.

Insufficient cooling of the laser will damage the diode. If leaks are detected,
start the shutdown procedure immediately.

## Control measures

### Laser protective eyewear type(s) and requirements for use

During alignment, wear appropriate safety goggles that specifically cover
532 nm emission with OD \> 4. Remove jewelry (e.g. watches, rings, earrings) to
mitigate scattering risks. Use an alignment card to view the beam.

### Laser control area

Under normal operation, the laser is enclosed in an opaque box that mitigates
scattering hazards. Light is coupled to a fiber that runs directly to
a confocal microscope. The total power of the focused laser light through the
microscope objectives is nominally a few milliwatts, and varies slightly depending on
specific microscope objectives and laser operation power.

If alignment to the output fiber is necessary, the enclosure box may be
disassembled, in which case the system should be treated like a class IV laser
that is capable of producing 5W laser light. Direct beam exposure at high power
presents a fire hazard to flammable fabrics worn by users, burn hazards for
unintentional skin contact, and eye hazards for **direct and scattered**
radiation.

Protocols in this SOP dictate the laser be used in low-power mode (0.01 W)
during alignment.

### Entryway controls

Ensure the laser indicator light outside of the lab entrance is illuminated
whenever the laser is on. The switch to control this indicator light is the
right-most switch on the row of light switches near the entryway door and is
labeled "Laser".

### Reference manual

These operating instructions are borrowed from a Verdi V-8 laser. An
unofficial copy of the Verdi V-8/V-10 diode-pumped laser manual can be found
at
<https://vdocuments.net/operators-manual-verdi-v-8v-10-diode-pumped-lasers.html>.

An additional copy of the above referenced manual, along with manuals for
accompanying equipment for this laser, can be found at
<https://github.com/Stevenson6517/Witec> under the `docs` folder.

This document can be edited at
<https://github.com/Stevenson6517/Witec/blob/main/docs/verdi_SOP.md>.

<!-- ...and generated as a PDF with the following command: -->

<!-- ```bash -->
<!-- pandoc -o verdi_SOP.pdf verdi_SOP.md -->
<!-- ``` -->

### Procedures for safe alignment

Adjust the output on the power supply panel to its lowest setting (0.01 W).
Remove any jewelry and reflective articles of clothing and tie back long hair.
Remove all persons from the lab except for those actively involved in
alignment. Each active participant should wear laser safety goggles appropriate
for the laser (OD \> 4 at 532 nm). Work with the room lights on if possible.

Remove the side panel of the lab-made laser enclosure, taking care not to pinch
the optical fiber or water cooled lines that exit through a notch in the panel.
Open the laser shutter and begin alignment. Use an alignment card to view the
beam.

After alignment into the output fiber is complete, reassemble the laser
enclosure system.

### Turn-On (Cold Start)

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
7. Ensure the laser output is blocked or directed at an intended target. If the
   shielded box surrounding the laser is disassembled, **ensure all personnel
   in the area are wearing laser safety glasses.** Turn the keyswitch on the
   power supply front panel to ON.
8. Open the shutter by pressing the SHUTTER OPEN pushbottn on the power supply
   front panel.
9. Laser light will emit from the laser head after the current ramp-up.

### Daily turn-on (warm start)

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

### Daily turn-off (standby)

When the Verdi is being used on a daily basis, turn-off consists of turning the
keyswitch to the STANDBY position. This shuts off the laser diodes and places
the Verdi in standby. This method avoids the heater ramp-up cycle described in
the "Turn-On (Cold Start)" section. The system water chiller should be left on
during short-term shut downs.

> Do not turn the power switch on the power supply rear panel to the OFF
> position.

### Complete shut down

1. Turn the keyswitch power supply on the front panel to STANDBY.
2. Access and select the LBO Settings submenu. Press the MENU SELECT push
   button to start the LBO cool-down cycle. **This cycle takes approximately 30
   minutes.**
3. During the cool-down cycle, the LBO temperature can be monitored from the
   main screen or the LBO Settings submenu. When the LBO temperature decreases
   below 30ºC, tun the AC power switch on the power supply rear panel to the OFF
   position[^temperature].
4. Turn off the chiller.

[^temperature]: The Verdi instruction manual suggests waiting until the system
reaches 40ºC, but this assumes a functional backup battery whereby the power
reserve from the battery maintains the cooldown procedure after the power is
turned off. As of September 2023, the battery fails to maintain a sufficient
charge to run this procedure. These instructions can be updated to reflect the
suggested 40ºC temperature when the battery is replaced.

\clearpage

### Emergency shut down

In the event of an emergency, turn the keyswitch on the power supply front
panel to STANDBY.

If circumstances allow, begin the LBO cooldown procedure.

In the event where immediate evacuation is necessary but no lab hazards exist
(e.g. during a fire alarm), the laser may be left on STANDBY, skipping any LBO
cooldown procedure.

In the event of a water emergency that poses an electrical risk, turn the
keyswitch on the power supply front panel to STANDBY and the AC power switch on
the power supply rear panel to OFF without waiting for the LBO cooldown
procedure, **but beware that this will significantly damage the laser diode**.
Also turn off the chiller.

> If the electrical risk is resolved shortly after the above emergency
shutdown, you may leave the front panel keyswitch on STANDBY, turn the AC power
back to ON, and trigger the LBO cooldown in an effort to mitigate damage caused
by a rapid, uncontrolled cooldown of the laser diode. You may and should also
turn on the chiller if it is safe to do so.

#### Other notes

- The water in the chiller should be changed approximately every 6 months.
  Use only distilled water.
- Maintain a weekly log of the diode current (read from the front screen on the
  power supply) vs. output power. If the diode current increases 10% or more 
  over the initial installation value (or current baseline value) to achieve the
  same output power, use the LBO optimization menu as outlined in the manual.

## Lab-specific training requirements

- Complete and pass Laser Safety Training: <https://www.vanderbilt.edu/ehs/training/#Laser-Safety-Training>
- Complete Chemical Safety Training: <https://www.vanderbilt.edu/ehs/training/#Chemical-Safety-Training>
- Complete a safety walkthrough of laboratory hazards in Stevenson 6517

## Emergency procedures

For medical emergencies, call 911.

For lab-related emergencies, contact Richard Haglund.

### Emergency contact 1

Richard Haglund

Cell: (615) 720-2355

### Emergency contact 2

Sergey Avanesyan

Phone: (615) 343-2336

\clearpage

## Principal investigator

Name: Richard Haglund

Title: Professor

Office: Stevenson 6422

Phone: (615) 322-7964

E-mail: richard.haglund@vanderbilt.edu

## Approved personnel

The following individuals are approved to use this system as of September 21,
2023:

- Richard Haglund
- David Curie
- Alexander Klapowitz

\vfill

---

This Safety Procedure was reviewed and approved by

Name:

Title:

Date of approval:
