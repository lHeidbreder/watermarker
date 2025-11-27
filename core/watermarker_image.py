from PIL import Image, ImageDraw, ImageFont

# Tiled
def add_watermark(
    input_path,
    output_path,
    text="Placeholder",
    opacity=128,
    color=(255, 255, 255)
):
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size

    # Create overlay for watermark
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Measure text
    font = ImageFont.load_default()
    text_w, text_h = draw.textsize(text, font=font)

    text_img = Image.new("RGBA", (text_w, text_h), (0, 0, 0, 0))
    ImageDraw.Draw(text_img).text((0, 0), text, font=font, fill=color + (opacity,))

    # Rotate text 45 degrees
    rotated = text_img.rotate(45, expand=1)

    # Tile the rotated text over the overlay
    rx, ry = rotated.size
    step_x = int(rx * 1.5)
    step_y = int(ry * 1.5)

    for x in range(0, width, step_x):
        for y in range(0, height, step_y):
            overlay.paste(rotated, (x, y), rotated)

    watermarked = Image.alpha_composite(img, overlay)
    watermarked.convert("RGB").save(output_path)
