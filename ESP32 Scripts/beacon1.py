import sys

sys.path.append("")

from micropython import const
import uasyncio as asyncio
import aioble
import bluetooth

_ID = 1
_ALERT_NOTIF_UUID = bluetooth.UUID(0x1811)
_COMPUTER_APPEARANCE = const(128)
_ADV_INTERVAL_MS = const(5000)

alert_service = aioble.Service(_ALERT_NOTIF_UUID)
aioble.register_services(alert_service)

async def advertise():
    print(f"Started advertising as beacon{_ID}")
    
    while True:
        await aioble.advertise(
                _ADV_INTERVAL_MS,
                name= f"beacon{_ID}",
                services=[_ALERT_NOTIF_UUID],
                appearance= _COMPUTER_APPEARANCE,
                manufacturer=(0xabcd, b"1234"),
            )
        
async def main():
    
    await advertise()
    
asyncio.run(main())

