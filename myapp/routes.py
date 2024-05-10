import base64
import time
from datetime import datetime
from threading import Thread
import cv2
import socketio
from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for, Response
from werkzeug.utils import secure_filename
import os
import subprocess
from utils import clean_uploads_folder, allowed_file, draw_boundaries
# from aimodel import process_video
from auth import auth_login,auth_logout
from wsgi import app
from ultralytics import YOLO
from werkzeug.utils import secure_filename
import numpy as np
import pandas as pd
from processvideo import process_video, get_last_inserted_record
import toupcam

UPLOAD_FOLDER = 'static/uploads'
VIDEO_FOLDER = 'runs/detect/predict/'
RUNS_FOLDER = 'static/runs'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv'}
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'mp4'}

def login_required(func):
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
      
    wrapper.__name__ = func.__name__
    return wrapper


# # Authentication routes
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        # Extract username and password from the form data
        username = request.json.get('username')
        password = request.json.get('password')
        if auth_login(username, password):
            # response = Response(status=302)
            # response.headers['Location'] = '/'
            # # response
            # return response  # Redirect to home page
            # # return redirect('/')
            return jsonify({'msg': 'success in credentials'}), 200  # 401: Unauthorized
            
        else:
            print('login:failed')
            # Return an error response if authentication fails
            return jsonify({'error': 'Invalid credentials'}), 401  # 401: Unauthorized

@app.route('/logout')
def logout():
    auth_logout()
    return redirect ('/')



# Protected routes (require authentication)
@app.route('/')
@login_required
def home():
    print('home called', session)
    if not session.get('logged_in'):
        print('not logged in')
        return redirect(url_for('login'))
    else :# Redirect to login page if not logged in
        res=get_last_inserted_record()
        return render_template('index.html',results=res)


@app.route('/motilitycapture',methods=['GET'])
@login_required
def motilitycapture():
    return render_template('motilityCapture.html')


@app.route('/Dna',methods=['GET'])
@login_required
def dna():
    return render_template('Dna.html')


@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['video']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        clean_uploads_folder()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully', 'filename': filename})
    else:
        return jsonify({'error': 'File type not allowed'})
    
@app.route('/process-video', methods=['POST'])
@login_required
def process_video_route():
    return process_video()
  
@app.route('/get-video/<filename>', methods=['GET'])
@login_required
def get_video(filename):
    video_path = os.path.join(VIDEO_FOLDER, filename)

    if os.path.exists(video_path):
        return send_file(video_path, mimetype='video/mp4')
    else:
        return 'File not found', 404


@app.route('/process_image', methods=['POST'])
def process_image():
    file = request.files['image']
    if not file:
        return "No file uploaded", 400

    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
    contour_img, halo_counts = draw_boundaries(img)
    _, img_encoded = cv2.imencode('.png', contour_img)
    img_data = img_encoded.tobytes()
    img_data_b64 = base64.b64encode(img_data).decode('utf-8')  # Encode to base64
    return jsonify({'imageData': f'data:image/png;base64,{img_data_b64}', 'halo_counts': halo_counts})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image', f"{timestamp}_{filename}")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        file.save(save_path)
        return jsonify({'message': 'Image saved'}), 200


@app.route('/upload-video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'video', f"{timestamp}_{filename}")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        file.save(save_path)
        return jsonify({'message': 'Video saved'}), 200


class App:
    def __init__(self):
        self.hcam = None
        self.buf = None
        self.total = 0

# the vast majority of callbacks come from toupcam.dll/so/dylib internal threads
    @staticmethod
    def cameraCallback(nEvent, ctx):
        if nEvent == toupcam.TOUPCAM_EVENT_IMAGE:
            ctx.CameraCallback(nEvent)

    def CameraCallback(self, nEvent):
        if nEvent == toupcam.TOUPCAM_EVENT_IMAGE:
            try:
                self.hcam.PullImageV3(self.buf, 0, 24, 0, None)
                self.total += 1
                print('pull image ok, total = {}'.format(self.total))
                frame = np.frombuffer(self.buf, dtype=np.uint8).reshape((1920, 1080, 3))
                _, jpeg = cv2.imencode('.jpg', frame)
                encoded_string = base64.b64encode(jpeg.tobytes()).decode('utf-8')
                print("image_frame {encoded_string}")
                socketio.emit('image_frame', {'image': encoded_string})
            except toupcam.HRESULTException as ex:
                print('pull image failed, hr=0x{:x}'.format(ex.hr & 0xffffffff))
        else:
            print('event callback: {}'.format(nEvent))

    def run(self):
        a = toupcam.Toupcam.EnumV2()
        if len(a) > 0:
            print('{}: flag = {:#x}, preview = {}, still = {}'.format(a[0].displayname, a[0].model.flag, a[0].model.preview, a[0].model.still))
            for r in a[0].model.res:
                print('\t = [{} x {}]'.format(r.width, r.height))
            self.hcam = toupcam.Toupcam.Open(a[0].id)
            if self.hcam:
                try:
                    width, height = self.hcam.get_Size()
                    bufsize = toupcam.TDIBWIDTHBYTES(width * 24) * height
                    print('image size: {} x {}, bufsize = {}'.format(width, height, bufsize))
                    self.buf = bytes(bufsize)
                    if self.buf:
                        try:
                            self.hcam.StartPullModeWithCallback(self.cameraCallback, self)
                        except toupcam.HRESULTException as ex:
                            print('failed to start camera, hr=0x{:x}'.format(ex.hr & 0xffffffff))
                    input('press ENTER to exit')
                finally:
                    self.hcam.Close()
                    self.hcam = None
                    self.buf = None
            else:
                print('failed to open camera')
        else:
            print('no camera found')


if __name__ == '__main__':
    cam = App()  # Initialize your App which presumably starts the camera


    def run_camera():
        while True:
            cam.run()
            time.sleep(1)  # Adjust the sleep time based on how frequently you need to check or run camera operations


    # Start the camera run loop in a separate thread
    camera_thread = Thread(target=run_camera)
    camera_thread.start()

    # Start the Flask-SocketIO server
    socketio.run(app, debug=True, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)

    # Optionally, join the thread if you have a specific ending condition
    camera_thread.join()
