from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    mensagem = ""
    filename = None

    if request.method == "POST":
        url = request.form["url"]
        formato = request.form["formato"]

        if formato == "video":
            opcoes = {
                'format': '18',
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            }
        else:
            opcoes = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

        try:
            with yt_dlp.YoutubeDL(opcoes) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                mensagem = "✅ Download pronto!"
                filename = os.path.basename(filename).replace(".webm", ".mp3").replace(".m4a", ".mp3")
        except Exception as e:
            mensagem = f"❌ Erro: {str(e)}"

    return render_template("index.html", mensagem=mensagem, filename=filename)

@app.route("/downloads/<path:filename>")
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
