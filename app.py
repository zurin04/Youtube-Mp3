from flask import Flask, render_template, request, url_for, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_to_mp3():
    video_url = request.form['video_url']

    try:
        yt = YouTube(video_url)
        video = yt.streams.filter(only_audio=True).first()
        filename = f"{yt.title}.mp3"
        temp_dir = 'temp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        filepath = os.path.join(temp_dir, filename)
        video.download(filename=filepath)
        mp3_url = url_for('download_file', filename=filename)
        return render_template('download.html', mp3_url=mp3_url)
    except Exception as e:
        return render_template('index.html', error=f"An error occurred: {str(e)}")

@app.route('/download/<filename>')
def download_file(filename):
    temp_dir = 'temp'
    filepath = os.path.join(temp_dir, filename)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
