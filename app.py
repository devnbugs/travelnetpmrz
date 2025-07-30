import os
import json
import zipfile
from datetime import datetime
from flask import Flask, request, send_file, render_template
from PIL import Image
from fastmrz import FastMRZ
from pdf2image import convert_from_path

# === FOLDER SETUP ===
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
OUTPUT_FOLDER = 'output'

for folder in [UPLOAD_FOLDER, PROCESSED_FOLDER, OUTPUT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# === FLASK APP INIT ===
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mrz_reader = FastMRZ()

# === MRZ + RENAME ===
def extract_and_rename(filepath):
    result = {
        "passport_no": "",
        "surname": "",
        "firstname": "",
        "othername": "",
        "dob": ""
    }

    try:
        data = mrz_reader.get_details(filepath, include_checkdigit=False)

        if data and data.get("status") == "SUCCESS":
            # Required fields
            result["passport_no"] = data.get("passport_number", "").strip()
            result["dob"] = data.get("date_of_birth", "").strip()

            # Safe name parsing
            try:
                result["surname"] = data.get("surname", "").replace("<", " ").strip().upper()

                given_names = data.get("given_name", "").replace("<", " ").strip().upper()
                if given_names:
                    parts = given_names.split()
                    result["firstname"] = parts[0] if len(parts) > 0 else ""
                    result["othername"] = " ".join(parts[1:]) if len(parts) > 1 else ""
            except Exception as name_error:
                print("Name parsing failed:", name_error)
                # Name fields remain as empty strings if failed

    except Exception as e:
        print("MRZ extraction failed:", e)
        # Everything will stay as default empty values

    # === Generate safe filename ===
    name_parts = [result["surname"]]
    if result["firstname"]:
        name_parts.append(result["firstname"])
    if result["othername"]:
        name_parts.append(result["othername"])

    filename = "_".join(part for part in name_parts if part).strip("_")
    if not filename:
        filename = "UNNAMED_" + datetime.now().strftime("%Y%m%d%H%M%S")
    filename += ".jpg"

    # === Save Image ===
    try:
        img = Image.open(filepath)
        save_path = os.path.join(PROCESSED_FOLDER, filename)
        img.save(save_path, format="JPEG")
    except Exception as e:
        print("Image save error:", e)
        raise

    return save_path, result


# === INDEX + FILE UPLOAD ===
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist("files")
        if not files:
            return "No files uploaded", 400

        all_passport_data = []
        renamed_files = []

        for file in files:
            filename = file.filename.lower()
            temp_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(temp_path)

            if filename.endswith(".pdf"):
                # Convert PDF pages to images
                pages = convert_from_path(temp_path, dpi=300)
                for i, page in enumerate(pages):
                    img_path = os.path.join(UPLOAD_FOLDER, f"{os.path.splitext(filename)[0]}_page{i+1}.jpg")
                    page.save(img_path, "JPEG")

                    renamed_path, passport_info = extract_and_rename(img_path)
                    renamed_files.append(renamed_path)
                    all_passport_data.append(passport_info)
            else:
                renamed_path, passport_info = extract_and_rename(temp_path)
                renamed_files.append(renamed_path)
                all_passport_data.append(passport_info)

        # Save data.json
        data_path = os.path.join(PROCESSED_FOLDER, 'data.json')
        with open(data_path, 'w') as f:
            json.dump(all_passport_data, f, indent=2)

        # ZIP all
        zip_name = datetime.now().strftime("%Y%m%d-%H_%M") + ".zip"
        zip_path = os.path.join(OUTPUT_FOLDER, zip_name)

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in renamed_files:
                zipf.write(file_path, arcname=os.path.basename(file_path))
            zipf.write(data_path, arcname='data.json')

        return send_file(zip_path, as_attachment=True)

    return render_template('index.html')

# === START SERVER ===
if __name__ == '__main__':
    app.run(debug=True)
