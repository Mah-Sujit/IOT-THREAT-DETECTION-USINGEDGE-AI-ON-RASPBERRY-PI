
import requests
import time
import random

DETECTOR_IP = "192.168.1.73"

while True:
    data = [random.random() for _ in range(46)]

    try:
        response = requests.post(
            f"http://{DETECTOR_IP}:5000/predict",
            json={"data": data}
        )
        print(response.json())

    except Exception as e:
        print("Error:", e)

    time.sleep(1)
