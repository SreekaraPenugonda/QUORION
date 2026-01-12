import qrcode
import os
from PIL import Image

def generate_qr(data, category, filename,
                size=10, file_format="png",
                fill_color="black", back_color="white",
                logo_path=None,
                save_in_static=False):
    """
    Generates a QR code with optional logo and custom colors.
    """

    # Decide folder
    if save_in_static:
        output_dir = os.path.join("static", "qrcodes")
    else:
        output_dir = os.path.join("output", category)
    os.makedirs(output_dir, exist_ok=True)

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        box_size=size,
        border=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H  # high error correction for logo
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')

    # Add logo if provided
    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path)
        qr_width, qr_height = img.size

        # Resize logo (20% of QR size)
        factor = 4
        size_logo = qr_width // factor
        logo = logo.resize((size_logo, size_logo), Image.Resampling.LANCZOS)

        # Position logo at center
        pos = ((qr_width - size_logo) // 2, (qr_height - size_logo) // 2)
        img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

    # Safe filename
    filename = filename.strip().replace(" ", "_")
    final_path = os.path.join(output_dir, f"{filename}.{file_format}")

    # Prevent overwrite
    counter = 1
    while os.path.exists(final_path):
        final_path = os.path.join(
            output_dir,
            f"{filename}_{counter}.{file_format}"
        )
        counter += 1

    img.save(final_path)
    return final_path
