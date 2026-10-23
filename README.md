# waybar-clawd

Pixel-art Clawd walking along your Waybar.

![preview](preview.gif)

He walks from edge to edge, glances at you and blinks now and then, and hops and turns around when clicked.

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

To change the speed, set `CLAWD_DELAY` in `exec`. It is seconds per frame and defaults to `0.07`:

```jsonc
"exec": "CLAWD_DELAY=0.1 ~/.config/waybar/scripts/clawd/clawd.sh"
```

The sprite, colors, pixel size (`PX`) and track width (`TRACK`) are all set in `gen.py`. After editing them, regenerate the frames and CSS, which needs Pillow:

```bash
python gen.py
```

At the default `PX = 2` the sprite is 24px tall. On a thinner bar, use `PX = 1`.

