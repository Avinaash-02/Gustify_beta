import os
from flask import Flask ,render_template,jsonify,request,redirect


app = Flask(__name__)
MUSIC_DIR = "static/music"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["UPLOAD_FOLDER"] = MUSIC_DIR
app.config["MAX_CONTENT_LENGTH" ] = 20*1024*1024
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response
def  get_mp3_files():
    return [file for file in os.listdir(MUSIC_DIR)if file.endswith(".mp3")]
@app.route("/")
def home():
    songs = get_mp3_files()
    return render_template("index.html",songs = songs)
@app.route("/play/<song>")
def play(song):
    return jsonify({"song":song})
@app.route("/control/<cmd>")
def control(cmd):
    return jsonify({"command":cmd})
#Upload code

@app.route("/upload",methods = ["POST"])#Doubt check with gpt
def upload():
    if "file" not in request.files:
        return redirect("/")

    file = request.files["file"]
    if file.filename == "":
        return redirect("/")
    if file and file.filename.lower().endswith(".mp3"):
        save_path = os.path.join(app.config["UPLOAD_FOLDER"],file.filename)
        file.save(save_path)
    return redirect("/")
if __name__ == "__main__":
    if not os.path.exists(MUSIC_DIR):
        os.makedirs(MUSIC_DIR)
    app.run(debug=True)

