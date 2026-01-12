from qr_generator import generate_qr

def main():
    print("\nSMART QR GENERATOR\n")

    # -------------------------
    # Choose QR Category
    # -------------------------
    print("Choose QR Type:")
    print("1. Website / Menu / PDF")
    print("2. WiFi")
    print("3. Social Media")
    print("4. Contact")
    print("5. Plain Text")

    choice = input("Enter choice (1-5): ").strip()

    # -------------------------
    # Prepare Data
    # -------------------------
    if choice == "1":
        category = "website"
        data = input("Enter website / menu / PDF URL: ").strip()
        if not data:
            print("Error: URL cannot be empty.")
            return

    elif choice == "2":
        category = "wifi"
        ssid = input("Enter WiFi Name (SSID): ").strip()
        password = input("Enter WiFi Password: ").strip()
        security = input("Security type (WPA/WEP/none): ").strip().upper()

        if not ssid:
            print("Error: WiFi name cannot be empty.")
            return

        if security == "NONE":
            security = ""

        data = f"WIFI:T:{security};S:{ssid};P:{password};;"

    elif choice == "3":
        category = "social"
        platform = input("Enter platform (instagram / twitter / linkedin): ").strip().lower()
        username = input("Enter username: ").strip()

        if not platform or not username:
            print("Error: Platform and username required.")
            return

        base_urls = {
            "instagram": "https://instagram.com/",
            "twitter": "https://twitter.com/",
            "linkedin": "https://linkedin.com/in/"
        }

        if platform not in base_urls:
            print("Unsupported social platform.")
            return

        data = base_urls[platform] + username

    elif choice == "4":
        category = "contact"
        name = input("Enter name: ").strip()
        phone = input("Enter phone number: ").strip()
        email = input("Enter email: ").strip()

        if not name:
            print("Error: Name is required.")
            return

        data = (
            "BEGIN:VCARD\n"
            "VERSION:3.0\n"
            f"FN:{name}\n"
            f"TEL:{phone}\n"
            f"EMAIL:{email}\n"
            "END:VCARD"
        )

    elif choice == "5":
        category = "text"
        data = input("Enter text: ").strip()
        if not data:
            print("Error: Text cannot be empty.")
            return

    else:
        print("Invalid choice.")
        return

    # -------------------------
    # File & QR Settings
    # -------------------------
    filename = input("Enter output file name (without extension): ").strip().replace(" ", "_")

    try:
        box_size = int(input("Enter QR size (5–15 recommended): "))
        if box_size <= 0:
            raise ValueError
    except ValueError:
        box_size = 10

    img_format = input("Choose image format (png / jpg): ").strip().lower()
    if img_format not in ["png", "jpg"]:
        img_format = "png"

    fill_color = input("Enter QR color (default: black): ").strip() or "black"
    back_color = input("Enter background color (default: white): ").strip() or "white"

    # -------------------------
    # Generate QR
    # -------------------------
    saved_path = generate_qr(
        data=data,
        category=category,
        filename=filename,
        box_size=box_size,
        img_format=img_format,
        fill_color=fill_color,
        back_color=back_color
    )

    print(f"\n✅ QR Code successfully saved at:\n{saved_path}\n")


if __name__ == "__main__":
    main()
