# waybar-clawd

Pixel-art Clawd living in a tiny room on your Waybar.

![preview](preview.gif)

He has a bed, a window, a plant and a desk with a computer. For now he hangs out in the middle of the room, looks around and blinks. Click him to make him hop.

## Install

```bash
git clone https://github.com/egomalt/waybar-clawd.git ~/.config/waybar/scripts/clawd
```

Add the module to your Waybar config and put `"custom/clawd"` into one of the `modules-*` lists:

```jsonc
"custom/clawd": {
    "exec": "~/.config/waybar/scripts/clawd/clawd.sh",
    "return-type": "json",
    "format": "{}",
    "on-click": "pkill -USR1 -f scripts/clawd/[c]lawd.sh",
    "tooltip": true
}
```

Import the stylesheet in `style.css`, using an absolute path:

```css
@import "/home/<you>/.config/waybar/scripts/clawd/clawd.css";
```

Reload with `pkill -USR2 waybar`.

## Tweaking

To change the frame rate, set `CLAWD_DELAY` in `exec`. It is seconds per frame and defaults to `0.1`:

```jsonc
"exec": "CLAWD_DELAY=0.15 ~/.config/waybar/scripts/clawd/clawd.sh"
```

Clawd's sprite, the furniture and its layout, the colors and the pixel size (`PX`) are all set in `gen.py`. `STATIONS` there lists where Clawd stands at each piece of furniture. After editing any of this, regenerate the frames and CSS, which needs Pillow:

```bash
python gen.py
```

At the default `PX = 2` the room is 152×24px. On a thinner bar, use `PX = 1`.

