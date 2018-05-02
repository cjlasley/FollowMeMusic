# import os
import external_qr_to_human as qth
from flask import Flask, render_template, request

app = Flask(__name__)
app.counter = 0
app.firstFrame = True
app.spatialVolume = None


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    data = request.get_data()
    print(data)
    with open('raw_cv.jpg', 'wb') as f_output:
        f_output.write(data)
    if app.firstFrame:
        app.firstFrame = False
        app.spatialVolume = qth.SpatialQR("raw_cv.jpg")
        return -1
    volume = app.spatialVolume.getDistanceToVolume("raw_cv.jpg")
    return str(volume)


if __name__ == '__main__':
    app.run(host='0.0.0.0')  # run app in debug mode on port 5000
