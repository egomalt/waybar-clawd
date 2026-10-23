#!/usr/bin/env python3
"""Generate Clawd's room, his animation frames and the CSS that maps classes to them.

Clawd's animations are cut from an emoji pack: one directory of PNG frames per
emoji. Point CLAWD_PACK at the directory that holds them
(default ~/clawd-emoji/frames), then run:
    python gen.py
"""
import os
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
FRAMES = HERE / "frames"
PACK = Path(os.environ.get("CLAWD_PACK", "~/clawd-emoji/frames")).expanduser()

OVERSAMPLE = 2    # PNG px per logical px, keeps pixels crisp after scaling

# animations: name -> (emoji in the pack, how to cut it)
#   grid: drawn on the pack's 3px grid at Clawd's usual size
#   fit:  drawn smaller and off-grid, resampled to Clawd's usual size
ANIMS = {
    "code": ("79", "grid"),      # terminal on his head
    "busy": ("78", "grid"),      # progress bar
    "sleep": ("83", "grid"),     # Zz
    "music": ("39", "grid"),     # headphones
    "video": ("38", "grid"),     # popcorn
    "alert": ("42", "grid"),     # turns red
    "notify": ("35", "grid"),
    "ok": ("36", "grid"),
    "fail": ("37", "grid"),
    "love": ("41", "grid"),      # hearts, on click
    "read": ("59", "fit"),       # glasses and a book
    "happy": ("61", "fit"),
    "skate": ("66", "fit"),
    "ball": ("67", "fit"),
    "trumpet": ("68", "fit"),
}

# grid emoji frames are 100x100 with a 3px grid starting at (2, 2)
GRID_STEP, GRID_X, GRID_Y = 3, 2, 2
W, H = 33, 28      # Clawd sprite size in logical px
SKIN = (213, 124, 90)

ROOM_W, ROOM_H = 152, H

# where Clawd stands for each activity: left edge of his sprite in room px
STATIONS = {"home": 56, "bed": 4, "desk": 80}

WOOD = (138, 90, 59)
WOOD_LIGHT = (163, 112, 76)
WOOD_DARK = (94, 60, 39)
FRAME = (127, 132, 156)
SKY = (116, 167, 232)
CLOUD = (220, 230, 248)
PILLOW = (230, 233, 245)
PILLOW_SHADE = (186, 190, 208)
BLANKET = (108, 127, 184)
BLANKET_LIGHT = (134, 152, 205)
BLANKET_SHADE = (82, 99, 154)
LEAF = (127, 196, 106)
LEAF_DARK = (78, 143, 69)
POT = (181, 101, 74)
POT_DARK = (140, 74, 53)
METAL = (127, 132, 156)
MONITOR = (69, 71, 90)
SCREEN = (30, 32, 48)
CODE = (166, 227, 161)
CODE_ALT = (137, 180, 250)
LAMP = (249, 226, 175)
COFFEE = (120, 72, 46)


