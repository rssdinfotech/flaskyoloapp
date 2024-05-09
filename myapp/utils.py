import os
import shutil
import cv2
import numpy as np

UPLOAD_FOLDER = 'static/uploads'
RUNS_FOLDER = 'runs'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv'}

def clean_uploads_folder():
    try:
        # Loop through files in the uploads folder and delete them
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        return True, 'Uploads folder cleaned successfully'
    except Exception as e:
        return False, f'Failed to clean uploads folder: {str(e)}'


def clean_runs_folder():
    try:
        # Recursively loop through all files and directories in the runs folder
        for root, dirs, files in os.walk(RUNS_FOLDER):
            for filename in files:
                file_path = os.path.join(root, filename)
                os.remove(file_path)
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                shutil.rmtree(dir_path)
        return True, 'Runs folder cleaned successfully'
    except Exception as e:
        return False, f'Failed to clean runs folder: {str(e)}'
    
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def classify_contour_size(area):
    if area < 2000:
        return 'small', (0, 0, 255)  # Red
    elif 2000 <= area < 4000:
        return 'medium', (0, 255, 0)  # Green
    elif 4000 <= area:
        return 'big', (255, 0, 0)  # Blue
    else:
        return 'dead', (255, 255, 0)  # Cyan


def calculate_distance(cnt1, cnt2):
    M1 = cv2.moments(cnt1)
    M2 = cv2.moments(cnt2)
    if M1['m00'] == 0 or M2['m00'] == 0:  # Avoid division by zero
        return 0
    cx1 = int(M1['m10'] / M1['m00'])
    cy1 = int(M1['m01'] / M1['m00'])
    cx2 = int(M2['m10'] / M2['m00'])
    cy2 = int(M2['m01'] / M2['m00'])
    return np.sqrt((cx2 - cx1) ** 2 + (cy2 - cy1) ** 2)


def draw_boundaries(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    kernel = np.ones((12, 12), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=2)
    contours_outer, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contour_img = img.copy()
    halo_counts = {'total': 0, 'small': 0, 'medium': 0, 'big': 0, 'dead': 0}

    for cnt_inner, cnt_outer in zip(contours, contours_outer):
        label, color = classify_contour_size(cv2.contourArea(cnt_outer))
        distance = calculate_distance(cnt_inner, cnt_outer)
        cv2.drawContours(contour_img, [cnt_inner], -1, (0, 255, 255), 2)
        cv2.drawContours(contour_img, [cnt_outer], -1, color, 2)
        x, y, w, h = cv2.boundingRect(cnt_outer)
        cv2.putText(contour_img, f"{label} Halo", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        halo_counts['total'] += 1
        halo_counts[label] += 1

    return contour_img, halo_counts

