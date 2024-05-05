import os
import shutil


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
