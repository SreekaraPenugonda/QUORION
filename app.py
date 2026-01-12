from flask import Flask, render_template, request
from qr_generator import generate_qr
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/logos'  # temp folder for logos
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_url = None
    download_url = None

    if request.method == "POST":
        category = request.form.get("category")
        filename = request.form.get("filename", "qr_code")
        size = int(request.form.get("size", 10))
        fill_color = request.form.get("fill_color", "black")
        back_color = request.form.get("back_color", "white")
        file_format = request.form.get("file_format", "png")

        # Handle logo upload
        logo_file = request.files.get("logo")
        logo_path = None
        if logo_file and logo_file.filename != "":
            logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_file.filename)
            logo_file.save(logo_path)

        # Determine QR data based on category (same as before)
        if category == "wifi":
            ssid = request.form.get("ssid")
            password = request.form.get("password")
            security = request.form.get("security", "").upper()
            if security == "NONE":
                security = ""
            data = f"WIFI:T:{security};S:{ssid};P:{password};;"

        elif category == "contact":
            name = request.form.get("name")
            phone = request.form.get("phone")
            email = request.form.get("email")
            data = (
                "BEGIN:VCARD\n"
                "VERSION:3.0\n"
                f"FN:{name}\n"
                f"TEL:{phone}\n"
                f"EMAIL:{email}\n"
                "END:VCARD"
            )

        elif category == "social":
            platform = request.form.get("platform").lower()
            username = request.form.get("username")
            base_urls = {
                "instagram": "https://instagram.com/",
                "twitter": "https://twitter.com/",
                "linkedin": "https://linkedin.com/in/"
            }
            if platform not in base_urls:
                data = ""
            else:
                data = base_urls[platform] + username

        elif category == "website":
            data = request.form.get("data")
        else:
            data = request.form.get("data")

        # Generate QR with logo
        qr_path = generate_qr(
            data=data,
            category=category,
            filename=filename,
            size=size,
            file_format=file_format,
            fill_color=fill_color,
            back_color=back_color,
            logo_path=logo_path,
            save_in_static=True
        )

        qr_url = qr_path.replace("\\", "/")
        download_url = qr_url

        # Permanent save in output/category
        generate_qr(
            data=data,
            category=category,
            filename=filename,
            size=size,
            file_format=file_format,
            fill_color=fill_color,
            back_color=back_color,
            logo_path=logo_path,
            save_in_static=False
        )

    return render_template("index.html", qr_url=qr_url, download_url=download_url)
@app.route("/features")
def features():
    return render_template("features.html")


if __name__ == "__main__":
    app.run(debug=True)
