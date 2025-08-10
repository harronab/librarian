from PIL import Image, ImageDraw, ImageFont

# Default canvas size for a 2.13" e-paper display
DEFAULT_W, DEFAULT_H = 250, 122

def new_canvas(width=DEFAULT_W, height=DEFAULT_H):
    """Create a white 1-bit canvas and a draw helper."""
    img = Image.new("1", (width, height), 1)  # 1=white
    draw = ImageDraw.Draw(img)
    return img, draw

def measure(img):
    return img.size

def _load_font():
    # Use PIL's built-in bitmap font (portable)
    try:
        return ImageFont.load_default()
    except Exception:
        return None

def draw_2x2_buttons(draw, width, height, labels):
    """
    Draw 2 rows x 2 columns of big buttons.
    Returns list of rects [(x0,y0,x1,y1), ...] in order btn1..btn4.
    """
    assert len(labels) == 4, "Need exactly 4 labels"
    status_bar_h = 18
    area_h = height - status_bar_h
    gap = 2
    btn_w = (width - gap) // 2
    btn_h = (area_h - gap) // 2
    rects = []
    font = _load_font()

    for row in range(2):
        for col in range(2):
            idx = row * 2 + col
            x0 = col * (btn_w + gap)
            y0 = row * (btn_h + gap)
            x1 = x0 + btn_w
            y1 = y0 + btn_h

            draw.rectangle([x0, y0, x1, y1], fill=1, outline=0)

            label = labels[idx]
            tw, th = draw.textsize(label, font=font)
            cx = x0 + (btn_w - tw) // 2
            cy = y0 + (btn_h - th) // 2 - 4
            draw.text((cx, cy), label, fill=0, font=font)

            id_text = f"[btn{idx+1}]"
            itw, ith = draw.textsize(id_text, font=font)
            icx = x0 + (btn_w - itw) // 2
            icy = cy + th + 2
            draw.text((icx, icy), id_text, fill=0, font=font)

            rects.append((x0, y0, x1, y1))
    return rects

def draw_status_bar(draw, width, height, msg_text, clock_text=""):
    """Bottom bar: left = message, right = clock (12h)."""
    bar_h = 18
    y0 = height - bar_h
    draw.rectangle([0, y0, width, height], fill=1, outline=0)
    draw.line([0, y0, width, y0], fill=0)

    font = _load_font()
    if not font:
        return

    # Right-side clock
    ctw = 0
    cy = y0 + 2
    if clock_text:
        ctw, cth = draw.textsize(clock_text, font=font)
        cx = width - ctw - 4
        cy = y0 + (bar_h - cth) // 2
        draw.text((cx, cy), clock_text, fill=0, font=font)

    # Left-side message, truncated to avoid overlapping clock
    max_w = width - 8 - (ctw + 8)
    text = msg_text
    while draw.textsize(text, font=font)[0] > max_w and len(text) > 3:
        text = text[:-4] + "..."
    mx = 4
    my = cy
    draw.text((mx, my), text, fill=0, font=font)

def render_home(labels=("Check-Out","Check-In","View Patron","Print Due List"),
                status_text="Ready",
                clock_text="12:34"):
    """Render the 2x2 home screen with status bar clock."""
    img, draw = new_canvas()
    w, h = measure(img)
    rects = draw_2x2_buttons(draw, w, h, labels)
    draw_status_bar(draw, w, h, status_text, clock_text=clock_text)
    return img, rects
