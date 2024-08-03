import platform
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
    
    
    if platform.system() == 'Windows':
        ffmpeg_path = os.path.join(os.getcwd(), 'tools', 'win64', 'ffmpeg.exe')
    elif platform.system() == 'Linux':
        ffmpeg_path = os.path.join(os.getcwd(), 'tools', 'linux64', 'ffmpeg')
    else:
        raise EnvironmentError("Unsupported OS")

    ydl_opts = {
        'format': format,
        'ffmpeg_location': ffmpeg_path,
        'progress_hooks': [lambda d: download_hook(d, session_id)],
        'postprocessor_hooks': [lambda d: postprocessor_hook(d, session_id)],
        'outtmpl': os.path.join('output', f'%(extractor)s-%(id)s.%(format_id)s.%(ext)s'),
        'noplaylist': True,
        'cookiefile': 'cookies.txt',
    }
    try:
        create_folder('status')
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except yt_dlp.DownloadError as e:
        print(f"Download error occurred: {e}")
        progress = {'step': 'Err', 'msg': f"Download error occurred: {e}"}
        write_status(session_id, progress)
    except Exception as e:
        print(f"An error occurred: {e}")
        progress = {'step': 'Err', 'msg': f"An error occurred: {e}"}
        write_status(session_id, progress)



def download_hook(d, session_id):
    if d['status'] == 'downloading':
        progress = {
            'step': 'Downloading',
            'percent': d['_percent_str'].strip()
        }
    elif d['status'] == 'finished':
        progress = {
            'step': 'Finished downloading, now post-processing',
            'fileName': d['filename']
        }
    else:
        progress = {'step': 'Unknown'}
    
    write_status(session_id, progress)

def postprocessor_hook(d, session_id):
    if d['status'] == 'started':
        progress = {'step': 'Processing'}
    elif d['status'] == 'finished':
        progress = {
            'step': 'Finished',
            'fileName': d['info_dict']['filepath']
        }
    else:
        progress = {'step': 'Unknown'}
    
    write_status(session_id, progress)

def write_status(session_id, progress):
    status_folder = 'status'
    status_path = os.path.join(status_folder, f'{session_id}.json')
    with open(status_path, 'w') as f:
        json.dump(progress, f)

@bp.route('/api/start-download', methods=['GET'])
def start_download():
    url = request.args.get('url')
    format = request.args.get('format')
    session_id = str(uuid.uuid4())
    
    print(f"Start download, url={url} , format={format}, session={session_id}") 
    
    # Create status folder if not exists
    create_folder('status')
    
    # Write initial status
    write_status(session_id, {'step': 'Started'})

    # Start the download in a new thread
    thread = threading.Thread(target=download_video, args=(url, format, session_id))
    thread.start()


    base_url = request.host_url.rstrip('/')  # Gets the base URL of the request
    session_status_url = f"{base_url}/api/session-status/{session_id}"
    download_file_url = f"{base_url}/api/download-file/{session_id}"

    return jsonify({
        'sessionId': session_id,
        'sessionStatusUrl': session_status_url,
        'downloadFileUrl': download_file_url
    }), 200
