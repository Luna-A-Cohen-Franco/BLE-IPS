import sys

sys.path.append("")

import uasyncio as asyncio
import aioble
import bluetooth
import socket
import network

async def connect_to_wifi(_SSID, _PASSWORD):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(_SSID, _PASSWORD)
    
async def create_socket(_HOST, _PORT):
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.connect((_HOST, _PORT))

    return sckt

async def scan(sckt):
    _SCAN_INTERVAL_MS = 5000

    print("Started hearing")

    while True:
        async with aioble.scan(duration_ms = _SCAN_INTERVAL_MS) as scanner:
            async for result in scanner:
                await asyncio.sleep(1)
                if isinstance(result.name(), str) and "beacon" in result.name():
                    id = result.name().replace("beacon", "")
                    
                    meassure = b"{\n" + f"\t \"id\": {id},\n \t \"rssi\": {result.rssi}\n" + "}"
                    print(meassure)
                    sckt.send(meassure)

async def main():
    _SSID = "ServerBLE"
    _PASSWORD = "oqwin1238ajsdjqi"
    await connect_to_wifi(_SSID, _PASSWORD)
    
    _HOST = "172.16.254.42"
    _PORT = 50028
    sckt = await create_socket(_HOST, _PORT)
    
    await scan(sckt)
    
asyncio.run(main())