def room():
    img = Image.new("RGBA", (ROOM_W, ROOM_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def r(x, y, w, h, c):
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=c)

    # window above the bed
    r(7, 2, 24, 13, FRAME)
    r(8, 3, 22, 11, SKY)
    r(18, 3, 2, 11, FRAME)
    r(8, 8, 22, 1, FRAME)
    r(10, 5, 5, 2, CLOUD)
    r(11, 4, 3, 1, CLOUD)
    r(23, 11, 5, 1, CLOUD)
    r(24, 10, 2, 1, CLOUD)
    r(6, 15, 26, 1, WOOD_LIGHT)
    r(6, 16, 26, 1, WOOD_DARK)

    # bed
    r(1, 14, 3, 1, WOOD_LIGHT)
    r(1, 15, 3, 13, WOOD_DARK)
    r(34, 18, 3, 1, WOOD_LIGHT)
    r(34, 19, 3, 9, WOOD_DARK)
    r(4, 19, 30, 3, PILLOW_SHADE)
    r(4, 22, 30, 2, WOOD)
    r(4, 24, 30, 1, WOOD_DARK)
    r(5, 17, 8, 2, PILLOW)
    r(5, 19, 8, 1, PILLOW_SHADE)
    r(13, 18, 21, 1, BLANKET_LIGHT)
    r(13, 19, 21, 2, BLANKET)
    r(13, 21, 21, 1, BLANKET_SHADE)

    # plant
    r(45, 9, 2, 12, LEAF_DARK)
    r(42, 12, 4, 2, LEAF)
    r(41, 13, 2, 2, LEAF_DARK)
    r(47, 10, 4, 2, LEAF)
    r(50, 11, 2, 2, LEAF_DARK)
    r(44, 7, 3, 2, LEAF)
    r(41, 17, 5, 2, LEAF)
    r(47, 15, 5, 2, LEAF)
    r(48, 17, 3, 1, LEAF_DARK)
    r(41, 21, 11, 2, POT)
    r(42, 23, 9, 5, POT)
    r(48, 23, 3, 5, POT_DARK)
    r(41, 22, 11, 1, POT_DARK)

    # desk
    r(112, 16, 39, 1, WOOD_LIGHT)
    r(112, 17, 39, 2, WOOD)
    r(112, 19, 39, 1, WOOD_DARK)
    r(113, 20, 2, 8, WOOD_DARK)
    r(138, 20, 12, 8, WOOD)
    r(138, 23, 12, 1, WOOD_DARK)
    r(149, 20, 1, 8, WOOD_DARK)
    r(142, 21, 3, 1, METAL)
    r(142, 25, 3, 1, METAL)

    # monitor
    r(127, 3, 22, 11, MONITOR)
    r(128, 4, 20, 9, SCREEN)
    r(130, 5, 6, 1, CODE)
    r(132, 7, 9, 1, CODE_ALT)
    r(132, 9, 5, 1, CODE)
    r(138, 9, 4, 1, CODE_ALT)
    r(130, 11, 3, 1, CODE)
    r(136, 14, 4, 1, MONITOR)
    r(134, 15, 8, 1, MONITOR)

    # lamp and mug
    r(114, 15, 6, 1, METAL)
    r(116, 9, 1, 6, METAL)
    r(116, 8, 3, 1, METAL)
    r(117, 5, 6, 3, LAMP)
    r(122, 12, 4, 4, PILLOW)
    r(122, 12, 4, 1, COFFEE)
    r(126, 13, 1, 2, PILLOW)
    return img


def sample(path, step, gx, gy):
    """Take the centre pixel of every grid cell of one emoji frame."""
    src = Image.open(path).convert("RGBA")
    px = src.load()
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for j in range(H):
        for i in range(W):
            x, y = int(gx + (i + 0.5) * step), int(gy + (j + 0.5) * step)
            if 0 <= x < src.width and 0 <= y < src.height and px[x, y][3] > 128:
                out.putpixel((i, j), px[x, y][:3] + (255,))
    return out


def cut(path):
    """Resample one 100x100 emoji frame drawn on the 3px grid."""
    return sample(path, GRID_STEP, GRID_X, GRID_Y)


def fit_grid(path):
    """Grid that puts Clawd's skin from this frame where it sits in grid emoji:
    30 cells wide, arms from column 1, top of the body at row 9."""
    src = Image.open(path).convert("RGBA")
    px = src.load()
    xs, ys = [], []
    for y in range(src.height):
        for x in range(src.width):
            c = px[x, y]
            if c[3] > 200 and all(abs(c[k] - SKIN[k]) < 25 for k in range(3)):
                xs.append(x)
                ys.append(y)
    step = (max(xs) - min(xs) + 1) / 30
    return step, min(xs) - step, min(ys) - 9 * step


def face(base, eyes, dx=0):
    """Clear the sleeping eyes from base and draw others; eyes = [(x, y), ...] for the left eye."""
    f = base.copy()
    skin = base.getpixel((15, 12))
    for x in (8, 9, 10, 21, 22, 23):
        f.putpixel((x, 14), skin)
    for x, y in eyes:
        f.putpixel((x + dx, y), EYE)
        f.putpixel((x + 13 + dx, y), EYE)
    return f


EYE = (20, 20, 19)
OPEN = [(x, y) for x in (8, 9, 10) for y in (12, 13, 14)]
HAPPY = [(9, 12), (8, 13), (10, 13)]

BUBBLE = [
    ".bbbbbbbbb.",
    "bbbbbbbbbbb",
    "bb.bb.bb.bb",
    "bbbbbbbbbbb",
    ".bbbbbbbbb.",
    "..bb.......",
    "..b........",
]
BUBBLE_COLOR = (91, 143, 214)
DOT_COLOR = (230, 233, 245)
FLAG_COLORS = {"#": (20, 20, 19), "w": (230, 233, 245)}


def chat_frames(sleeping):
    """Speech bubble over his head, dots appearing one by one."""
    out = []
    for dots in range(4):
        f = face(sleeping, OPEN, dx=1)
        for y, row in enumerate(BUBBLE):
            for x, ch in enumerate(row):
                if ch == "b":
                    f.putpixel((18 + x, 1 + y), BUBBLE_COLOR + (255,))
                elif ch == "." and y == 2 and (x - 2) // 3 < dots:
                    f.putpixel((18 + x, 1 + y), DOT_COLOR + (255,))
        out += [f] * 3
    return out


def done_frames(sleeping):
    """Happy face, waving a checkered flag."""
    out = []
    for wave in range(2):
        f = face(sleeping, HAPPY)
        for y in range(0, 15):
            f.putpixel((27, y), (127, 132, 156, 255))
        for y in range(6):
            for x in range(5):
                ch = "#" if (x // 1 + y // 1 + wave) % 2 else "w"
                yy = y + (1 if wave and x >= 3 else 0)
                f.putpixel((28 + x, yy), FLAG_COLORS[ch] + (255,))
        out += [f] * 4
    return out * 3


def anims():
    out = {}
    for name, (emoji, how) in ANIMS.items():
        srcs = sorted((PACK / emoji).glob("*.png"))
        if not srcs:
            raise SystemExit(f"no frames for {name!r} in {PACK / emoji}")
        grid = (GRID_STEP, GRID_X, GRID_Y) if how == "grid" else fit_grid(srcs[0])
        out[name] = [sample(p, *grid) for p in srcs]

    # calm idle face: the sleeping pose with eyes drawn open
    # frames: 0 rest, 1 blink, 2 look left, 3 look right
    sleeping = out["sleep"][0]
    out["idle"] = [face(sleeping, OPEN), sleeping, face(sleeping, OPEN, -1), face(sleeping, OPEN, 1)]
    out["chat"] = chat_frames(sleeping)
    out["done"] = done_frames(sleeping)
    return out


def save(img, path):
    img.resize((img.width * OVERSAMPLE, img.height * OVERSAMPLE), Image.NEAREST).save(path)


def preview(base, fr, scale=6):
    """preview.gif for the README: a short tour through the activities."""
    bg = Image.new("RGBA", base.size, (30, 30, 46, 255))
    bg.alpha_composite(base)
    tour = [("idle", "home", 6), ("code", "desk", 2), ("busy", "desk", 2), ("ok", "desk", 2),
            ("read", "home", 1), ("chat", "home", 2), ("music", "home", 2), ("video", "home", 2),
            ("skate", "home", 1), ("done", "home", 1), ("sleep", "bed", 2)]
    pics = []
    for name, station, loops in tour:
        for f in fr[name] * loops:
            img = bg.copy()
            img.alpha_composite(f, (STATIONS[station], 0))
            pics.append(img.resize((img.width * scale, img.height * scale), Image.NEAREST).convert("P"))
    pics[0].save(HERE / "preview.gif", save_all=True, append_images=pics[1:],
                 duration=83, loop=0, disposal=2)


def main():
    FRAMES.mkdir(exist_ok=True)
    for old in FRAMES.glob("*.png"):
        old.unlink()
    base = room()
    save(base, FRAMES / "room.png")
    fr = anims()

    meta = [f"{k}={v}" for k, v in STATIONS.items()] + [f"n-{k}={len(v)}" for k, v in fr.items()]
    css = [
        "/* generated by gen.py */",
        f"/* clawd: {' '.join(meta)} */",
        "#custom-clawd {",
        f"    min-width: {ROOM_W}px;",
        f"    min-height: {H}px;",
        "    padding: 0;",
        "    background-repeat: no-repeat, no-repeat;",
        f"    background-size: {W}px {H}px, {ROOM_W}px {ROOM_H}px;",
        "}",
    ]
    for name, frames in fr.items():
        for i, f in enumerate(frames):
            save(f, FRAMES / f"{name}-{i}.png")
            css.append(f'#custom-clawd.f-{name}-{i} {{ background-image: url("frames/{name}-{i}.png"), url("frames/room.png"); }}')
    for x in range(ROOM_W - W + 1):
        css.append(f"#custom-clawd.p-{x} {{ background-position: {x}px 0, 0 0; }}")
    (HERE / "clawd.css").write_text("\n".join(css) + "\n")
    preview(base, fr)
    print(" ".join(meta))


if __name__ == "__main__":
    main()
