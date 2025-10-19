# Module `picts`

<a name='module-picts'></a>
*Generated on 2025-10-18T20:08:17*

## Imports

- [datetime](https://docs.python.org/3/library/datetime.html)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [pygnition](https://docs.python.org/3/library/pygnition.html)

## Module Data

<a name='picts-var-module_name'></a>
- **MODULE_NAME** = `Path(__file__).stem`
<a name='picts-var-leading_space'></a>
- **LEADING_SPACE** = `''`
<a name='picts-var-critical_pict'></a>
- **CRITICAL_PICT** = `f'🛑{LEADING_SPACE}'`
<a name='picts-var-info_pict'></a>
- **INFO_PICT** = `f'💬{LEADING_SPACE}'`
<a name='picts-var-error_pict'></a>
- **ERROR_PICT** = `f'❗{LEADING_SPACE}'`
<a name='picts-var-warning_pict'></a>
- **WARNING_PICT** = `f'⚠️{LEADING_SPACE}'`
<a name='picts-var-debug_pict'></a>
- **DEBUG_PICT** = `f'🐞{LEADING_SPACE}'`
<a name='picts-var-construction_pict'></a>
- **CONSTRUCTION_PICT** = `f'🚧{LEADING_SPACE}'`
<a name='picts-var-newline'></a>
- **NEWLINE** = `'\n'`
<a name='picts-var-stop_pict'></a>
- **STOP_PICT** = `f'✋{LEADING_SPACE}'`
<a name='picts-var-wave_pict'></a>
- **WAVE_PICT** = `f'🖐️{LEADING_SPACE}'`
<a name='picts-var-ask_pict'></a>
- **ASK_PICT** = `f'\x1b[38;2;0;183;235m❔\x1b[0m{LEADING_SPACE}'` — ❔ in blue
<a name='picts-var-check_pict'></a>
- **CHECK_PICT** = `f'✅{LEADING_SPACE}'`
<a name='picts-var-failure_pict'></a>
- **FAILURE_PICT** = `f'❌{LEADING_SPACE}'`
<a name='picts-var-hourglass_pict'></a>
- **HOURGLASS_PICT** = `f'⏳{LEADING_SPACE}'`
<a name='picts-var-info_pict_2'></a>
- **INFO_PICT_2** = `f'ℹ️{LEADING_SPACE}'`
<a name='picts-var-gear_pict'></a>
- **GEAR_PICT** = `f'⚙️{LEADING_SPACE}'`
<a name='picts-var-text_pict'></a>
- **TEXT_PICT** = `f'✍️{LEADING_SPACE}'`
<a name='picts-var-python_pict'></a>
- **PYTHON_PICT** = `f'🐍{LEADING_SPACE}'`
<a name='picts-var-c_pict'></a>
- **C_PICT** = `f'💻{LEADING_SPACE}'`
<a name='picts-var-script_pict'></a>
- **SCRIPT_PICT** = `f'📜{LEADING_SPACE}'`
<a name='picts-var-framed_pict'></a>
- **FRAMED_PICT** = `f'🖼️{LEADING_SPACE}'`
<a name='picts-var-music_pict'></a>
- **MUSIC_PICT** = `f'🎵{LEADING_SPACE}'`
<a name='picts-var-video_pict'></a>
- **VIDEO_PICT** = `f'🎬{LEADING_SPACE}'`
<a name='picts-var-book_pict'></a>
- **BOOK_PICT** = `f'📖{LEADING_SPACE}'`
<a name='picts-var-pkg_pict'></a>
- **PKG_PICT** = `f'📦{LEADING_SPACE}'`
<a name='picts-var-folder_pict'></a>
- **FOLDER_PICT** = `f'📁{LEADING_SPACE}'`
<a name='picts-var-log_pict'></a>
- **LOG_PICT** = `f'🗃️{LEADING_SPACE}'`
<a name='picts-var-police_light_pict'></a>
- **POLICE_LIGHT_PICT** = `f'🚨{LEADING_SPACE}'`
<a name='picts-var-link_pict'></a>
- **LINK_PICT** = `f'🔗{LEADING_SPACE}'`
<a name='picts-var-worried_pict'></a>
- **WORRIED_PICT** = `f'😦{LEADING_SPACE}'`
<a name='picts-var-frown_pict'></a>
- **FROWN_PICT** = `f'😞{LEADING_SPACE}'`
<a name='picts-var-tear_pict'></a>
- **TEAR_PICT** = `f'😢{LEADING_SPACE}'`
<a name='picts-var-frown_mad_pict'></a>
- **FROWN_MAD_PICT** = `f'😣{LEADING_SPACE}'`
<a name='picts-var-clock_picts'></a>
- **CLOCK_PICTS** = `{'1:00': f'🕐{LEADING_SPACE}', '2:00': f'🕑{LEADING_SPACE}', '3:00': f'🕒{LEADING_SPACE}', '4:00': f'🕓{LEADING_SPACE}', '5:00': f'🕔{LEADING_SPACE}', '6:00': f'🕕{LEADING_SPACE}', '7:00': f'🕖{LEADING_SPACE}', '8:00': f'🕗{LEADING_SPACE}', '9:00': f'🕘{LEADING_SPACE}', '10:00': f'🕙{LEADING_SPACE}', '11:00': f'🕚{LEADING_SPACE}', '12:00': f'🕛{LEADING_SPACE}', '1:30': f'🕜{LEADING_SPACE}', '2:30': f'🕝{LEADING_SPACE}', '3:30': f'🕞{LEADING_SPACE}', '4:30': f'🕟{LEADING_SPACE}', '5:30': f'🕠{LEADING_SPACE}', '6:30': f'🕡{LEADING_SPACE}', '7:30': f'🕢{LEADING_SPACE}', '8:30': f'🕣{LEADING_SPACE}', '9:30': f'🕤{LEADING_SPACE}', '10:30': f'🕥{LEADING_SPACE}', '11:30': f'🕦{LEADING_SPACE}', '12:30': f'🕧{LEADING_SPACE}'}`
<a name='picts-var-globe_america_pict'></a>
- **GLOBE_AMERICA_PICT** = `f'🌎{LEADING_SPACE}'`
<a name='picts-var-globe_africa_pict'></a>
- **GLOBE_AFRICA_PICT** = `f'🌍{LEADING_SPACE}'`
<a name='picts-var-globe_asia_pict'></a>
- **GLOBE_ASIA_PICT** = `f'🌏{LEADING_SPACE}'`
<a name='picts-var-globe_meridians'></a>
- **GLOBE_MERIDIANS** = `f'🌐{LEADING_SPACE}'`
<a name='picts-var-saturn_pict'></a>
- **SATURN_PICT** = `f'🪐{LEADING_SPACE}'`
<a name='picts-var-world_map_pict'></a>
- **WORLD_MAP_PICT** = `f'🗺️{LEADING_SPACE}'`

## Function **current_clock_pict**

<a name='picts-function-current_clock_pict'></a>
```python
current_clock_pict(dt)
```

Return the clock emoji from [CLOCK_PICTS](picts.md#picts-var-clock_picts) most closely representing the given datetime.

