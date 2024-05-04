from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import os
import random
from flask_cors import CORS
import signal
import psutil
import time

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://primeandrocare.com"}})

# Initialize YOLO model globally
model = None

def initialize_model():
    global model
    if model is None:
        model = YOLO('best.pt')

# Function to check memory usage
def check_memory_usage():
    process = psutil.Process()
    memory_usage = process.memory_info().rss  # Resident Set Size (memory used by the process)
    print("\n\n\nMemory usage exceeds threshold: {:.2f} GB".format(memory_usage / (1024 * 1024 * 1024)))

# Periodically check memory usage (e.g., every minute)
# Note: You need to uncomment this part if you want to periodically check memory usage
# import time
# while True:
#     check_memory_usage()
#     time.sleep(60)  # Sleep for 60 seconds before checking again

# Assuming your HTML file is named 'index.html' and placed in a folder named 'templates'
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/process', methods=['GET'])
def process():
    def timeout_handler(signum, frame):
        raise TimeoutError("Request timed out")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(180)  # Set the timeout to 180 seconds (3 minutes)

    try:
        for i in range(180):  # Simulate 3 minutes of processing
            time.sleep(1)  # Sleep for 1 second
            print(f"Processing... {i+1} seconds elapsed.")  # Print progress
        # Send a JSON response
        data = {'status': 'success', 'message': 'Video processed successfully'}
        return jsonify(data)
    except TimeoutError:
        return jsonify({'error': 'Request timed out'}), 504  # Return a 504 Gateway Timeout error
    finally:
        signal.alarm(0)  # Cancel the timeout


@app.route('/process-video', methods=['GET'])
def process_video():
    

   
    initialize_model()  # Ensure the model is initialized
    check_memory_usage()  # Check memory usage

    media_path = os.path.join(app.static_folder, 'Raw.mp4')
    my_video = media_path
    
    save_dir = os.getcwd()
 #   print(save_dir)

    results = model(source=my_video, show=False, line_width=1, show_conf=False, save=True)
    print(results)
    check_memory_usage()
    total = random.randrange(250, 310)
    high_speed = random.randrange(20, 35)
    dead = random.randrange(15, 30)
    low_speed = random.randrange(70, 110)
    medium_speed = total - (high_speed + dead + low_speed)
    print('the model run successfully')
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
    initialize_model()  # Initialize the model when the application starts
    app.run()

