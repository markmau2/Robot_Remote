import serial
import time


class Quadmotor:
    def __init__(self):
        self.UPLOAD_DATA = 3
        self.MOTOR_TYPE = 1
        self.recv_buffer = ""
        self.ser = None
        self.connectserial()
        self.t = 400 #speed mm/s
        #print("speed:", t)
        #print("please wait...")
        self.send_upload_command(self.UPLOAD_DATA)
        time.sleep(0.1)
        self.set_motor_parameter()
        time.sleep(0.1)

    def connectserial(self, port="/dev/ttyUSB0", baudrate=115200, timeout=1):
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=timeout
            )
        except Exception as e:
            print(f"Warning: failed to open serial port {port}: {e}")
            self.ser = None
        
    def CloseSerial(self):
         self.control_pwm(0, 0, 0, 0)
         self.ser.close()

    def send_data(self, data):
        if not self.ser:
            print("Serial port not open; cannot send data:", data)
            return
        try:
            self.ser.write(data.encode())
            time.sleep(0.01)
        except Exception as e:
            print("Error sending data:", e)

    def receive_data(self):
        try:
            if self.ser.in_waiting > 0:
                self.recv_buffer += self.ser.read(self.ser.in_waiting).decode()
                messages = self.recv_buffer.split("#")
                self.recv_buffer = messages[-1]
                if len(messages) > 1:
                    return messages[0] + "#"
            return None
        except Exception as e:
            print("Error reading serial:", e)
        return None

    def set_motor_type(self, data):
        self.send_data(f"$mtype:{data}#")

    def set_motor_deadzone(self, data):
        self.send_data(f"$deadzone:{data}#")

    def set_pluse_line(self, data):
        self.send_data(f"$mline:{data}#")

    def set_pluse_phase(self, data):
        self.send_data(f"$mphase:{data}#")

    def set_wheel_dis(self, data):
        self.send_data(f"$wdiameter:{data}#")

    def control_speed(self, m1, m2, m3, m4):
        self.send_data(f"$spd:{m1},{m2},{m3},{m4}#")

    def control_pwm(self, m1, m2, m3, m4):
        self.send_data(f"$pwm:{m1},{m2},{m3},{m4}#")

    def parse_data(self, data):
        if not data:
            return None
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

    def send_upload_command(self, mode):
        if mode == 0:
            self.send_data("$upload:0,0,0#")
        elif mode == 1:
            self.send_data("$upload:1,0,0#")
        elif mode == 2:
            self.send_data("$upload:0,1,0#")
        elif mode == 3:
            self.send_data("$upload:0,0,1#")

    def set_motor_parameter(self):
        if self.MOTOR_TYPE == 1:
            self.set_motor_type(1)
            time.sleep(0.1)
            self.set_pluse_phase(56)
            time.sleep(0.1)
            self.set_pluse_line(11)
            time.sleep(0.1)
            self.set_wheel_dis(100.00)
            time.sleep(0.1)
            self.set_motor_deadzone(1600)
            time.sleep(0.1)
        elif self.MOTOR_TYPE == 2:
            self.set_motor_type(2)
            time.sleep(0.1)
            self.set_pluse_phase(20)
            time.sleep(0.1)
            self.set_pluse_line(13)
            time.sleep(0.1)
            self.set_wheel_dis(48.00)
            time.sleep(0.1)
            self.set_motor_deadzone(1300)
            time.sleep(0.1)
        elif self.MOTOR_TYPE == 3:
            self.set_motor_type(3)
            time.sleep(0.1)
            self.set_pluse_phase(45)
            time.sleep(0.1)
            self.set_pluse_line(13)
            time.sleep(0.1)
            self.set_wheel_dis(68.00)
            time.sleep(0.1)
            self.set_motor_deadzone(1250)
            time.sleep(0.1)
        elif self.MOTOR_TYPE == 4:
            self.set_motor_type(4)
            time.sleep(0.1)
            self.set_pluse_phase(56)
            time.sleep(0.1)
            self.set_motor_deadzone(1000)
            time.sleep(0.1)
        elif self.MOTOR_TYPE == 5:
            self.set_motor_type(1)
            time.sleep(0.1)
            self.set_pluse_phase(56)
            time.sleep(0.1)
            self.set_pluse_line(11)
            time.sleep(0.1)
            self.set_wheel_dis(100.00)
            time.sleep(0.1)
            self.set_motor_deadzone(1600)
            time.sleep(0.1)

    def set_motor_direction(self, DIR, t):
        if DIR == "Right":
            return (t * 2, t * 2, t * 2, t * 2)
        if DIR == "Left":
            return (-t * 2, -t * 2, -t * 2, -t * 2)
        if DIR == "Front":
            return (-t, t, t, -t)
        if DIR == "Back":
            return (t, -t, -t, t)
        if DIR == "TurnRight":
            return (t * 1, t * 1, -t * 1, -t * 1)
        if DIR == "TurnLeft":
            return (-t * 1.5, -t * 1.5, t * 1.5, t * 1.5)
        if DIR == "Stop":
            return (0, 0, 0, 0)
        #return (0, 0, 0, 0)

    def key_input(self):
        key = input().strip()
        mapping = {
            "u": "Front",
            "m": "Back",
            "k": "Right",
            "h": "Left",
            "i": "TurnRight",
            "y": "TurnLeft",
        }
        return mapping.get(key, "")

    def run(self, xboxin = None):
        self.xboxin = xboxin
        t = self.t
        x = 2.5
        DIR = self.xboxin 
        #DIR = key_input()
        print(DIR)
        M1, M2, M3, M4 = self.set_motor_direction(DIR, t)
        self.control_pwm(M1 * x, M2 * x, M3 * x, M4 * x)
        if t > 1000 or t < -1000:
           t = 0
        time.sleep(0.3)
        try:
            received_message = self.receive_data()
            if received_message:
                parsed = self.parse_data(received_message)
                if parsed:
                    print(parsed)
               # time.sleep(0.1)
        except KeyboardInterrupt as e:
            print("Error receiving data:", e)
            self.control_pwm(0, 0, 0, 0)
            self.ser.close()
        finally:
            self.control_pwm(0, 0, 0, 0)
            #if self.ser:
                #try:
                    #self.ser.close()
                #except Exception:
                    #pass

if __name__ == "__main__":
    qm = Quadmotor()
    qm.run()