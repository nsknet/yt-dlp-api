import os
from flask import Flask
import yt_dlp

app = Flask(__name__)


# Set the FFmpeg executable path
ffmpeg_path = os.path.join(os.getcwd(), 'tools', 'ffmpeg.exe')
# Ensure yt_dlp uses the custom FFmpeg path
yt_dlp.utils.std_headers['FFMPEG'] = ffmpeg_path



# Import API endpoints
from api import get_download_info, start_download, session_status, download_file, get_download_json
from p404 import bp as index_bp

# Register API endpoints
app.register_blueprint(get_download_info.bp)
app.register_blueprint(start_download.bp)
app.register_blueprint(session_status.bp)
app.register_blueprint(download_file.bp)
app.register_blueprint(get_download_json.bp)

# Register the index blueprint to handle un-routed URLs
app.register_blueprint(index_bp)

if __name__ == "__main__":
    app.run(debug=True)
