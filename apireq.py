import requests
import uuid
from camera_thread import VideoStreamWidget
import time
import cv2

def sendtoserver(frame):
    imencoded = cv2.imencode(".jpg", frame)[1]
    file = {'image': ('image.jpg', imencoded.tostring(), 'image/jpeg', {'Expires': '0'})}
    response = requests.post("http://10.0.2.235:5000/v1/object-detection/yolov5s", files=file, timeout=5)
    j = response.json()
    result = [i for i in j if i['confidence'] > 0.5 and i['class'] == 0]
    return result


video_stream_widget = VideoStreamWidget('https://testvs.iviscloud.net/hls/IVISUSA1003C7/playlist.m3u8')
time.sleep(5)

while True:
    result = sendtoserver(video_stream_widget.frame)
    print(result)
    video_stream_widget.show_frame()
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

