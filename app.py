from flask import Flask, request, send_file
from pydub import AudioSegment
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "API Conversor 432Hz Online"

@app.route("/convert", methods=["POST"])
def convert():
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]
    input_path = "input.mp3"
    output_path = "output.mp3"

    file.save(input_path)

    sound = AudioSegment.from_file(input_path)

    # Ajuste aproximado 440 → 432
    new_sample_rate = int(sound.frame_rate * (432.0 / 440.0))
    shifted_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    shifted_sound = shifted_sound.set_frame_rate(sound.frame_rate)

    shifted_sound.export(output_path, format="mp3")

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
