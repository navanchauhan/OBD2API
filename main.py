from typing import Optional

from fastapi import FastAPI

import obd

description = """
OBD2REST API 🏎

## /obd

Interact with the OBD adapter using this endpoint.
You can do the following:

* Scan serial port
* Return values from given serial port
* Stream directly to Grafana
"""

api_version = "0.0.1"
api_name = "OBD2REST"

app = FastAPI(
    title=api_name,
    description=api_version,
    contact={
        "name": "Navan Chauhan",
        "url": "https://navan.dev",
        "email": "obd2api@navan.dev"
    }
)

app.streaming_to_grafana = False


api_response_format = {
    "api_version": api_version,
    "api_name": api_name,
}

@app.get("/obd/scan_serial")
def obd_scan_serial():
    ports = obd.scan_serial()
    res = api_response_format
    res["content"] = {"devices":ports}
    return res

@app.get("/obd/get_data")
def obd_get_data(
    serial_port: str = "AUTO", 
    commands: str = "ENGINE_LOAD,MAF,RPM,GET_DTC",
    fast_connect: bool = True,
    timeout: int = 2
    ):
    if not app.streaming_to_grafana:
        res = api_response_format
        if serial_port == "AUTO":
            connection = obd.OBD(fast=fast_connect,timeout=timeout)
        else:
            print(f"Connecting to {serial_port}")
            connection = obd.OBD(serial_port,fast=fast_connect,timeout=timeout)
    else:
        return "no"