#!/usr/bin/env python3

from pathlib import Path

from .startmeup import *

MODULE_NAME = Path(__file__).stem

__doc__ = f"""Python IDE for the command line.

========== ⚠️  WARNING! ⚠️  ==========
This project is currently under construction.
Stay tuned for updates.

Module: {PROJECT_NAME}.{MODULE_NAME}
Version: {VERSION}
Author: {AUTHOR}
Date: {LAST_SAVED_DATE}

## Description

This module defines the Workshop class.

## Typical Use
```python
args = parse_arguments()

## Notes

You can include implementation notes, dependencies, or version-specific
details here.

"""



from datetime import datetime

# if __package__:
#     from .where import *
# else:
#     from where import *

from pygnition.where import *

LEADING_SPACE = ''
if RUNNING_CLI:
    LEADING_SPACE = '  '

CRITICAL_PICT = f"🛑{LEADING_SPACE}"
INFO_PICT = f"💬{LEADING_SPACE}"
ERROR_PICT = f"❗{LEADING_SPACE}"
WARNING_PICT = f"⚠️{LEADING_SPACE}"
DEBUG_PICT = f"🐞{LEADING_SPACE}"
CONSTRUCTION_PICT = f"🚧{LEADING_SPACE}"
NEWLINE = '\n'
STOP_PICT = f"✋{LEADING_SPACE}"
WAVE_PICT = f"🖐️{LEADING_SPACE}"
# RGB for CMYK process blue: approximately (0, 183, 235)
ASK_PICT = f"\033[38;2;0;183;235m\u2754\033[0m{LEADING_SPACE}"  # ❔ in blue
CHECK_PICT = f"✅{LEADING_SPACE}"
FAILURE_PICT = f"❌{LEADING_SPACE}"
HOURGLASS_PICT = f"⏳{LEADING_SPACE}"
INFO_PICT_2 = f"ℹ️{LEADING_SPACE}"
GEAR_PICT = f"⚙️{LEADING_SPACE}"
TEXT_PICT = f"✍️{LEADING_SPACE}"
PYTHON_PICT = f"🐍{LEADING_SPACE}"
C_PICT = f"💻{LEADING_SPACE}"
SCRIPT_PICT = f"📜{LEADING_SPACE}"
FRAMED_PICT = f"🖼️{LEADING_SPACE}"
MUSIC_PICT = f"🎵{LEADING_SPACE}"
VIDEO_PICT = f"🎬{LEADING_SPACE}"
BOOK_PICT = f"📖{LEADING_SPACE}"
PKG_PICT = f"📦{LEADING_SPACE}"
FOLDER_PICT = f"📁{LEADING_SPACE}"
LOG_PICT = f"🗃️{LEADING_SPACE}"
POLICE_LIGHT_PICT = f"🚨{LEADING_SPACE}"
LINK_PICT = f"🔗{LEADING_SPACE}"

WORRIED_PICT = f"😦{LEADING_SPACE}"
FROWN_PICT = f"😞{LEADING_SPACE}"
TEAR_PICT = f"😢{LEADING_SPACE}"
FROWN_MAD_PICT = f"😣{LEADING_SPACE}"

CLOCK_PICTS = {
    "1:00": f"🕐{LEADING_SPACE}",
    "2:00": f"🕑{LEADING_SPACE}",
    "3:00": f"🕒{LEADING_SPACE}",
    "4:00": f"🕓{LEADING_SPACE}",
    "5:00": f"🕔{LEADING_SPACE}",
    "6:00": f"🕕{LEADING_SPACE}",
    "7:00": f"🕖{LEADING_SPACE}",
    "8:00": f"🕗{LEADING_SPACE}",
    "9:00": f"🕘{LEADING_SPACE}",
    "10:00": f"🕙{LEADING_SPACE}",
    "11:00": f"🕚{LEADING_SPACE}",
    "12:00": f"🕛{LEADING_SPACE}",

    "1:30": f"🕜{LEADING_SPACE}",
    "2:30": f"🕝{LEADING_SPACE}",
    "3:30": f"🕞{LEADING_SPACE}",
    "4:30": f"🕟{LEADING_SPACE}",
    "5:30": f"🕠{LEADING_SPACE}",
    "6:30": f"🕡{LEADING_SPACE}",
    "7:30": f"🕢{LEADING_SPACE}",
    "8:30": f"🕣{LEADING_SPACE}",
    "9:30": f"🕤{LEADING_SPACE}",
    "10:30": f"🕥{LEADING_SPACE}",
    "11:30": f"🕦{LEADING_SPACE}",
    "12:30": f"🕧{LEADING_SPACE}",
}

GLOBE_AMERICA_PICT = f"🌎{LEADING_SPACE}"
GLOBE_AFRICA_PICT = f"🌍{LEADING_SPACE}"
GLOBE_ASIA_PICT = f"🌏{LEADING_SPACE}"
GLOBE_MERIDIANS = f"🌐{LEADING_SPACE}"
SATURN_PICT = f"🪐{LEADING_SPACE}"
WORLD_MAP_PICT = f"🗺️{LEADING_SPACE}"

def current_clock_pict(dt: datetime) -> str:
    """
    Return the clock emoji from CLOCK_PICTS most closely representing the given datetime.
    """
    hour = dt.hour % 12
    if hour == 0:
        hour = 12
    minute = dt.minute

    # Round to nearest half hour
    if minute < 15:
        rounded_hour, rounded_minute = hour, 0
    elif minute < 45:
        rounded_hour, rounded_minute = hour, 30
    else:
        rounded_hour = (hour % 12) + 1
        if rounded_hour == 13:
            rounded_hour = 1
        rounded_minute = 0

    key = f"{rounded_hour}:{rounded_minute:02d}"

    # Fallback if not in CLOCK_PICTS
    if key not in CLOCK_PICTS:
        def minutes_from_key(k: str) -> int:
            h, m = map(int, k.split(":"))
            return (h % 12) * 60 + m
        target_minutes = (rounded_hour % 12) * 60 + rounded_minute
        key = min(CLOCK_PICTS.keys(), key=lambda k: abs(minutes_from_key(k) - target_minutes))

    return CLOCK_PICTS[key]

if __name__ == '__main__':
    now = datetime.now()
    print(f'{current_clock_pict(now)} Current time: {now}')
