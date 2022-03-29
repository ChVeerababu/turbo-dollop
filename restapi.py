"""
Run a rest API exposing the yolov5s object detection model
"""
import argparse
import io
from PIL import Image

import torch
import time
from flask import Flask, request

app = Flask(__name__)

DETECTION_URL = "/v1/object-detection/yolov5s"

@app.route('/')
def index():
    return 'hello world'


@app.route(DETECTION_URL, methods=["POST"])
def predict():
    if not request.method == "POST":
        return

    if request.files.get("image"):
        image_file = request.files["image"]
        image_bytes = image_file.read()

        img = Image.open(io.BytesIO(image_bytes))

        results = model(img, size=480)
        data = results.pandas().xyxy[0].to_json(orient="records")
        return data

map_location = torch.device("cpu")
model = torch.hub.load("ultralytics/yolov5", "yolov5n",pretrained=True)  # force_reload = recache latest code
model.to(map_location)
model.eval()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
