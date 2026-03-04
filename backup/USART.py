import serial
import time


class Quadmotor:

 def __init__(self, xboxin):
    # Store the initial value as an instance variable
    self.xboxin = xboxin

 UPLOAD_DATA = 3  
                 #0: Do not receive data 1: Receive total encoder data 2: Receive real-time encoder 3: Receive current motor speed mm/s

 MOTOR_TYPE = 1  
                #1:520 motor 2:310 motor 3:speed code disc TT motor 4:TT DC reduction motor 5:L type 520 motor

 # Serial port initialization
 ser = serial.Serial(
    port='/dev/ttyUSB0',  # Modify it to your serial port device path according to the actual situation
    baudrate=115200,      # Baud rate, must be consistent with the driver board
    parity=serial.PARITY_NONE,  #No check digit
    stopbits=serial.STOPBITS_ONE,  # One stop bit
    bytesize=serial.EIGHTBITS,    # Data bit 8 bits
    timeout=1                     # Timeout (seconds)
 )

 # Receive Buffer
 recv_buffer = ""

 def main():
        t = 400 #speed
        DIR = ""
        print("please wait...")
        send_upload_command(UPLOAD_DATA)#Send the data that needs to be reported to the motor module
        time.sleep(0.1)
        #send_data("$flash_reset#")
        set_motor_parameter() #Design motor parameters
        
        #while True:
        received_message = receive_data()  # Receiving Messages
        if received_message:    # If there is data returned
                parsed = parse_data(received_message) # Parsing the data
                if parsed:
                    print(parsed)  # Print the parsed data
            
        #DIR = key_input()
        DIR = xboxin
        # Front, Back, Right, Left, TurnRight, TurnLeft
        M1, M2, M3, M4 = set_motor_direction(DIR, t)

        #control_speed(M1, M2, M3, M4)# Send commands directly to control the motor
        control_pwm(M1*2.5, M2*2.5, M3*2.5, M4*2.5)
            
        if t> 1000 or t < -1000:
                t = 0
            
        print ("speed:",t)
        #t += 10
        time.sleep(1)

 # Sending Data
 def send_data(data):
    ser.write(data.encode())  # Convert the string to bytes before sending
    time.sleep(0.01)  # Delay to ensure data transmission is completed

 # Receiving Data
 def receive_data():
    global recv_buffer
    if ser.in_waiting > 0:  # Check if there is data in the serial port buffer
        recv_buffer += ser.read(ser.in_waiting).decode()  # Read and decode data
        
        # Split the message by the ending character "#"
        messages = recv_buffer.split("#")
        recv_buffer = messages[-1]
        
        if len(messages) > 1:
            return messages[0] + "#"  #Return a complete message
    return None

 # Configure motor type
 def set_motor_type(data):
    TYPE = data
    send_data("$mtype:{}#".format(TYPE))

 # Configuring Dead Zone
 def set_motor_deadzone(data):
    DZ = data
    send_data("$deadzone:{}#".format(DZ))

 # Configuring magnetic loop
 def set_pluse_line(data):
    LINE = data
    send_data("$mline:{}#".format(LINE))

 # Configure the reduction ratio
 def set_pluse_phase(data):
    PHASE = data
    send_data("$mphase:{}#".format(PHASE))

 # Configuration Diameter
 def set_wheel_dis(data):
    WHEEL = data
    send_data("$wdiameter:{}#".format(WHEEL))

 # Controlling Speed
 def control_speed(m1, m2, m3, m4):
    send_data("$spd:{},{},{},{}#".format(m1, m2, m3, m4))

 # PID
 #def set_p_i_d(p, i, d):
 #    send_data("$MPID:{},{},{}#".format(p, i, d))

 # Control PWM (for motors without encoder)
 def control_pwm(m1, m2, m3, m4):
    send_data("$pwm:{},{},{},{}#".format(m1, m2, m3, m4))

 # Parsing received data
 def parse_data(data):
    data = data.strip()  # Remove spaces or line breaks at both ends

    if data.startswith("$MAll:"):
        values_str = data[6:-1]  #Remove "$MAll:" and "#"
        values = list(map(int, values_str.split(',')))  # Split and convert to integer
        parsed = ', '.join([f"M{i+1}:{value}" for i, value in enumerate(values)])
        return parsed
    elif data.startswith("$MTEP:"):
        values_str = data[6:-1]
        values = list(map(int, values_str.split(',')))
        parsed = ', '.join([f"M{i+1}:{value}" for i, value in enumerate(values)])
        return parsed
    elif data.startswith("$MSPD:"):
        values_str = data[6:-1]
        values = [float(value) if '.' in value else int(value) for value in values_str.split(',')]
        parsed = ', '.join([f"M{i+1}:{value}" for i, value in enumerate(values)])
        return parsed

  #Switch that needs to receive data
 def send_upload_command(mode):
      if mode == 0:
          send_data("$upload:0,0,0#")
      elif mode == 1:
          send_data("$upload:1,0,0#")
      elif mode == 2:
          send_data("$upload:0,1,0#")
      elif mode == 3:
          send_data("$upload:0,0,1#")

 ##The following parameters can be configured according to the actual motor you use. You only need to configure it once. The motor driver board has a power-off saving function.
 def set_motor_parameter():

    if MOTOR_TYPE == 1:
        set_motor_type(1)  # Configure motor type
        time.sleep(0.1)
        set_pluse_phase(56)  # Configure the reduction ratio and check the motor manual for the result.
        time.sleep(0.1)
        set_pluse_line(11)  # Configure the magnetic ring wire and check the motor manual to get the result
        time.sleep(0.1)
        set_wheel_dis(100.00)  # Configure the wheel diameter and measure it
        time.sleep(0.1)
        set_motor_deadzone(1600)  # Configure the motor dead zone, and the experiment shows
        time.sleep(0.1)
        #set_p_i_d(0.8,0.06,0.5)  # Configure the motor pid, cycle power after send this command
        #time.sleep(0.1)

    elif MOTOR_TYPE == 2:
        set_motor_type(2)
        time.sleep(0.1)
        set_pluse_phase(20)
        time.sleep(0.1)
        set_pluse_line(13)
        time.sleep(0.1)
        set_wheel_dis(48.00)
        time.sleep(0.1)
        set_motor_deadzone(1300)
        time.sleep(0.1)

    elif MOTOR_TYPE == 3:
        set_motor_type(3)
        time.sleep(0.1)
        set_pluse_phase(45)
        time.sleep(0.1)
        set_pluse_line(13)
        time.sleep(0.1)
        set_wheel_dis(68.00)
        time.sleep(0.1)
        set_motor_deadzone(1250)
        time.sleep(0.1)

    elif MOTOR_TYPE == 4:
        set_motor_type(4)
        time.sleep(0.1)
        set_pluse_phase(56)
        time.sleep(0.1)
        set_motor_deadzone(1000)
        time.sleep(0.1)

    elif MOTOR_TYPE == 5:
        set_motor_type(1)
        time.sleep(0.1)
        set_pluse_phase(56)
        time.sleep(0.1)
        set_pluse_line(11)
        time.sleep(0.1)
        set_wheel_dis(100.00)
        time.sleep(0.1)
        set_motor_deadzone(1600)
        time.sleep(0.1)  

 def set_motor_direction(DIR, t):

    if DIR == "Right":
        M1 = t*1.5
        M2 = t*1.5
        M3 = t*1.5
        M4 = t*1.5
        return (M1, M2, M3, M4)

    elif DIR == "Left":
        M1 = -t*1.5
        M2 = -t*1.5
        M3 = -t*1.5
        M4 = -t*1.5
        return (M1, M2, M3, M4)

    elif DIR == "Front":
        M1 = -t
        M2 = t
        M3 = t
        M4 = -t
        return (M1, M2, M3, M4)
    
    elif DIR == "Back":
        M1 = t
        M2 = -t
        M3 = -t
        M4 = t
        return (M1, M2, M3, M4)
    
    elif DIR == "TurnRight":
        M1 = t*1.5
        M2 = t*1.5
        M3 = -t*1.5
        M4 = -t*1.5
        return (M1, M2, M3, M4)
    
    elif DIR == "TurnLeft":
        M1 = -t*1.5
        M2 = -t*1.5
        M3 = t*1.5
        M4 = t*1.5       
        return (M1, M2, M3, M4)   
    
    else:
        M1 = 0
        M2 = 0
        M3 = 0
        M4 = 0   
        return (M1, M2, M3, M4)     

 def key_input():
    key = input()
    if key == "u":
                DIR = "Front"
    elif key == "m":
                DIR = "Back"
    elif key == "k":
                DIR = "Right"
    elif key == "h":
                DIR = "Left"
    elif key == "i":
                DIR = "TurnRight"
    elif key == "y":
                DIR = "TurnLeft"
    else:
                DIR = ""
    return DIR

 if __name__ == "__main__":
    try:
        t = 400 #speed
        DIR = ""
        print("please wait...")
        send_upload_command(UPLOAD_DATA)#Send the data that needs to be reported to the motor module
        time.sleep(0.1)
        #send_data("$flash_reset#")
        set_motor_parameter() #Design motor parameters
        
        while True:
            received_message = receive_data()  # Receiving Messages
            if received_message:    # If there is data returned
                parsed = parse_data(received_message) # Parsing the data
                if parsed:
                    print(parsed)  # Print the parsed data
            
            #DIR = key_input()
            DIR = xboxin
            # Front, Back, Right, Left, TurnRight, TurnLeft
            M1, M2, M3, M4 = set_motor_direction(DIR, t)

            #control_speed(M1, M2, M3, M4)# Send commands directly to control the motor
            control_pwm(M1*2.5, M2*2.5, M3*2.5, M4*2.5)
            
            if t> 1000 or t < -1000:
                t = 0
            
            print ("speed:",t)
            #t += 10
            time.sleep(1)

    except KeyboardInterrupt:
        control_pwm(0, 0, 0, 0)#Stop the motor
        control_pwm(0, 0, 0, 0)#Stop the motor
    finally:
        ser.close()  # Close the serial port
        ser.close()  # Close the serial port
