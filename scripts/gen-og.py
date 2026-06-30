from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
img = Image.new("RGB", (W, H), "#0a0a0a")
draw = ImageDraw.Draw(img)

# Background glow
for cx, cy, r, color in [
    (180, 300, 380, "#00d4aa"),
    (1020, 330, 350, "#f59e0b"),
    (600, 630, 500, "#00d4aa"),
]:
    for i in range(50, 0, -1):
        alpha = int(6 * (1 - i / 50))
        x0 = cx - r * i // 50
        y0 = cy - r * i // 50
        x1 = cx + r * i // 50
        y1 = cy + r * i // 50
        draw.ellipse([x0, y0, x1, y1], fill=color + hex(alpha)[2:].zfill(2))

# Font setup
font_path = None
for fp in ["/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/HelveticaNeue.ttc"]:
    if os.path.exists(fp):
        font_path = fp
        break

if not font_path:
    raise SystemExit("No font found")

# Large "GP"
font_gp = ImageFont.truetype(font_path, 200)
gp_text = "GP"
bbox = draw.textbbox((0, 0), gp_text, font=font_gp)
gp_w = bbox[2] - bbox[0]
gp_h = bbox[3] - bbox[1]
gp_x = 80
gp_y = 140
draw.text((gp_x, gp_y), gp_text, fill="#ffffff", font=font_gp)

# "TRADING" next to GP
font_trading = ImageFont.truetype(font_path, 130)
tr_text = "TRADING"
bbox2 = draw.textbbox((0, 0), tr_text, font=font_trading)
tr_w = bbox2[2] - bbox2[0]
tr_h = bbox2[3] - bbox2[1]
tr_x = gp_x + gp_w + 20
tr_y = gp_y + 30
draw.text((tr_x, tr_y), tr_text, fill="#ffffff", font=font_trading)

# Subtitle below
font_sub = ImageFont.truetype(font_path, 40)
sub = "SUITE PREMIUM NINJATRADER 8"
bbox3 = draw.textbbox((0, 0), sub, font=font_sub)
sw = bbox3[2] - bbox3[0]
sx = gp_x
sy = gp_y + gp_h + 15
draw.text((sx, sy), sub, fill="#d1d5db", font=font_sub)

# Gold underline
line_y = sy + 50
draw.rectangle([(gp_x, line_y), (gp_x + 180, line_y + 4)], fill="#f59e0b")

# Tagline
font_tag = ImageFont.truetype(font_path, 26)
tag = "Order Flow  ·  Copy Trading  ·  Algoritmos Predictivos"
bbox4 = draw.textbbox((0, 0), tag, font=font_tag)
tw = bbox4[2] - bbox4[0]
tx = gp_x
ty = line_y + 22
draw.text((tx, ty), tag, fill="#6b7280", font=font_tag)

# URL bottom right
font_url = ImageFont.truetype(font_path, 28)
url = "gptradingfx.pages.dev"
bbox5 = draw.textbbox((0, 0), url, font=font_url)
uw = bbox5[2] - bbox5[0]
ux = W - uw - 40
uy = H - 50
draw.text((ux, uy), url, fill="#4b5563", font=font_url)

# Draw logo-like circle
logo_cx, logo_cy, logo_r = 1120, 90, 45
for i in range(30, 0, -1):
    alpha = int(5 * (1 - i / 30))
    r2 = logo_r * i // 30
    draw.ellipse([logo_cx - r2, logo_cy - r2, logo_cx + r2, logo_cy + r2],
                 fill="#00d4aa" + hex(alpha)[2:].zfill(2))
draw.ellipse([logo_cx - 15, logo_cy - 15, logo_cx + 15, logo_cy + 15],
             fill="#00d4aa")

out = "/Users/macbookpro/gp-trading-site/public/og-image.png"
img.save(out, "PNG")
print(f"OG image saved: {out} ({os.path.getsize(out)} bytes)")
