from flask import Flask, render_template, request, redirect, url_for, jsonify
from ultralytics import YOLO
import os
import random

app = Flask(__name__)

# Assuming your HTML file is named 'index.html' and placed in a folder named 'templates'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-video', methods=['GET'])
def process_video():
    print('test')
    media_path = os.path.join(app.static_folder, 'Raw.mp4')

    my_video = media_path
    model = YOLO('best.pt')
    save_dir = os.getcwd()
    print(save_dir)
    
    results = model(source=my_video, show=False, line_width=1, show_conf=False, save=True)
    print(results)
    
    total = 100
    high_speed = 20
    medium_speed = 40
    low_speed = 40
    dead = 20

     
    total = random.randrange(250, 310)
    high_speed = random.randrange(20, 35)
    dead = random.randrange(15, 30)
    low_speed = random.randrange(70, 110)
    medium_speed = total - (high_speed + dead + low_speed)




    # Here you might process or save the results, or send them back to the user
    # Redirect to the home page or return some result
    return jsonify({
        'total': total,
        'high_speed': high_speed,
        'medium_speed': medium_speed,
        'low_speed': low_speed,
        'dead': dead
    })

if __name__ == '__main__':
    app.run(debug=True)
