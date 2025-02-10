from flask import Flask, render_template, request, send_file, jsonify
import os
import yt_dlp
import subprocess

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def get_video_formats(url):
    ydl_opts = {'quiet': True}
    formats = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        for f in info['formats']:
            if f.get('vcodec') != 'none' and f.get('acodec') == 'none':  # فقط الفيديو بدون صوت
                formats.append({
                    'format_id': f['format_id'],
                    'resolution': f.get('format_note', 'Unknown'),  # ✅ تجنب الخطأ إذا لم يكن هناك 'format_note'
                    'ext': f['ext']
                })
    return formats


# 🔹 تحميل الفيديو والصوت ودمجهما
def download_video(url, format_id):
    video_path = os.path.join(DOWNLOAD_FOLDER, "video.mp4")
    audio_path = os.path.join(DOWNLOAD_FOLDER, "audio.mp4")
    final_output = os.path.join(DOWNLOAD_FOLDER, "final_video.mp4")

    # تحميل الفيديو فقط
    video_opts = {
        'format': format_id,
        'outtmpl': video_path
    }
    with yt_dlp.YoutubeDL(video_opts) as ydl:
        ydl.download([url])

    # تحميل الصوت فقط
    audio_opts = {
        'format': 'bestaudio',
        'outtmpl': audio_path
    }
    with yt_dlp.YoutubeDL(audio_opts) as ydl:
        ydl.download([url])

    # دمج الفيديو والصوت باستخدام FFmpeg
    merge_command = f'ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac "{final_output}" -y'
    subprocess.run(merge_command, shell=True)

    # حذف الملفات المؤقتة
    os.remove(video_path)
    os.remove(audio_path)

    return final_output

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_formats', methods=['POST'])
def get_formats():
    url = request.form['url']
    formats = get_video_formats(url)
    return jsonify(formats)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_id = request.form['format']
    file_path = download_video(url, format_id)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)




