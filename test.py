import requests
import random

data = [random.random() for _ in range(46)]

response = requests.post(
    "http://127.0.0.1:5000/predict",
    json={"data": data}
)

print("Status:", response.status_code)
print("Response:", response.text)
