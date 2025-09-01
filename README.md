# Cloakify_SmartIDMasker

Cloakify is a web-based tool that automatically redacts sensitive information from images of documents, invoices, and IDs. It uses OCR (Tesseract), regex patterns, and keyword detection to blur or blackout personal data like names, DOBs, emails, phone numbers, addresses, and IDs.



# 🎯 Features

Upload images in PNG or JPG format.

Mask sensitive info with Blur (Natural) or Blackout (Solid).

Live Preview of masked images.

Download the processed images directly.

Works locally on the server, no data is stored beyond the session.



# 💻 Tech Stack

Backend: Flask (Python)

OCR: Tesseract

Image Processing: OpenCV

Regex & Keyword Detection: Python

Frontend: HTML, TailwindCSS



# ⚡ How It Works

1. Upload an image.


2. Choose mask style (blur or blackout).


3. Click Upload & Mask.


4. Watch the preview reveal the masked image.


5. Download the redacted image.



# 🛠 Setup Locally

1. Clone the repo:

git clone https://github.com/shakthi000/Cloakify_SmartIDMasker.git

cd Cloakify_SmartIDMasker

2. Install dependencies:

pip install --upgrade pip
pip install -r requirements.txt

3. Install Tesseract:

Windows: https://github.com/tesseract-ocr/tesseract

Ubuntu/Linux:

sudo apt-get update
sudo apt-get install tesseract-ocr

4. Run the app:

python app.py

5. Open in browser: http://127.0.0.1:10000



# 📂 File Structure

Cloakify_SmartIDMasker/
│
├─ app.py                 # Flask app
├─ processor.py           # Image processing & masking logic
├─ requirements.txt       # Python dependencies
├─ static/
│   ├─ uploads/           # Uploaded files
│   └─ output/            # Masked output files
├─ templates/
│   └─ index.html         # Frontend template
└─ README.md



# ⚠️ Notes

Only supports image files (PNG, JPG, JPEG, TIFF).

Maximum file size recommended: 5 MB.

Masking uses regex patterns and a keyword list—may not catch everything in complex documents.




🛡 License

MIT License © 2025 The Conquerors
