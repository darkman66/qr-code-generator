"""
Usage: python qr_badge.py <url> [text] [-o output.png]
Example: python qr_badge.py https://example.com "SCAN ME" -o badge.png

Requires: pip install qrcode[pil] pillow
"""
import argparse
import qrcode
from qrcode.constants import ERROR_CORRECT_M
from PIL import Image, ImageDraw, ImageFont


def load_font(size):
    for name in ("arial.ttf", "Arial.ttf", "DejaVuSans.ttf",
                 "/System/Library/Fonts/Helvetica.ttc",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                 "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_mini_icon(d, cx, cy, s):
    """Small QR-like icon: corner brackets plus little squares."""
    h = s // 2
    w = max(2, s // 12)
    L = s // 3
    # corner brackets
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = cx + sx * h, cy + sy * h
            d.line([(x, y), (x - sx * L, y)], fill="black", width=w)
            d.line([(x, y), (x, y - sy * L)], fill="black", width=w)
    # inner squares
    q = s // 5
    for dx, dy in ((-1, -1), (1, -1), (-1, 1)):
        x, y = cx + dx * q * 1.1, cy + dy * q * 1.1
        d.rectangle([x - q / 2, y - q / 2, x + q / 2, y + q / 2], outline="black", width=w)
    d.rectangle([cx + q * 0.6, cy + q * 0.6, cx + q * 1.4, cy + q * 1.4], fill="black")


def make_badge(url, text, out):
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=10, border=0)
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.get_image().convert("RGB")

    qr_size = 800
    qr_img = qr_img.resize((qr_size, qr_size), Image.NEAREST)

    frame = 40          # black frame thickness
    pad = 80            # white padding around QR
    box = qr_size + 2 * (pad + frame)
    W = box
    gap = 30
    pill_h = 200
    H = box + gap + pill_h

    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    # Rounded black frame with white inside
    d.rounded_rectangle([0, 0, W - 1, box - 1], radius=60, fill="black")
    d.rounded_rectangle([frame, frame, W - frame - 1, box - frame - 1], radius=35, fill="white")
    img.paste(qr_img, (frame + pad, frame + pad))

    # Pill
    py = box + gap
    d.rounded_rectangle([0, py, W - 1, py + pill_h - 1], radius=pill_h // 2, fill="black")

    # White circle with icon
    m = 20
    cd = pill_h - 2 * m
    d.ellipse([m, py + m, m + cd, py + m + cd], fill="white")
    draw_mini_icon(d, m + cd // 2, py + pill_h // 2, int(cd * 0.5))

    # Text, auto-shrunk to fit
    area_x0 = m + cd + 40
    area_x1 = W - 40
    size = 120
    font = load_font(size)
    while size > 10:
        font = load_font(size)
        bbox = d.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= area_x1 - area_x0:
            break
        size -= 4
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = area_x0 + (area_x1 - area_x0 - tw) / 2 - bbox[0]
    ty = py + (pill_h - th) / 2 - bbox[1]
    d.text((tx, ty), text, font=font, fill="white")

    img.save(out)
    print(f"Saved {out}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generate a styled QR code badge")
    p.add_argument("url", help="URL to encode")
    p.add_argument("text", nargs="?", default="SCAN ME", help="Label text")
    p.add_argument("-o", "--output", default="qr_badge.png", help="Output file")
    a = p.parse_args()
    make_badge(a.url, a.text, a.output)

