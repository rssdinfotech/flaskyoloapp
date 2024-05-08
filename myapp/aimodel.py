# # model.py
# from ultralytics import YOLO
# import pandas as pd
# import os
# import subprocess

# VIDEO_FOLDER = 'runs/detect/predict/'
# def process_video(media_path):
#     model = YOLO("best.pt")
#     names = model.names
#     results = model(source=media_path, show=False, line_width=1, show_conf=False, save=True, max_det=1000)

#     TC = []
#     for result in results:
#         id = list(names)[list(names.values()).index('sperm')]
#         TC.append(result.boxes.cls.tolist().count(id))

#     series = pd.Series(TC)

#     total = round(series.describe().iloc[-1])
#     high_speed = len([speed for speed in TC if speed < series.describe().iloc[7]])
#     dead = len([speed for speed in TC if speed < series.describe().iloc[4]])
#     low_speed = len([speed for speed in TC if speed > series.describe().iloc[4]]) + len([speed for speed in TC if speed < series.describe().iloc[5]])
#     medium_speed = total - (high_speed + low_speed + low_speed)
    
    
#       #video_path = os.path.join(VIDEO_FOLDER, uploaded_file)
#     directory = VIDEO_FOLDER
#     for filename in os.listdir(VIDEO_FOLDER):
#         if filename.lower().endswith(".avi"):
#             full_path = os.path.join(directory, filename)
#             base_name, _ = os.path.splitext(filename) 
#             new_filename = base_name + ".mp4"    
#             new_full_path = os.path.join(directory, new_filename)

#             try:
#                 subprocess.run(["ffmpeg", "-i", full_path, new_full_path])
#                 print(f"Converted '{filename}' to '{new_filename}'")
#             except Exception as e:
#                 print(f"Error converting '{filename}': {e}")

#     return {
#         'total': total,
#         'high_speed': high_speed,
#         'medium_speed': medium_speed,
#         'low_speed': low_speed,
#         'dead': dead
#     }
