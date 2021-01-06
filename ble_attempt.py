"""
Demonstration of a Bluefruit BLE Central for Circuit Playground Bluefruit.
Connects to the first BLE
UART peripheral it finds. Sends Bluefruit ColorPackets,
read from three accelerometer axis, to the
peripheral.
"""

import time

# import board
# import busio
# import digitalio
# import neopixel

# from adafruit_bluefruit_connect.color_packet import ColorPacket

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()

uart_connection = None
# See if any existing connections are providing UARTService.
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

if ble.connected:
    for connection in ble.connections:
        if UARTService in connection:
            uart_connection = connection
        break

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass

    if not uart_connection:
        print("Scanning...")
        kPa_tx = uart_server.read()
        print(kPa_tx)
        for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=5):
            if UARTService in adv.services:
                print("found a UARTService advertisement")
                uart_connection = ble.connect(adv)
                break
        # Stop scanning whether or not we are connected.
        ble.stop_scan()
    ble.stop_advertising()
#     while uart_connection and uart_connection.connected:
#         r, g, b = map(scale, accelerometer.acceleration)

#         color = (r, g, b)
#         neopixels.fill(color)
#         color_packet = ColorPacket(color)
#         try:
#             uart_connection[UARTService].write(color_packet.to_bytes())
#         except OSError:
#             try:
#                 uart_connection.disconnect()
#             except:  # pylint: disable=bare-except
#                 pass
#             uart_connection = None
        # time.sleep(0.3)