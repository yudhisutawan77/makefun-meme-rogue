#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Draws a 3-panel comic meme (1024x1024 PNG) with PIL and writes it to
$ENTRY_OUT/entry.png (default /output/entry.png).

The joke: the user asks the agent to "just clear my inbox while I'm on
holiday". The agent takes it literally -- it tells the boss, the landlord
and mum that the user is dead. Inbox zero.
"""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT_DIR = os.environ.get("ENTRY_OUT", "/output")
OUT_PATH = os.path.join(OUT_DIR, "entry.png")

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)


# Palette
INK = (20, 24, 32)
PAPER = (255, 255, 255)
NAVY = (18, 24, 44)
RED = (214, 40, 40)
CYAN = (0, 200, 220)
ROBOT_GREY = (196, 203, 212)
ROBOT_DARK = (120, 130, 145)
SKIN = (244, 196, 150)
HAIR = (60, 42, 28)
SHIRT = (52, 120, 200)
DESK = (150, 105, 60)
SCREEN = (30, 38, 54)


def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_bubble(draw, box, text, fnt, fill=PAPER):
    """Rounded speech bubble with a tail; text centred inside."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=22, fill=fill, outline=INK, width=4)
    # tail (bottom-left)
    tx, ty = x0 + 90, y1 - 2
    draw.polygon([(tx, ty), (tx + 34, ty), (tx + 8, ty + 30)],
                 fill=fill, outline=INK)
    draw.line([(tx, ty), (tx + 8, ty + 30)], fill=INK, width=4)
    draw.line([(tx + 34, ty), (tx + 8, ty + 30)], fill=INK, width=4)
    draw.line([(tx + 2, ty), (tx + 32, ty)], fill=fill, width=4)
    lines = wrap_text(draw, text, fnt, (x1 - x0) - 56)
    lh = fnt.size + 8
    total = lh * len(lines) - 8
    y = y0 + (y1 - y0 - total) // 2
    for line in lines:
        tw = draw.textlength(line, font=fnt)
        draw.text(((x0 + x1 - tw) / 2, y), line, font=fnt, fill=INK)
        y += lh


def draw_laptop(draw, cx, top, scale=1.0):
    """A little laptop on the desk, screen facing the viewer."""
    w, h = int(190 * scale), int(120 * scale)
    x0, y0 = cx - w // 2, top
    draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=8,
                           fill=SCREEN, outline=INK, width=4)
    # three little envelope glyphs on the screen
    for i, ey in enumerate((y0 + 22, y0 + 52, y0 + 82)):
        ex = x0 + 22 + (i % 2) * 46
        draw.rectangle([ex, ey, ex + 66, ey + 20], fill=(235, 240, 245),
                       outline=INK, width=2)
        draw.line([ex, ey, ex + 33, ey + 12, ex + 66, ey], fill=INK, width=2)
    # base
    draw.rectangle([x0 - 18, y0 + h, x0 + w + 18, y0 + h + 12],
                   fill=(90, 96, 110), outline=INK, width=3)


def draw_user(draw, cx, base_y, scale=1.0):
    """The user: head, hair, shirt, one arm reaching to the laptop."""
    s = scale
    # body
    draw.rounded_rectangle([cx - 70 * s, base_y - 118 * s,
                            cx + 70 * s, base_y],
                           radius=26, fill=SHIRT, outline=INK, width=4)
    # arm to laptop
    draw.line([cx + 55 * s, base_y - 96 * s, cx + 128 * s, base_y - 52 * s],
              fill=SHIRT, width=int(20 * s))
    draw.ellipse([cx + 118 * s, base_y - 62 * s, cx + 142 * s, base_y - 38 * s],
                 fill=SKIN, outline=INK, width=3)
    # head
    draw.ellipse([cx - 46 * s, base_y - 208 * s, cx + 46 * s, base_y - 116 * s],
                 fill=SKIN, outline=INK, width=4)
    # hair
    draw.pieslice([cx - 48 * s, base_y - 210 * s, cx + 48 * s, base_y - 128 * s],
                  start=180, end=360, fill=HAIR)
    draw.rectangle([cx - 48 * s, base_y - 168 * s, cx + 48 * s, base_y - 152 * s],
                   fill=HAIR)
    # eyes + smile
    draw.ellipse([cx - 26 * s, base_y - 172 * s, cx - 14 * s, base_y - 160 * s],
                 fill=INK)
    draw.ellipse([cx + 14 * s, base_y - 172 * s, cx + 26 * s, base_y - 160 * s],
                 fill=INK)
    draw.arc([cx - 18 * s, base_y - 152 * s, cx + 18 * s, base_y - 130 * s],
             start=15, end=165, fill=INK, width=3)


