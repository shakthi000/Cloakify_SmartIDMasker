from flask import Flask, request, render_template, url_for
from processor import process_file
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload():
    preview_img = None
    download_url = None
    error = None

    if request.method == "POST":
        file = request.files.get("file")
        mask_type = request.form.get("mask_type", "blur")
        if not file or file.filename == "":
            error = "No file uploaded."
        else:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            try:
                result = process_file(filepath, mask_type)
                preview_img = url_for("static", filename="output/" + os.path.basename(result))
                download_url = preview_img
            except Exception as e:
                error = f"Processing failed: {e}"

    return render_template("index.html",
                           preview_img=preview_img,
                           download_url=download_url,
                           error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
