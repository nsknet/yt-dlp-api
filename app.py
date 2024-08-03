import os
from zoneinfo import ZoneInfo
from flask import Flask
import pytz
import yt_dlp
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit
from schedules.folder_cleanup import folder_cleanup  # Import the folder_cleanup function
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Import API endpoints
from api import get_download_info, start_download, session_status, download_file, get_download_json
from pages import index
from pages.p404 import bp as p404

# Register API endpoints
app.register_blueprint(get_download_info.bp)
app.register_blueprint(start_download.bp)
app.register_blueprint(session_status.bp)
app.register_blueprint(download_file.bp)
app.register_blueprint(get_download_json.bp)
app.register_blueprint(index.bp)

# Register the index blueprint to handle un-routed URLs
app.register_blueprint(p404)


# setup scheduler
# Set the TZ environment variable
os.environ['TZ'] = 'Europe/Berlin' 

# Explicitly set the timezone in the zoneinfo module
timezone = ZoneInfo(os.environ['TZ'])
scheduler = BackgroundScheduler(timezone=timezone)
scheduler.add_job(func=folder_cleanup, trigger=CronTrigger.from_crontab('* * * * *')) 
scheduler.start()
    
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


if __name__ == "__main__":
    app.run(debug=True)
