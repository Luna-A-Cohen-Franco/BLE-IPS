# BLE-IPS

An indoor positioning system that uses 3 beacons as ESP32s, a tracker that is also an ESP32 which requires a connection to WiFi (configurable within the tracker.py file) and a computer that displays its positioning using the Desmos HTML API.

It requires 4 ESP32s for complete functionality aswell as some form of power source to feed them with.

## Setup

Flash micropython firmware into your esp32s(preferably using the Thonny IDE) and install the aioble module for them with mpremote and mip: "mpremote connect <your port> mip install aioble"

Run httpgethandler.py seperatley before running server.py and open index.html in a web browser.

Inside system.py configure the IP adress with the computer's, use that same IP adress in tracker.py.

Now start system.py, input the distances(Do not move the beacons after this), boot up the tracker and your position will be shown in your web browser through a Desmos graph.

## Warning

This system is intended for institutional and educational purposes only.
