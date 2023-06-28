"""An example script on how to control the ES-100 stage via SMC Pollux box"""

from micos import SMCPollux

settings = {
        "port" : "/dev/tty.usbserial-1401", # Use COM on Windows
        "baudrate" : 192000,
        "timeout" : 0,
        }

# Using `with` takes care of calling `open()` at start of block and
# `close()` at end of block so connection exits gracefully
with SMCPollux(**settings) as z_stage:
    # z_stage.open()  # Called automatically as part of `with` block
    print(f"Connection to {z_stage.name} established")

    # test ASCII commands from VENUS2 with this syntax:
    z_stage._send_command("1 nst")
    # If the command provides a return value, read it here
    # BEWARE: reading a return value from a write command will stall the
    # program. Use Ctrl+C in python terminal to quit on stall.
    print(z_stage._read_command())


    # Use the high-level commands instead, where the send-query protocol
    # is explicitly defined.


    # Example: read current position
    starting_position = z_stage.get_position()
    print("current position:", z_stage.get_position())

    # Example: move the stage up and query new position
    print("\nMoving the stage up")
    z_stage.move_by(1)  # Relative distance in mm
    # Wait for stage movement to complete
    z_stage.wait_move()
    print("Current position:", z_stage.get_position())

    # Example: move the stage to its known focus point
    print("\nMoving the stage to focus point")
    FOCUS_POINT = -0.916130  # mm (for 50x objective)
    z_stage.move_to(FOCUS_POINT)
    z_stage.wait_move()
    print("Current position:", z_stage.get_position())

    # Example: move the stage to its initial position at the start of
    # this script
    print("\nMoving the stage to starting position ")
    z_stage.move_to(starting_position)
    z_stage.wait_move()
    print("current position:", z_stage.get_position())

    # Example: set the current position to 0 mm
    #
    # z_stage.set_position(0)

    # Example: Begin a continuous jog at 2 mm/s (upwards) and wait for a
    # trigger event before stopping movement
    #
    # z_stage.begin_jog(2)
    # if trigger_condition:
    #     z_stage.end_jog()

    # z_stage.close()  # Called auotmatically as part of `with` block
    print("closing connection")
