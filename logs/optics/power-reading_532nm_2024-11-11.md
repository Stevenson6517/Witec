---
date: 2024-11-11
description: 'Laser power measurements throughout the beam path'
measured by:
- David Curie
- Richarda Niemann
laser:
    - model: 'Verdi-5W'
    - serial: 'V5-G5403'
    - manufacture date: 'Dec-2004'
    - wavelength: 532
measurement:
    - device: 'Thorlabs PM101'
    - model: 'M00702598'
    - serial: '210608107'
    - calibration date: '2021-05-19'
    - mode: 'Mean over 4000 samples'
---

After realizing that the laser power fluctuates at the sample because of the
observed irregularities at the single-mode fiber output and not because of poor
alignment inside the microscope, I suspected that the laser may be mode hopping
at lower power. I suspect these mode hops to occur only when moving through
certain power thresholds, or when the diode current changes as a result of
requesting higher set power.

I began to wonder if the alignment into the single-mode fiber from the Verdi
output is tuned to an inappropriate laser mode. I know that the Verdi
guarantees the I~00~ mode of a Gaussian profile. I further know that any modes
that aren't the fundamental Gaussian mode are severely attenuated in
a single-mode fiber, such that single-mode fibers can reasonably guarantee
I~00~ transmission, even if the Verdi did have weak non-fundamental Gaussian
transmission.

Because we are dealing with non-standard operating powers, I have doubts on the
reasonable guarantee of I~00~ transmission from the Verdi output and whether
2 meters of single-mode fiber is enough to filter out any modes other than
I~00~.

I wanted to observe the focused laser spot under a microscope objective to see
if the laser spot changes as a result of increased laser power. Because of the
increased laser power involved in this investigation, I insist to use
a protective neutral density filter before the 10x objective that couples the
Verdi output into the single-mode fiber. I wanted to check the laser spot in a focused video feed as a function of laser power to see if there is an obvious shift in the focused profile.

Unfortunately, the laser spot size is difficult to discern at higher set powers
in a camera feed with a filter in place, and it is unclear if the spot size is
affected by the filter or from operating at a higher set laser power (0.1 W).

I instead attempted to quantify this difference in spot size numerically.
I already know the measured power through each objective varies non-linearly as
a function of set laser power, but I have never visually quantified the focused
laser spot as a function of input coupling alignment. If the alignment into the
single-mode fiber is tuned to an inappropriate laser mode, my hope is that the
focused spot size changes size or shape with purposeful misalignment of the
Verdi laser. My assumption for this is that an improper laser mode will exit
the single-mode fiber at a slight angle other than the typical divergence cone
associated with the I~00~ transmission, and that this exit angle will
correspond approximately to the angle of the laser light coming into the fiber
(assuming a non-normal incidence to the fiber core). If we are focusing an
incorrect mode onto the sample, the location of the laser spot should be
dependent on the orientation of the laser incidence into the fiber.

I observed no such change in the focused beam spot for various misalignments.
Two explanations are likely. It is possible the output orientation of the
transmitted laser light is too slight of an adjustment with the misalignments,
and in all such misaligned cases, the laser beam—after having been collimated
inside the WITec—fills the back of the microscope objective in all cases. This
would render the spot size as a limited subset of the true beam profile, whose
propagation mode yet remains undetermined, but whose profile changes as
a function of laser diode current. The simpler conclusion is that the
transmission mode is indeed I~00~ in all cases, and that the laser profile from
the Verdi is uniformly I~00~ as stated by the manufacturer. This then implies
that the non-monotonic power response of the Verdi is related to the diode
current, which is discovered to change across certain power thresholds.

---

After previous purposeful misalignments into the single-mode fiber, I attempted
to get back to my optimum alignment, signaled by a single-mode fiber output of
9.1 mW.

I did not have as much luck or persistence, and after several hours of diligent
tweaking, called the alignment good enough. My quantified results of the system
are listed below.


Configuration
: Verdi -> 10x objective -> SM fiber -> LL filter -> 50:50 BS -> Obj -> Sample -> Obj -> 50:50 BS -> MM assembly out

Diode current
: 23.42 A

| Set power (W) | Location                    | Measured Power (mW) |
|---------------|-----------------------------|---------------------|
| 0.01          | Single-mode fiber out       | 8.3    ± 0.3        |
| 0.01          | Sample (no objective)       | 2.6    ± 0.09       |
| 0.01          | Sample (50x objective)      | 1.91   ± 0.07       |
| 0.01          | Multi-mode fiber out (50x)  | 0.17   ± 0.01       |
| 0.01          | Sample (100x objective)     | 0.64   ± 0.02       |
| 0.01          | Multi-mode fiber out (100x) | 0.078  ± 0.003      |
