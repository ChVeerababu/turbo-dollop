"""
Run a rest API exposing the yolov5s object detection model
"""
import argparse
import io
from PIL import Image

import torch
import time
from flask import Flask, request, render_template,redirect

app = Flask(__name__)

DETECTION_URL = "/v1/object-detection/yolov5s"
#parser = argparse.ArgumentParser(description="Flask api exposing yolov5 model")
#parser.add_argument("--port", default=5000, type=int, help="port number")
#args = parser.parse_args()
map_location = torch.device("cpu")
model = torch.hub.load("ultralytics/yolov5", "yolov5n", classes = 0,pretrained=True)  # force_reload = recache latest code
model.to(map_location)
model.eval()

@app.route('/')
def index():
	global model
	model = torch.hub.load("ultralytics/yolov5", "yolov5n", classes = 0,pretrained=True) 
	model.to(map_location)
	model.eval()
	return 'hello world'

@app.route(DETECTION_URL, methods=["POST"])
def predict():
    s = time.time()
    if not request.method == "POST":
        return

    if request.files.get("image"):
        image_file = request.files["image"]
        image_bytes = image_file.read()

        img = Image.open(io.BytesIO(image_bytes))

        results = model(img, size=640)
        data = results.pandas().xyxy[0].to_json(orient="records")
        e = time.time()
        print(e-s)
        return data

@app.route("/predict", methods=["GET", "POST"])
def web():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if not file:
            return

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        results = model(img, size=640)

        # for debugging
        # data = results.pandas().xyxy[0].to_json(orient="records")
        # return data

        results.render()  # updates results.imgs with boxes and labels
        for img in results.imgs:
            img_base64 = Image.fromarray(img)
            img_base64.save("static/image0.jpg", format="JPEG")
        return redirect("static/image0.jpg")

    return render_template("index.html")


#app.run(host="0.0.0.0", port=5000)  # debug=True causes Restarting with stat
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
