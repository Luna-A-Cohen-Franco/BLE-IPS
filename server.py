import socket
import json
from math import sqrt
    
class Beacon:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.distance = 0
        self.avg = 0
        self.value_count = 0

    def update_avg(self, new_value):
        avg = ((self.avg * self.value_count) + new_value) / (self.value_count + 1)
        self.avg = avg
        return avg

    def json(self):
        return f"\t\"beacon{self.id}\": " + "{\n" + f"\t\t\"id\": {self.id},\n\t\t\"x\":{self.x},\n\t\t\"y\":{self.y},\n\t\t\"distance\":{self.distance}" + "\n\t}" 

class Tracker:
    def __init__(self, x = 0, y = 0):
        self.x = float(x)
        self.y = float(y)

    def json(self):
        return "\t\"tracker\": {\n" + f"\t\t\"x\": {self.x},\n\t\t\"y\": {self.y}\n\t" + "}"
    
    def update_position(self, beacons):
        x = (pow(beacons[0].distance, 2) - pow(beacons[1].distance, 2) + pow(beacons[1].x, 2)) / (2*beacons[2].x)
        y = (pow(beacons[0].distance, 2) - pow(beacons[2].distance, 3) + pow(beacons[2].y, 2) - (2*beacons[1].x * self.x)) / (2*beacons[2].y)
        if abs(abs(self.x) - abs(x)) > 5 or abs(abs(self.y) - abs(y)) > 5:
            return
        self.x = x
        self.y = y

#Parse RSSI to Meter
def r2m(rssi, meassured_power = -69, env_factor = 4):
    return round(pow(10, (meassured_power - rssi)/(10*env_factor)))



def setup():
    c = float(input("Enter the distance in meters from beacon 0 to beacon 1\n"))
    b = float(input("Enter the distance in meters from beacon 0 to beacon 2\n"))
    a = float(input("Enter the distance in meters from beacon 1 to beacon 2\n"))
    beacon0 = Beacon(0, 0, 0)
    beacon1 = Beacon(1, c, 0)

    aux = pow(c, 2) + pow(a, 2) - pow(b, 2)
    x2 = aux / (2*a)
    y2 = sqrt(pow(c, 2) - (pow(aux, 2)/(4*pow(a, 2))))
    beacon2 = Beacon(2, round(x2), round(y2))

    return ([
        beacon0,
        beacon1,
        beacon2
    ], Tracker())

def update_distance(beacons, id, distance):
    beacons[id].distance = distance

def create_socket(_HOST, _PORT):
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.bind((_HOST, _PORT))
    sckt.listen()
    conn, addr = sckt.accept()
    
    print(f"Connected with {addr}")
    
    return conn

def listen(conn, beacons, tracker):
    while True:
        bdata = conn.recv(1024)
        jdata = json.loads(bdata)
        print(jdata)
        update_distance(beacons, jdata['id'], r2m(beacons[jdata['id']].update_avg(jdata['rssi'])))
        tracker.update_position(beacons)
        with open('coordinates.json', 'w') as file:
            file.write(jsonify_data(beacons, tracker))
        
 
# Turn the tracker and the beacons into a json string
def jsonify_data(beacons, tracker):
        json = "{\n" + tracker.json() + ','

        for beacon in beacons:
            json = json + beacon.json()
            if beacon.id != 2:
                json = json + ","
        return json + "}"


      
def main():
    (beacons, tracker) = setup()
    
    _HOST = "172.16.254.42"
    _PORT = 50028   
    conn = create_socket(_HOST, _PORT)
    listen(conn, beacons, tracker);

main()