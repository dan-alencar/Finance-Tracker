import argparse
import os
import tempfile
from PIL import Image
from sec import encode_message, decode_message

VALID_FORMATS = (".png", ".bmp", ".jpg", ".jpeg")

def convert_to_png_if_needed(image_path):
    ext = os.path.splitext(image_path.lower())[1]
    if ext in [".jpg", ".jpeg"]:
        print("⚠️  JPEG detected. Converting to PNG...")
        img = Image.open(image_path)
        temp_path = tempfile.mktemp(suffix=".png")
        img.save(temp_path, format="PNG")
        return temp_path
    return image_path

def main():
    parser = argparse.ArgumentParser(description="Steganography tool for Finance Tracker")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Encode
    encode_parser = subparsers.add_parser("encode", help="Encode a message into an image")
    encode_parser.add_argument("input_image", help="Input image file (PNG/BMP/JPG)")
    encode_parser.add_argument("output_image", help="Output image file (must be PNG or BMP)")
    encode_parser.add_argument("message", help="Message to encode")

    # Decode
    decode_parser = subparsers.add_parser("decode", help="Decode a message from an image")
    decode_parser.add_argument("image", help="Image file to decode from (PNG/BMP/JPG)")

    args = parser.parse_args()

    if args.command == "encode":
        input_path = convert_to_png_if_needed(args.input_image)

        output_ext = os.path.splitext(args.output_image.lower())[1]
        if output_ext not in [".png", ".bmp"]:
            print("❌ Output image must be PNG or BMP.")
            return

        encode_message(input_path, args.output_image, args.message)
        print(f"✅ Message encoded into {args.output_image}")

    elif args.command == "decode":
        image_path = convert_to_png_if_needed(args.image)
        msg = decode_message(image_path)
        print(f"🔓 Decoded message: {msg if msg else '[No valid message found]'}")

if __name__ == "__main__":
    main()
