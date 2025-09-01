from flask import Flask, request, render_template, url_for
from processor import process_file
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tiff"}

def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload():
    preview_imgs = []
    download_url = None
    error = None

    if request.method == "POST":
        if "file" not in request.files or request.files["file"].filename == "":
            error = "No file uploaded."
        else:
            file = request.files["file"]
            if not allowed_file(file.filename):
                error = "Unsupported file type. Use PNG/JPG/TIFF."
            else:
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                mask_type = request.form.get("mask_type", "blur")
                try:
                    output_path = process_file(filepath, mask_type)
                    preview_url = url_for("static", filename="output/" + os.path.basename(output_path))
                    preview_imgs = [preview_url]
                    download_url = preview_url
                except Exception as e:
                    error = f"Processing failed: {str(e)}"

    return render_template(
        "index.html",
        preview_imgs=preview_imgs,
        download_url=download_url,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