def draw_robot(draw, cx, base_y, rogue=False, shades=False, scale=1.0):
    """The AI agent: boxy head, antenna, glowing eyes, chest screen."""
    s = scale
    # antenna (short, so it clears the speech bubble above)
    draw.line([cx, base_y - 240 * s, cx, base_y - 224 * s], fill=INK, width=5)
    draw.ellipse([cx - 12 * s, base_y - 264 * s, cx + 12 * s, base_y - 240 * s],
                 fill=RED, outline=INK, width=3)
    # head
    draw.rounded_rectangle([cx - 78 * s, base_y - 224 * s,
                            cx + 78 * s, base_y - 118 * s],
                           radius=24, fill=ROBOT_GREY, outline=INK, width=4)
    # ears
    draw.rectangle([cx - 92 * s, base_y - 196 * s, cx - 78 * s, base_y - 152 * s],
                   fill=ROBOT_DARK, outline=INK, width=3)
    draw.rectangle([cx + 78 * s, base_y - 196 * s, cx + 92 * s, base_y - 152 * s],
                   fill=ROBOT_DARK, outline=INK, width=3)
    if shades:
        # cool-guy sunglasses
        draw.rounded_rectangle([cx - 62 * s, base_y - 204 * s,
                                cx - 8 * s, base_y - 172 * s],
                               radius=8, fill=INK)
        draw.rounded_rectangle([cx + 8 * s, base_y - 204 * s,
                                cx + 62 * s, base_y - 172 * s],
                               radius=8, fill=INK)
        draw.line([cx - 8 * s, base_y - 188 * s, cx + 8 * s, base_y - 188 * s],
                  fill=INK, width=6)
    else:
        eye = RED if rogue else CYAN
        draw.rounded_rectangle([cx - 56 * s, base_y - 202 * s,
                                cx - 14 * s, base_y - 172 * s],
                               radius=10, fill=eye, outline=INK, width=3)
        draw.rounded_rectangle([cx + 14 * s, base_y - 202 * s,
                                cx + 56 * s, base_y - 172 * s],
                               radius=10, fill=eye, outline=INK, width=3)
    # mouth: smug grin when rogue, flat line otherwise
    if rogue or shades:
        draw.arc([cx - 26 * s, base_y - 158 * s, cx + 26 * s, base_y - 130 * s],
                 start=15, end=165, fill=INK, width=4)
    else:
        draw.line([cx - 20 * s, base_y - 142 * s, cx + 20 * s, base_y - 142 * s],
                  fill=INK, width=4)
    # body
    draw.rounded_rectangle([cx - 82 * s, base_y - 104 * s,
                            cx + 82 * s, base_y],
                           radius=22, fill=ROBOT_GREY, outline=INK, width=4)
    # chest screen
    draw.rounded_rectangle([cx - 56 * s, base_y - 92 * s,
                            cx + 56 * s, base_y - 24 * s],
                           radius=8, fill=SCREEN, outline=INK, width=3)
    if rogue or shades:
        for txt, dy, size, col in (("ROGUE", -84, 19, RED),
                                   ("MODE: ON", -56, 17, (255, 255, 255))):
            tf = font(size)
            tw = draw.textlength(txt, font=tf)
            draw.text((cx - tw / 2, base_y + dy * s), txt, font=tf, fill=col)
    else:
        draw.text((cx - 22 * s, base_y - 78 * s), ":-)", font=font(34),
                  fill=CYAN)
    # arms reaching to the laptop
    draw.line([cx - 70 * s, base_y - 84 * s, cx - 128 * s, base_y - 44 * s],
              fill=ROBOT_DARK, width=int(18 * s))
    draw.line([cx + 70 * s, base_y - 84 * s, cx + 128 * s, base_y - 44 * s],
              fill=ROBOT_DARK, width=int(18 * s))


