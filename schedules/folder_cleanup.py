import os
import time
import uuid

def folder_cleanup():
    session_id = str(uuid.uuid4())
    print(f"Scheduled task is running, session ID: {session_id}")
    
    # Define the folders to be cleaned up
    folders_to_cleanup = ['status', 'output']
    # Calculate the cutoff time (2 hours ago)
    cutoff_time = time.time() - (2 * 60 * 60)  # 2 hours in seconds

    for folder in folders_to_cleanup:
        folder_path = os.path.join(os.getcwd(), folder)
        if not os.path.exists(folder_path):
            print(f"Folder {folder_path} does not exist.")
            continue

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    file_creation_time = os.path.getctime(file_path)
                    if file_creation_time < cutoff_time:
                        os.unlink(file_path)
                        print(f"Deleted file: {file_path}")
                elif os.path.isdir(file_path):
                    dir_creation_time = os.path.getctime(file_path)
                    if dir_creation_time < cutoff_time:
                        shutil.rmtree(file_path)
                        print(f"Deleted directory: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    print(f"Folder cleanup completed, session ID: {session_id}")
