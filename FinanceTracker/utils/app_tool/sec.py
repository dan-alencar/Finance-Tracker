from PIL import Image

def encode_message(image_path, output_path, message):
    """Encodes a message into the LSBs of the image and saves a new image."""
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = list(img.getdata())

    # Convert message to bits and add end marker
    message += "<EOF>"
    bits = ''.join(f'{ord(c):08b}' for c in message)

    if len(bits) > len(pixels) * 3:
        raise ValueError("Image too small to hold the message.")

    new_pixels = []
    bit_index = 0
    for pixel in pixels:
        r, g, b = pixel
        if bit_index < len(bits):
            r = (r & ~1) | int(bits[bit_index])
            bit_index += 1
        if bit_index < len(bits):
            g = (g & ~1) | int(bits[bit_index])
            bit_index += 1
        if bit_index < len(bits):
            b = (b & ~1) | int(bits[bit_index])
            bit_index += 1
        new_pixels.append((r, g, b))
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    new_img.save(output_path)


def decode_message(image_path):
    """Extracts the hidden message from the LSBs of the image."""
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = list(img.getdata())

    bits = []
    for pixel in pixels:
        for channel in pixel[:3]:
            bits.append(str(channel & 1))

    chars = [chr(int(''.join(bits[i:i+8]), 2)) for i in range(0, len(bits), 8)]
    message = ''.join(chars)

    if "<EOF>" in message:
        return message.split("<EOF>")[0]
    return None

