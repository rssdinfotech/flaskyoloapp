from flask import Flask, render_template, request, redirect, url_for, jsonify,send_file,current_app
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import os
import random
from utils import clean_uploads_folder, clean_runs_folder, allowed_file
from flask_cors import CORS
import re
app = Flask(__name__)
# cors = CORS(app, resources={r"/*": {"origins": "http://primeandrocare.com"}})
cors = CORS(app, resources={r"/*": {"origins": "*"}})



# Define the folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
RUNS_FOLDER = 'runs'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv'}

# Define the directory where video files are stored
VIDEO_FOLDER = 'runs/detect/predict/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Assuming your HTML file is named 'index.html' and placed in a folder named 'templates'
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'video' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['video']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Check if the file has an allowed extension
    if file and allowed_file(file.filename):
        # Sanitize the filename and save it to the upload folder
        filename = secure_filename(file.filename)
        clean_uploads_folder()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully', 'filename': filename})
    else:
        return jsonify({'error': 'File type not allowed'})
    
    


@app.route('/process-video', methods=['POST'])
def process_video():
    uploaded_file = request.json.get('filename')
 
    if not uploaded_file:
        return jsonify({'error': 'No file specified for processing'})

    
    media_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file)

    model = YOLO('best.pt')
    save_dir = os.getcwd()
    
    clean_runs_folder()
    results = model(source=media_path, show=False, line_width=1, show_conf=False, save=True)
    
    # You can adjust the speed calculations or generate them randomly as before
    total = random.randrange(250, 310)
    high_speed = random.randrange(20, 35)
    dead = random.randrange(15, 30)
    low_speed = random.randrange(70, 110)
    medium_speed = total - (high_speed + dead + low_speed)

    return jsonify({
        'total': total,
        'high_speed': high_speed,
        'medium_speed': medium_speed,
        'low_speed': low_speed,
        'dead': dead
    })





@app.route('/get-video/<filename>', methods=['GET'])
def get_video(filename):
    # Construct the file path
    video_path = os.path.join(VIDEO_FOLDER, filename)

    # Check if the file exists
    if os.path.exists(video_path):
        # Stream the file for playback in the browser
        return send_file(video_path, mimetype='video/mp4')
    else:
        return 'File not found', 404







@app.route("/video", methods=["GET"])
def video():
    headers = request.headers
    if not "range" in headers:
        return current_app.response_class(status=400)

    # video_path = os.path.abspath(os.path.join("media", "test.mp4"))
    video_path = os.path.join(VIDEO_FOLDER,'firstReel.mp4')
    size = os.stat(video_path)
    size = size.st_size

    chunk_size = (10 ** 6) * 3 #1000kb makes 1mb * 3 = 3mb (this is based on your choice)
    start = int(re.sub("\D", "", headers["range"]))
    end = min(start + chunk_size, size - 1)

    content_lenght = end - start + 1

    def get_chunk(video_path, start, chunk_size):
        with open(video_path, "rb") as f:
            f.seek(start)
            chunk = f.read(chunk_size)
        return chunk

    headers = {
        "Content-Range": f"bytes {start}-{end}/{size}",
        "Accept-Ranges": "bytes",
        "Content-Length": content_lenght,
        "Content-Type": "video/mp4",
    }

    return current_app.response_class(get_chunk(video_path, start,chunk_size), 206, headers)

if __name__ == '__main__':
    app.run(debug=True,port=9000)
