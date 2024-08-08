from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import shutil


def authenticate():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json")

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("credentials.json")
    return GoogleDrive(gauth)


def upload_files(drive):
    result_dir = "result"
    uploaded_dir = "uploaded"

    if not os.path.exists(uploaded_dir):
        os.makedirs(uploaded_dir)

    for filename in os.listdir(result_dir):
        file_path = os.path.join(result_dir, filename)
        if os.path.isfile(file_path):
            # Create a new file in Google Drive with the same name as the local file
            gfile = drive.CreateFile(
                {
                    "title": filename,
                    "parents": [{"id": "15t1-TcjMEilfFH2w9WDO0lZP6syDFGZe"}],
                }
            )
            gfile.SetContentFile(file_path)
            gfile.Upload()
            print(f"Uploaded: {filename}")
            shutil.move(file_path, os.path.join(uploaded_dir, filename))
            print(f"Moved: {filename} to {uploaded_dir}")
