# waybar-clawd

Pixel-art Clawd living in a tiny room on your Waybar.

![preview](preview.gif)

He has a bed, a window, a plant and a desk with a computer, and what he does depends on what's happening on your screen:

| When | Clawd |
| --- | --- |
| battery is low or the CPU is hot | turns red and angry |
| no input for a minute | falls asleep by the bed |
| Claude Code is working, or the CPU is busy | watches a progress bar at the desk |
| a video is playing | eats popcorn |
| a terminal or code editor is focused | codes at the desk, with a terminal on his head |
| a browser or document viewer is focused | reads, in glasses |
| a messenger is focused | chats |
| music is playing | puts on headphones |
| anything else | hangs around, blinks, glances about, and now and then skates, plays ball, happily squints or plays the trumpet |

When more than one applies, the higher row wins. On top of that he briefly reacts to:

| Event | Clawd |
| --- | --- |
| a desktop notification | notification sign |
| a shell command that ran 5+ seconds finishes | ✓ or ✗ |
| Claude Code finishes a reply | waves a checkered flag |
| a click | hearts |

Requires Hyprland, `hypridle`, `playerctl`, `jq` and `dbus-monitor`.

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

### Hooks

These are optional. Each one makes Clawd react to one more thing.

Shell commands, for fish:

```bash
ln -s ~/.config/waybar/scripts/clawd/hooks/clawd.fish ~/.config/fish/conf.d/clawd.fish
```

Claude Code: merge [`hooks/claude-code.json`](hooks/claude-code.json) into `~/.claude/settings.json`:

```bash
jq -s '.[0] * .[1]' ~/.claude/settings.json ~/.config/waybar/scripts/clawd/hooks/claude-code.json > /tmp/settings.json \
    && mv /tmp/settings.json ~/.claude/settings.json
```

That merge replaces any `UserPromptSubmit`, `PreToolUse` or `Stop` hooks you already have. If you have some, add the entries by hand instead.

## Tweaking

Settings are environment variables in `exec`:

| Variable | Default | Meaning |
| --- | --- | --- |
| `CLAWD_IDLE` | `60` | seconds without input before he falls asleep |
| `CLAWD_PAUSE` | `120` | seconds without input before he freezes completely, to save power while the screen is locked |
| `CLAWD_CPU_BUSY` | `80` | CPU load in percent that counts as busy |
| `CLAWD_CPU_HOT` | `90` | CPU temperature in °C that counts as hot |
| `CLAWD_BATTERY_LOW` | `15` | battery percent that counts as low while discharging |
| `CLAWD_CODE_APPS` | common terminals and editors | regex for window classes that count as coding |
| `CLAWD_READ_APPS` | common browsers and document viewers | regex for window classes that count as reading |
| `CLAWD_CHAT_APPS` | Telegram, Discord, Signal, Slack, … | regex for window classes that count as chatting |
| `CLAWD_DELAY` | `0.083` | seconds per frame |
| `CLAWD_CMD_MS` | `5000` | fish hook: how long a command must run before Clawd reacts, in ms (set it in fish) |

```jsonc
"exec": "CLAWD_IDLE=300 ~/.config/waybar/scripts/clawd/clawd.sh"
```

Idle time comes from a separate `hypridle` instance that the script starts with its own config, so your `hypridle.conf` is left alone. It respects systemd idle inhibitors, so he stays awake in caffeine mode (`systemd-inhibit --what=idle`, as in HyDE) and while a video player blocks idling. Notifications are picked up with `dbus-monitor`, so it works with any notification daemon.

The room, the furniture layout and `STATIONS` (where Clawd stands for each activity) are in `gen.py`. So is `ANIMS`, which says which emoji from the pack plays for each activity. To regenerate, point `CLAWD_PACK` at a directory with one folder of PNG frames per emoji, then run the script (needs Pillow):

```bash
CLAWD_PACK=~/clawd-emoji/frames python gen.py
```

The room is 152×28px.

