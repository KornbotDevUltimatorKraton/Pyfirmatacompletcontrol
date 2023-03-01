import pyfirmata
import time

# Define the sysex command for the I2C_CONFIG message
I2C_CONFIG = 0x78

# Define the sysex command for the I2C_REQUEST message
I2C_REQUEST = 0x76

# Define the sysex command for the I2C_REPLY message
I2C_REPLY = 0x77

# Define the address of the MPU6050
MPU6050_ADDR = 0x68

# Define the register address of the accelerometer data
ACCEL_XOUT_H = 0x3B

# Define the register address of the gyroscope data
GYRO_XOUT_H = 0x43

# Connect to the Arduino board
board = pyfirmata.Arduino('/dev/ttyACM0')

# Set up the I2C bus
board.send_sysex(I2C_CONFIG, [0, 0, 2])  # Set up the bus to use the default clock frequency of 100kHz

# Define a function to read data from the MPU6050
def read_mpu6050_data():
    # Send a request for accelerometer data
    board.send_sysex(I2C_REQUEST, [MPU6050_ADDR, ACCEL_XOUT_H, I2C_REPLY, 6])
    # Wait for the reply to come back
    while not board.sp.read():
        pass
    # Parse the reply data
    data = board.sp.read()
    accel_x = (data[1] << 8) | data[0]
    accel_y = (data[3] << 8) | data[2]
    accel_z = (data[5] << 8) | data[4]
    # Send a request for gyroscope data
    board.send_sysex(I2C_REQUEST, [MPU6050_ADDR, GYRO_XOUT_H, I2C_REPLY, 6])
    # Wait for the reply to come back
    while not board.sp.read():
        pass
    # Parse the reply data
    data = board.sp.read()
    gyro_x = (data[1] << 8) | data[0]
    gyro_y = (data[3] << 8) | data[2]
    gyro_z = (data[5] << 8) | data[4]
    # Return the data as a tuple
    return (accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)

# Main loop
while True:
    # Read the MPU6050 data
    accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = read_mpu6050_data()
    # Print the data
    print("Accelerometer: ({}, {}, {})".format(accel_x, accel_y, accel_z))
    print("Gyroscope:     ({}, {}, {})".format(gyro_x, gyro_y, gyro_z))
    # Wait for a short period of time
    time.sleep(0.1)
