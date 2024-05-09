# routes.py
from flask import Flask, render_template, request, jsonify, send_file,session,redirect,url_for,Response
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

UPLOAD_FOLDER = 'static/uploads'
VIDEO_FOLDER = 'runs/detect/predict/'
UPLOAD_FOLDER = 'static/uploads'
RUNS_FOLDER = 'static/runs'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv'}


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


if __name__ == '__main__':
    app.run(debug=True)
