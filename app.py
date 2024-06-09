from flask import Flask, render_template, request, url_for, send_file, redirect, session
from flask_sqlalchemy import SQLAlchemy
from pytube import YouTube
import os

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Set a secret key for session management

# Configuration for the SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy database
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    download_count = db.Column(db.Integer, default=0)
    download_history = db.relationship('DownloadHistory', backref='user', lazy=True)

# Define the DownloadHistory model
class DownloadHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Define the download limit
download_limit = 5

# Route for the home page
@app.route('/')
def index():
    if 'download_count' not in session:
        session['download_count'] = 0

    remaining_downloads = max(download_limit - session['download_count'], 0)
    return render_template('index.html', remaining_downloads=remaining_downloads)

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('signup.html', error="Username already exists")
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        return redirect(url_for('index'))
    return render_template('signup.html')

# Route for converting YouTube video to MP3
@app.route('/convert', methods=['POST'])
def convert_to_mp3():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    if user.download_count >= download_limit:
        remaining_downloads = 0
        return render_template('index.html', error="Download limit reached. You can't download more than 5 files.", remaining_downloads=remaining_downloads)

    video_url = request.form['video_url']

    try:
        yt = YouTube(video_url)
        video = yt.streams.filter(only_audio=True).first()
        filename = f"{yt.title}.mp3"
        temp_dir = 'temp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        filepath = os.path.join(temp_dir, filename)
        video.download(output_path=temp_dir, filename=filename)

        user.download_count += 1
        db.session.commit()

        download_history = DownloadHistory(filename=filename, user_id=user_id)
        db.session.add(download_history)
        db.session.commit()

        mp3_url = url_for('download_file', filename=filename)
        remaining_downloads = download_limit - user.download_count
        return render_template('download.html', mp3_url=mp3_url, remaining_downloads=remaining_downloads)
    except Exception as e:
        remaining_downloads = download_limit - user.download_count
        return render_template('index.html', error=f"An error occurred: {str(e)}", remaining_downloads=remaining_downloads)

# Route for downloading the MP3 file
@app.route('/download/<filename>')
def download_file(filename):
    temp_dir = 'temp'
    filepath = os.path.join(temp_dir, filename)
    return send_file(filepath, as_attachment=True)

# Route for the dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    download_history = DownloadHistory.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', download_history=download_history, username=user.username)

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

# Function to create database tables
def create_tables():
    with app.app_context():
        db.create_all()

# Run the Flask application
if __name__ == '__main__':
    create_tables()  # Ensure tables are created before the app starts
    app.run(host='0.0.0.0', debug=True)
