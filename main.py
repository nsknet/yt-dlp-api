import os
from flask import Flask
import yt_dlp
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit
from schedules.folder_cleanup import folder_cleanup  # Import the folder_cleanup function

app = Flask(__name__)

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


# setup scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=folder_cleanup, trigger=CronTrigger.from_crontab('* * * * *')) 
scheduler.start()
    
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


if __name__ == "__main__":
    app.run(debug=True)