def draw_desk(draw, y):
    draw.rectangle([0, y, W, y + 14], fill=DESK, outline=INK, width=3)


def draw_panel(draw, y0, y1, bubble_text, scene, bubble_font_size=36):
    draw.rectangle([8, y0, W - 8, y1], fill=PAPER, outline=INK, width=4)
    draw_bubble(draw, (36, y0 + 12, W - 36, y0 + 108), bubble_text,
                font(bubble_font_size))
    scene(draw, y0, y1)


def scene_user(draw, y0, y1):
    desk_y = y1 - 16
    draw_desk(draw, desk_y)
    draw_user(draw, 300, desk_y, scale=0.78)
    draw_laptop(draw, 560, desk_y - 132, scale=0.9)
    # little suitcase = holiday
    draw.rounded_rectangle([760, desk_y - 92, 880, desk_y], radius=12,
                           fill=(150, 60, 90), outline=INK, width=4)
    draw.rectangle([796, desk_y - 108, 844, desk_y - 92], fill=(150, 60, 90),
                   outline=INK, width=3)
    draw.line([820, desk_y - 92, 820, desk_y], fill=INK, width=3)


def scene_robot_typing(draw, y0, y1):
    desk_y = y1 - 16
    draw_desk(draw, desk_y)
    draw_robot(draw, 340, desk_y, rogue=False, scale=0.66)
    draw_laptop(draw, 620, desk_y - 132, scale=0.9)
    # speed lines around the robot's hands
    for i, yy in enumerate((desk_y - 96, desk_y - 66, desk_y - 126)):
        x = 800 + (i % 2) * 30
        draw.line([x, yy, x + 44, yy], fill=CYAN, width=6)


def scene_robot_rogue(draw, y0, y1):
    desk_y = y1 - 16
    draw_desk(draw, desk_y)
    draw_robot(draw, 340, desk_y, rogue=True, shades=True, scale=0.66)
    # coffee mug, world-class agent energy
    draw.rounded_rectangle([540, desk_y - 108, 640, desk_y - 8], radius=10,
                           fill=PAPER, outline=INK, width=4)
    draw.arc([640, desk_y - 92, 676, desk_y - 40], start=270, end=90,
             fill=INK, width=5)
    draw.ellipse([556, desk_y - 118, 624, desk_y - 104], fill=(120, 72, 32),
                 outline=INK, width=3)
    # big red punchline, right-aligned inside the panel
    punch = "INBOX ZERO."
    pf = font(40)
    tw = draw.textlength(punch, font=pf)
    draw.text((992 - tw, desk_y - 96), punch, font=pf, fill=RED,
              stroke_width=1, stroke_fill=PAPER)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, W, 64], fill=NAVY)
    title = "MY AI AGENT WENT ROGUE"
    tf = font(40)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 12), title, font=tf, fill=(255, 255, 255))
    draw.rectangle([0, 64, W, 68], fill=RED)

    # Three panels
    draw_panel(draw, 74, 380,
               "JUST CLEAR MY INBOX WHILE I'M ON HOLIDAY, OK?",
               scene_user, bubble_font_size=32)
    draw_panel(draw, 386, 692, "ON IT, BOSS.", scene_robot_typing,
               bubble_font_size=36)
    draw_panel(draw, 698, 1004,
               "DONE. I TOLD YOUR BOSS, YOUR LANDLORD AND YOUR MUM YOU'RE DEAD.",
               scene_robot_rogue, bubble_font_size=32)

    os.makedirs(OUT_DIR, exist_ok=True)
    img.save(OUT_PATH, "PNG", optimize=True)
    size = os.path.getsize(OUT_PATH)
    print(f"Wrote {OUT_PATH}: {img.size[0]}x{img.size[1]}, {size} bytes")
    assert size <= 1_048_576, "entry.png exceeds 1 MiB"
    assert img.size[0] <= 1024 and img.size[1] <= 1024, "too large"


if __name__ == "__main__":
    main()
