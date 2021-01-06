import time
from adafruit_crickit import crickit
import board
import busio
import adafruit_mprls
# may need to import PWMOut via pulseio or, on CP7, pwmio
# for the motor's duty_cycle: 50% recommended.
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

motor_1 = crickit.dc_motor_1
i2c = busio.I2C(board.D6, board.D5)
mpr = adafruit_mprls.MPRLS(i2c, psi_min=0, psi_max=25)  # 25psi = 172kPa

print("Initial pressure (kPa):", mpr.pressure/10)

while True:

    ble.start_advertising(advertisement)
    while not ble.connected:
        pass
    # ble.stop_advertising()

    while ble.connected:
        kPa = mpr.pressure/10
        uart_server.write("{},\n".format(kPa, ))
        print(kPa)
        # time.sleep(3.0)
        # kPa_tx = uart_server.read()
        # print(kPa_tx)

        if kPa > 96.5266 and kPa <= 172.3600:
            # print((kPa, ))
            motor_1.throttle = 0.0
            # time.sleep(1.0)
        elif 0 < kPa <= 96.5266:
            # print((kPa, ))
            motor_1.throttle = 1.0
            # time.sleep(1.0)
        else:
            # print((kPa, ))
            motor_1.throttle = 0.0
            # time.sleep(1.0)
        time.sleep(2.0)
    # Advertise when not connected.

    # and repeat!