import os
import base64
from flask import Flask, render_template, request

app = Flask(__name__)

# UPLOAD_FOLDER = os.path.basename('uploads')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    data = request.get_json()
    print (data)
    return "Poopy"
    jpg_original = base64.b64decode(data)

    with open('test.jpg', 'wb') as f_output:
        f_output.write(jpg_original)
if __name__ == '__main__':
    app.run(host = '0.0.0.0') #run app in debug mode on port 5000
