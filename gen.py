#!/usr/bin/env python3
"""Generate Clawd's room, his frames and the CSS that maps classes to them.

Run after editing the sprites, the room or the layout:
    python gen.py
"""
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
FRAMES = HERE / "frames"

PX = 2            # logical px per sprite pixel on the bar
OVERSAMPLE = 4    # PNG px per logical px, keeps pixels crisp after scaling
STEP = 2          # logical px per position class

PALETTE = {
    # Clawd
    "o": (217, 119, 87, 255),   # body
    "h": (232, 150, 120, 255),  # highlight
    "s": (178, 88, 60, 255),    # shadow / legs
    "e": (20, 20, 19, 255),     # eyes
    # room
    "w": (138, 90, 59, 255),    # wood
    "W": (94, 60, 39, 255),     # dark wood
    "b": (108, 127, 184, 255),  # blanket
    "B": (82, 99, 154, 255),    # blanket shadow
    "p": (230, 233, 245, 255),  # pillow
    "f": (127, 132, 156, 255),  # window frame
    "k": (116, 167, 232, 255),  # sky
    "K": (220, 230, 248, 255),  # cloud
    "g": (127, 196, 106, 255),  # leaf
    "G": (78, 143, 69, 255),    # dark leaf
    "t": (181, 101, 74, 255),   # pot
    "T": (140, 74, 53, 255),    # pot shadow
    "m": (69, 71, 90, 255),     # monitor
    "c": (60, 90, 150, 255),    # screen
    "C": (166, 227, 161, 255),  # code on screen
    "l": (249, 226, 175, 255),  # lamp shade
    "L": (127, 132, 156, 255),  # lamp pole
}

# Clawd sprite
W, H = 16, 12


def body(eyes, blink=False):
    """Body rows; eyes = (left col, right col)."""
    rows = [
        "...hhhhhhhhhh...",
        "...oooooooooo...",
        "...oooooooooo...",
        "...oooooooooo...",
        ".oooooooooooooo.",
        ".soooooooooooos.",
        "...oooooooooo...",
        "...ssssssssss...",
    ]
    rows = [list(r) for r in rows]
    eye_rows = (3,) if blink else (2, 3)
    for r in eye_rows:
        for c in eyes:
            rows[r][c] = "e"
    return ["".join(r) for r in rows]


LEGS = {
    "stand": ["...s.s....s.s...", "...s.s....s.s..."],
    "step_a": ["...s.s....s.s...", "...s......s....."],
    "step_b": ["...s.s....s.s...", ".....s......s..."],
    "tuck": ["...s.s....s.s..."],
}
EYES = {"r": (6, 11), "l": (4, 9), "c": (5, 10)}


def compose(rows_body, legs, lift=0):
    top = H - len(rows_body) - len(legs) - lift
    grid = ["." * W] * top + rows_body + legs
    grid += ["." * W] * (H - len(grid))
    return grid


def frames():
    out = {}
    for d in "rlc":
        out[f"look-{d}"] = compose(body(EYES[d]), LEGS["stand"])
        out[f"blink-{d}"] = compose(body(EYES[d], blink=True), LEGS["stand"])
        out[f"hop-{d}"] = compose(body(EYES[d]), LEGS["tuck"], lift=2)
    for d in "rl":
        out[f"walk-{d}-0"] = out[f"look-{d}"]
        out[f"walk-{d}-1"] = compose(body(EYES[d]), LEGS["step_a"])
        out[f"walk-{d}-2"] = compose(body(EYES[d]), LEGS["step_b"])
    return out


# Room: furniture sprites placed by (col, row of their top edge)
ROOM_W, ROOM_H = 76, H

BED = [
    "WW..............",
    "WWppp...........",
    "WWpppbbbbbbbbbbW",
    "WWBBBBBBBBBBBBBW",
    "WWwwwwwwwwwwwwwW",
    "WW............WW",
]
WINDOW = [
    ".ffffffffffff.",
    ".fkkkkkfkkKKf.",
    ".fkKKkkfkkkkf.",
    ".ffffffffffff.",
    ".fkkkkkfkkkkf.",
    ".fkkkkkfkkkkf.",
    ".ffffffffffff.",
    "wwwwwwwwwwwwww",
]
PLANT = [
    "..g.g.",
    ".gGgGg",
    "gGgGg.",
    ".gGg..",
    "TttttT",
    ".tttt.",
    ".TTTT.",
]
DESK = [
    "wwwwwwwwwwwwwwwwww",
    "WWWWWWWWWWWWWWWWWW",
    ".W...........WwwW.",
    ".W...........WWWW.",
    ".W...........W..W.",
    ".W...........W..W.",
]
MONITOR = [
    "mmmmmmmmmm",
    "mcCCCccccm",
    "mccCCCCccm",
    "mcCCcCCccm",
    "mmmmmmmmmm",
    "....mm....",
]
LAMP = [
    "lll.",
    "llll",
    "..L.",
    "..L.",
    ".LLL",
]

