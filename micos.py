"""
A module to interact with a PI-Micos stage through a serial port.

The functions in this module are wrappers around the Venus 2 serial
commands.

ref: http://supernovae.in2p3.fr/~llg/DESI/throughput/docs/motor-Micos-Pollux/Pollux_Venus_eng_2_3.pdf
"""

import time
import logging

import serial

log = logging.getLogger(__name__)

# Temporary workaround to print log to stdout
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# End temporary workaround

class SMCPollux(serial.Serial):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _send_command(self, text):
        try:
            # Commands must be terminated with a blank space and sent
            # as bytestring
            command = (text + " ").encode("utf-8")
            log.debug("Sending command: %s", command)
            self.write(command)
        except serial.serialutil.PortNotOpenError:
            pass

    def _read_command(self):
        try:
            # Remove newline characters from return string
            return self.readline().decode("utf-8").strip("\r\n")
        except serial.serialutil.PortNotOpenError:
            pass

    def _read_status(self):
        try:
            return self.read(1)
        except serial.serialutil.PortNotOpenError:
            pass


    def move_by(self, value, axis=1):
        """Move by a relative amount, in millimeters. Positive values
        move the stage up.
        """
        return self._send_command(f"{float(value)} {axis} nrmove")

    def move_to(self, value, axis=1):
        """Move to an absolute position, in millimeters. Positions are
        measured relative to the focused sample, which is assumed to be
        at 0 mm.
        """
        return self._send_command(f"{float(value)} {axis} nmove")

    def abort(self, *, axis=1):
        """Stop a movement."""
        return self._send_command(f"{axis} nabort")

    def get_position(self, *, axis=1):
        """Read the current stage position in millimeters."""
        self._send_command(f"{axis} npos")
        return self._read_command()

    def set_position(self, value, axis=1):
        """Redefines the current position to the new value."""
        return self._send_command(f"{float(value)} {axis} setnpos")

    def begin_jog(self, speed, axis=1):
        """Move continuously at a constant speed (+/- mm/s) until an
        abort command is issued.

        The speed and direction can be readjusted on the fly by
        reapplying begin_jog(speed).

        Movement can be stopped with end_jog() or abort().
        """
        return self._send_command(f"{float(speed)} {axis} speed")

    def end_jog(self, *, axis=1):
        """Stop a continuous speed movement."""
        return self._send_command(f"{axis} stopspeed")

    def get_status(self, *, axis=1):
        """Query stage status."""
        self._send_command(f"{axis} nstatus")
        return self._read_command()

    def is_moving(self, *, axis=1):
        """Query the movement status of the stage."""
        self._send_command(f"{axis} getaxis")
        return self._read_command()

    def wait_move(self, *, axis=1, query_interval=1e-3):
        """Query repeatedly for stage movement and wait until done.

        Parameters
        ----------
        query_interval : float
            How many seconds to wait before the next stage movement
            query.
            Smaller intervals improve time-sensitive responses, but
            might tie up other system resources more agressively. The
            default query time checks for stage movement once every
            millisecond (1e-3 s).
        """
        # while self.is_moving(axis=axis):
        #     time.sleep(query_interval)

        # TODO: protect against read timeout
        # For now, manually wait a long time to ensure stage is done
        # moving
        time.sleep(3)

    def get_firmware(self, *, axis=1):
        """Query stage firmware."""
        self._send_command(f"{axis} nversion")
        return self._send_command(f"{axis} nversion")

    def get_controller(self, *, axis=1):
        """Query stage controller identification."""
        self._send_command(f"{axis} nidentify")
        return self._read_command()

    def get_serial(self, *, axis=1):
        """Query stage serial number."""
        self._send_command(f"{axis} getnserialno")
        return self._read_command()

    def get_options(self, *, axis=1):
        """Query stage options code."""
        self._send_command(f"{axis} getnoptions")
        return self._read_command()

    def get_address(self, *, axis=1):
        """Query axis address of the current controller."""
        self._send_command(f"{axis} getaxisno")
        return self._read_command()

    def set_address(self, value):
        """Define the axis address of the current controller."""
        return self._send_command(f"{value} setaxisno")

    def reset(self, *, axis=1):
        """Reset the controller."""
        return self._send_command(f"{axis} nreset")
