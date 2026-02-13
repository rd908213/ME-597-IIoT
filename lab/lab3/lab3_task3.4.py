### place your code for Task 3.4
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
import requests
import datetime

URL = "http://10.165.67.146/"
BODY = {
    "code": "request",
    "cid": -1,
    "adr": "/iolinkmaster/port[1]/iolinkdevice/iolreadacyclic",
    "data": {"index": 40, "subindex": 0},
}
HOST = "10.165.67.146"
PORT = 502


class PowerMeterRegister:
    def __init__(self, name: str, address: int) -> float:
        self.name = name
        self.address = address

    def read_register(self, client: ModbusTcpClient):
        read = client.read_holding_registers(self.address, count=2, unit=1)

        if read.isError():
            client.close()
            raise RuntimeError(f"Modbus read error: {read}")

        reg = read.registers

        decoder = BinaryPayloadDecoder.fromRegisters(
            reg, byteorder=Endian.Big, wordorder=Endian.Big
        )

        value = decoder.decode_32bit_float()
        return value


registers = [
    PowerMeterRegister("Frequency [Hz]", 1536),
    PowerMeterRegister("Voltage 1 [V]", 1538),
    PowerMeterRegister("Current 1 [A]", 1550),
    PowerMeterRegister("Power Factor [-]", 1582),
    PowerMeterRegister("True Power [W]", 1564),
]


def read_modbus_data(client):
    if not client.connect():
        raise RuntimeError(f"Connect failed: {HOST}:{PORT}")

    now = datetime.datetime.now()

    for reg in registers:
        value = reg.read_register(client)
        print(f"{now}: {reg.name} is {value}")


def read_iolink_data():
    now = datetime.datetime.now()
    req = requests.post(url=URL, json=BODY)
    data_json = req.json()
    value = data_json["data"]["value"]
    v_rms = round(int(value[0:4], 16) * 0.0001)
    a_peak = round(int(value[8:12], 16) * 0.1)
    a_rms = round(int(value[16:20], 16) * 0.1)
    temperature = round(int(value[24:28], 16) * 0.1)
    crest = round(int(value[32:36], 16) * 0.1)
    print(f"{now}: v_Rms [m/s] is {v_rms}")
    print(f"{now}: a_Peak [m/s^2] is {a_peak}")
    print(f"{now}: a_Rms [m/s^2] is {a_rms}")
    print(f"{now}: Temperature [C] is {temperature}")
    print(f"{now}: Crest [-] is {crest}")


while True:
    with ModbusTcpClient(HOST, port=PORT) as client:
        read_modbus_data(client)
        read_iolink_data()