FURNITURE = [
    (BED, 1, ROOM_H - len(BED)),
    (WINDOW, 18, 1),
    (PLANT, 33, ROOM_H - len(PLANT)),
    (DESK, 57, ROOM_H - len(DESK)),
    (MONITOR, 63, ROOM_H - len(DESK) - len(MONITOR)),
    (LAMP, 58, ROOM_H - len(DESK) - len(LAMP)),
]

# where Clawd stands for each activity, in room cols (left edge of his sprite)
STATIONS = {"home": 40, "bed": 2, "window": 18, "plant": 31, "desk": 60}

TRACK = ROOM_W * PX   # module width in logical px


def room():
    grid = [["."] * ROOM_W for _ in range(ROOM_H)]
    for sprite, col, row in FURNITURE:
        for y, line in enumerate(sprite):
            for x, ch in enumerate(line):
                if ch != ".":
                    grid[row + y][col + x] = ch
    return ["".join(r) for r in grid]


def render(grid, path=None, scale=PX * OVERSAMPLE, bg=(0, 0, 0, 0)):
    img = Image.new("RGBA", (len(grid[0]) * scale, len(grid) * scale), bg)
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch in PALETTE:
                img.paste(PALETTE[ch], (x * scale, y * scale, (x + 1) * scale, (y + 1) * scale))
    if path:
        img.save(path)
    return img


def overlay(base, sprite, col):
    rows = [list(r) for r in base]
    for y, line in enumerate(sprite):
        for x, ch in enumerate(line):
            if ch != ".":
                rows[y][col + x] = ch
    return ["".join(r) for r in rows]


def preview(fr, scale=6):
    """Idle preview.gif for the README."""
    home = STATIONS["home"]
    script = (["look-c"] * 12 + ["blink-c"] * 2 + ["look-c"] * 6 + ["look-l"] * 10
              + ["look-r"] * 10 + ["blink-r"] * 2 + ["look-r"] * 4 + ["look-c"] * 4
              + ["hop-c"] * 4 + ["look-c"] * 6)
    base = room()
    pics = [render(overlay(base, fr[name], home), scale=scale, bg=(30, 30, 46, 255)).convert("P")
            for name in script]
    pics[0].save(HERE / "preview.gif", save_all=True, append_images=pics[1:],
                 duration=100, loop=0, disposal=2)


def main():
    FRAMES.mkdir(exist_ok=True)
    for old in FRAMES.glob("*.png"):
        old.unlink()
    render(room(), FRAMES / "room.png")

    stations = " ".join(f"{k}={v * PX}" for k, v in STATIONS.items())
    css = [
        "/* generated by gen.py */",
        f"/* clawd: max={TRACK - W * PX} step={STEP} {stations} */",
        "#custom-clawd {",
        f"    min-width: {TRACK}px;",
        f"    min-height: {H * PX}px;",
        "    padding: 0;",
        "    background-repeat: no-repeat, no-repeat;",
        f"    background-size: {W * PX}px {H * PX}px, {TRACK}px {ROOM_H * PX}px;",
        "}",
    ]
    fr = frames()
    for name, grid in fr.items():
        render(grid, FRAMES / f"{name}.png")
        css.append(f'#custom-clawd.f-{name} {{ background-image: url("frames/{name}.png"), url("frames/room.png"); }}')
    for p in range(0, TRACK - W * PX + 1, STEP):
        css.append(f"#custom-clawd.p-{p} {{ background-position: {p}px center, 0 center; }}")
    (HERE / "clawd.css").write_text("\n".join(css) + "\n")
    preview(fr)
    print(f"track: {TRACK}px, stations: {stations}")


if __name__ == "__main__":
    main()
