from flask import Blueprint, request, jsonify
import yt_dlp
import os
import json
import uuid
import threading

bp = Blueprint('start_download', __name__)

def create_folder(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder created at: {folder_path}")
    except Exception as e:
        print(f"An error occurred while creating the folder: {e}")

def download_video(url, format, session_id):
    ffmpeg_path = os.path.join(os.getcwd(), 'tools', 'ffmpeg', 'bin', 'ffmpeg')
    ydl_opts = {
        'format': format,
        'ffmpeg_location': ffmpeg_path,
        'progress_hooks': [lambda d: download_hook(d, session_id)],
        'postprocessor_hooks': [lambda d: postprocessor_hook(d, session_id)],
        'outtmpl': os.path.join('output', f'{session_id}.%(ext)s'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_hook(d, session_id):
    if d['status'] == 'downloading':
        progress = {
            'Step': 'Downloading',
            'Percent': d['_percent_str'].strip()
        }
    elif d['status'] == 'finished':
        progress = {
            'Step': 'Finished downloading, now post-processing',
            'FileName': d['filename']
        }
    else:
        progress = {'Step': 'Unknown'}
    
    write_status(session_id, progress)

def postprocessor_hook(d, session_id):
    if d['status'] == 'started':
        progress = {'Step': 'Processing'}
    elif d['status'] == 'finished':
        progress = {
            'Step': 'Finished',
            'FileName': d['info_dict']['filepath']
        }
    else:
        progress = {'Step': 'Unknown'}
    
    write_status(session_id, progress)

def write_status(session_id, progress):
    status_folder = 'status'
    create_folder(status_folder)
    status_path = os.path.join(status_folder, f'{session_id}.json')
    with open(status_path, 'w') as f:
        json.dump(progress, f)

@bp.route('/api/start-download', methods=['GET'])
def start_download():
    url = request.args.get('url')
    format = request.args.get('format')
    session_id = str(uuid.uuid4())
    
    # Create status folder if not exists
    create_folder('status')
    
    # Write initial status
    write_status(session_id, {'Step': 'Started'})

    # Start the download in a new thread
    thread = threading.Thread(target=download_video, args=(url, format, session_id))
    thread.start()

    return jsonify({'sessionId': session_id}), 200
