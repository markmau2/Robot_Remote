from __future__ import print_function
import sys
import time
import xbox
import USART
import readchar
import select
import termios
import tty


# Keyboard keys -> robot direction
KEY_MAP = {
    "u": "Front",
    "m": "Back",
    "h": "Left",
    "k": "Right",
    "y": "TurnLeft",
    "i": "TurnRight",
}


def main():
    # Instantiate the quadmotor driver
    QM = USART.Quadmotor(port="/dev/ttyCH341USB0", baudrate=115200, timeout=1)
    joy = None
    active = "n"
    try:
         print("Do you want to use keywork input: y/n?")
         if key_input() == "y":
              active = "y"
         # Instantiate the controller; in keyboard mode it is optional
         try:
              joy = xbox.Joystick()
         except IOError as e:
              if active != "y":
                   raise
              print(f"Warning: {e} - continuing with keyboard only")
         if joy is not None:
              print("Xbox controller: Press Right Trigger button to exit")
         if active == "y":
              print("Keyboard: u/m/h/k/y/i to move, q to exit")
         while True:
             if joy is not None:
                 try:
                     if joy.rightTrigger():
                         break
                     # Show connection status
                     show("Connected:")
                     showIf(joy.connected(), "Y", "N")
                     # Dpad U/D/L/R
                     show("  Dpad:")
                     showIf(joy.dpadUp(), "Front")
                     showIf(joy.dpadDown(), "Back")
                     showIf(joy.dpadLeft(), "Left")
                     showIf(joy.dpadRight(), "Right")
                     showIf(joy.Y(), "TurnLeft")
                     showIf(joy.A(), "TurnRight")
                     # Move cursor back to start of line
                     show(chr(13))

                     if joy.dpadUp(): QM.run("Front")
                     if joy.dpadDown(): QM.run("Back")
                     if joy.dpadLeft(): QM.run("Left")
                     if joy.dpadRight(): QM.run("Right")
                     if joy.Y(): QM.run("TurnLeft")
                     if joy.A(): QM.run("TurnRight")
                 except IOError as e:
                     # Controller unplugged: keep going if keyboard mode is on
                     if active != "y":
                         raise
                     print(f"\nWarning: {e} - continuing with keyboard only")
                     joy.close()
                     joy = None

             if active == "y":
                 key = key_input()
                 if key == "q":
                     break
                 if key in KEY_MAP:
                     QM.run(KEY_MAP[key])

    except Exception as e:
            print(f"Warning: failed: {e}")
    finally:
            # Close serial out when done
            QM.CloseSerial()
            # Close joy out when done
            if joy is not None:
                joy.close()

def key_input():
        key = readchar.readkey()
        #readable, writeable, exception = select.select([readchar.readkey()],[],[],0.1)
        #if readable:
             #key = readchar.readkey()
        #else: key = ""
        #mapping = {
            #"u": "Front",
            #"m": "Back",
            #"k": "Right",
            #"h": "Left",
            #"i": "TurnRight",
            #"y": "TurnLeft",
        #}
        #return mapping.get(key, "")
        return key

# Format floating point number to string format -x.xxx
def fmtFloat(n):
    return '{:6.3f}'.format(n)

# Print one or more values without a line feed
def show(*args):
    for arg in args:
        print(arg, end="")

# Print true or false value based on a boolean, without linefeed
def showIf(boolean, ifTrue, ifFalse=" "):
    if boolean:
        show(ifTrue)
    else:
        show(ifFalse)


if __name__ == "__main__":
    main()