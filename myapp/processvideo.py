from flask import Flask, render_template, request, redirect, url_for, jsonify,send_file
from ultralytics import YOLO
import os
import subprocess
from utils_services import clean_uploads_folder, clean_runs_folder, allowed_file
import numpy as np
import pandas as pd
from wsgi import app,mysql




UPLOAD_FOLDER = 'static/uploads'
VIDEO_FOLDER = 'runs/detect/predict/'
UPLOAD_FOLDER = 'static/uploads'
RUNS_FOLDER = 'static/runs'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv'}

def process_video():
    uploaded_file = request.json.get('filename')
 
    if not uploaded_file:
        return jsonify({'error': 'No file specified for processing'})

    
    media_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file)
    clean_runs_folder()
    # Load the model
    model = YOLO("best.pt")
    names=model.names

    # Use the model
    results = model(source=media_path, show=False, line_width=1, show_conf=False, save=True, max_det=1000)

    TC = []
    for result in results:
        id = list(names)[list(names.values()).index('sperm')]
        TC.append(result.boxes.cls.tolist().count(id))

    series = pd.Series(TC)


    total = round(series.describe().iloc[-1])
    high_speed = len([speed for speed in TC if speed < series.describe().iloc[7]])
    dead = len([speed for speed in TC if speed < series.describe().iloc[4]])
    low_speed = len([speed for speed in TC if speed > series.describe().iloc[4]]) + len([speed for speed in TC if speed < series.describe().iloc[5]])
    medium_speed = total - (high_speed + low_speed + low_speed)
    

    #video_path = os.path.join(VIDEO_FOLDER, uploaded_file)
    directory = VIDEO_FOLDER
    for filename in os.listdir(VIDEO_FOLDER):
        if filename.lower().endswith(".avi"):
            full_path = os.path.join(directory, filename)
            base_name, _ = os.path.splitext(filename) 
            new_filename = base_name + ".mp4"    
            new_full_path = os.path.join(directory, new_filename)

            try:
                subprocess.run(["ffmpeg", "-i", full_path, new_full_path])
                print(f"Converted '{filename}' to '{new_filename}'")
            except Exception as e:
                print(f"Error converting '{filename}': {e}")
    
    
    save_process_video_output(total,high_speed,medium_speed,low_speed,dead)
    return jsonify({
        'total': total,
        'high_speed': high_speed,
        'medium_speed': medium_speed,
        'low_speed': low_speed,
        'dead': dead
    })




def save_process_video_output(total_sperm,high_speed_sperm,medium_speed_sperm,low_speed_sperm,dead_sperm):
    try:
        # # Connect to the database
        cursor = mysql.cursor()
 
        cursor.execute("INSERT INTO process_results (total_sperm, high_speed_sperm, medium_speed_sperm, low_speed_sperm, dead_sperm) VALUES (%s, %s, %s, %s, %s)",
                       (total_sperm, high_speed_sperm, medium_speed_sperm, low_speed_sperm, dead_sperm))

           # Commit the transaction
        mysql.commit()
        
        
        cursor.close()


    except Exception as e:
        print(f"Error: {e}")
        return False

    
    
def get_last_inserted_record():
    try:
        # Connect to the database
        cursor = mysql.cursor()

        # Execute a query to retrieve the last inserted record
        cursor.execute("SELECT * FROM process_results ORDER BY id DESC LIMIT 1")

        # Fetch the last inserted record
        last_inserted_record = cursor.fetchone()

        # Close the cursor
        cursor.close()
        # Return the last inserted record
        print(last_inserted_record)
        return last_inserted_record

    except Exception as e:
        print(f"Error: {e}")
        return None
    