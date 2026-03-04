from __future__ import print_function
import time
import xbox
import USART
import readchar
import select


def main():
    # Instantiate the controller and the quadmotor driver
    joy = xbox.Joystick()
    #time.sleep(1)
    QM = USART.Quadmotor()
    input = ""
    active = "n"
    #timeout = 5
    try:
         # Show various axis and button states until Back button is pressed
         print("Do you want to use keywork input: y/n?")
         input = key_input()
         print("Xbox controller: Press Right Trigger button to exit")
         if input == "y":
              active = "y"
              input = ""
         while not joy.rightTrigger():
             #time.sleep(0.2)
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

             if active == "y":
                 input = key_input()
             
             if  input == "u": QM.run("Front")
             if  input == "m": QM.run("Back")
             if  input == "h": QM.run("Left")
             if  input == "k": QM.run("Right")
             if  input == "y": QM.run("TurnLeft")
             if  input == "i": QM.run("TurnRight")
             if joy.dpadUp(): QM.run("Front")
             if joy.dpadDown(): QM.run("Back")
             if joy.dpadLeft(): QM.run("Left")
             if joy.dpadRight(): QM.run("Right")
             if joy.Y(): QM.run("TurnLeft")
             if joy.A(): QM.run("TurnRight")
                           

    except Exception as e:
            print(f"Warning: failed: {e}")
    finally:       
            # Close serial out when done
            QM.CloseSerial()
            # Close joy out when done
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