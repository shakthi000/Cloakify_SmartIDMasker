import pytesseract
from pytesseract import Output
import cv2
import re
import os
from werkzeug.utils import secure_filename

# Sensitive patterns
patterns = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),  # SSN
    re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),  # Email
    re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"),  # Phone
    re.compile(r"\b\d{5}(?:-\d{4})?\b"),  # ZIP
    re.compile(r"\b\d{6,}\b"),  # Long numbers
]

keywords = ["name", "dob", "birth", "address", "city", "state", "country", "passport", "license", "id"]

def is_sensitive(word):
    if any(p.search(word) for p in patterns):
        return True
    if any(kw.lower() in word.lower() for kw in keywords):
        return True
    return False

def blur_area(img, x, y, w, h):
    roi = img[y:y+h, x:x+w]
    if roi.size > 0:
        img[y:y+h, x:x+w] = cv2.GaussianBlur(roi, (51, 51), 0)
    return img

def blackout_area(img, x, y, w, h):
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 0), -1)
    return img

def process_image(img_path, output_path, mask_type):
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError("Could not load image.")

    data = pytesseract.image_to_data(img, output_type=Output.DICT)
    for i, word in enumerate(data["text"]):
        if word.strip() and is_sensitive(word):
            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            if mask_type == "black":
                img = blackout_area(img, x, y, w, h)
            else:
                img = blur_area(img, x, y, w, h)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    if not cv2.imwrite(output_path, img):
        raise RuntimeError("Could not save masked image.")

def process_file(filepath, mask_type):
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in [".png", ".jpg", ".jpeg", ".tiff"]:
        raise ValueError("Unsupported file type.")

    output_dir = "static/output"
    os.makedirs(output_dir, exist_ok=True)

    safe_filename = secure_filename(os.path.basename(filepath))
    output_path = os.path.join(output_dir, f"masked_{safe_filename}")

    process_image(filepath, output_path, mask_type)
    return output_path
