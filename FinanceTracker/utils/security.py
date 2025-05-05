from tkinter import filedialog, Tk
from PIL import Image

def get_security_key_from_image():
    """Prompt for an image file and extract the first 256 LSBs of RGB channels."""
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select security image")
    root.destroy()

    if not file_path:
        return None  # Gracefully return None if user cancels

    img = Image.open(file_path)
    pixels = list(img.getdata())
    bits = []

    for pixel in pixels:
        for channel in pixel[:3]:  # Only RGB (ignore alpha)
            bits.append(str(channel & 1))
            if len(bits) == 256:
                return ''.join(bits)

    raise ValueError("Image too small to extract 256 LSBs.")
