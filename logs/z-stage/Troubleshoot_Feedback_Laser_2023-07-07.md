Troubleshoot\_Feedback\_Laser\_2023-07-07

Friday, July 7, 2023

7:47 PM

Feedback laser

-   Removed screws on panel front of Beam Deflector Laser module to check for poor electrical connection. The switch, laser input, and power LED connections to panel were attached from the inside, preventing the panel from being removed without severing the wires.

-   Potentially able to be accessed from the panel back? Two screws located underneath the padding on the back blue frame might open back panel. High voltage components so I will need to be grounded and extremely careful of capacitors.

405nm diode laser as substitute?

-   Datasheet says 30mW power output. Used THORLABS PM50 analog power meter to measure power at fiber output: ~25mW. Fiber is attached to the interior components of the laser and is therefore not able to be removed.

-   alphaSNOM manual says feedback laser is (785 ± 15) nm and between 1 and 5 mW. Will probably have to use ND filter on the 405 as the manual doesn't have any specs on the photodetector. Also, photodetector material may not respond to wavelengths under 700.

 

Update: Beam deflection laser \*does\* work. Measuring its power output via the analog power meter gives power reading of about 4 mW but does not appear to be on as it is likely a substituted laser in the near-IR (980 nm). One of the AlphaSNOM manuals lists this as a possible laser wavelength (the other lists 785nm).
