"""Constants for Xgimi Integration."""

# Base component constants
NAME = "Xgimi Projector Integration"
DOMAIN = "xgimi"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.8"
COMMAND_DICT = {
    "ok": "KEYPRESSES:49",
    "play": "KEYPRESSES:49",
    "pause": "KEYPRESSES:49",
    "power": "KEYPRESSES:116",
    "back": "KEYPRESSES:48",
    "home": "KEYPRESSES:35",
    "menu": "KEYPRESSES:139",
    "right": "KEYPRESSES:37",
    "left": "KEYPRESSES:50",
    "up": "KEYPRESSES:36",
    "down": "KEYPRESSES:38",
    "volumedown": "KEYPRESSES:114",
    "volumeup": "KEYPRESSES:115",
    "volumemute": "KEYPRESSES:113",
    "autofocus": "KEYPRESSES:2099",
    "autofocus_new": "KEYPRESSES:2103",
    "manual_focus_left": "KEYPRESSES:2097",
    "manual_focus_right": "KEYPRESSES:2098",
    "motor_left_overstep": "KEYPRESSES:2095",
    "motor_left_start": "KEYPRESSES:2092",
    "motor_right_overstep": "KEYPRESSES:2096",
    "motor_right_start": "KEYPRESSES:2093",
    "motor_stop": "KEYPRESSES:2101",
    "shortcut_setting": "KEYPRESSES:2094",
    "choose_source": "KEYPRESSES:2102",
    "hibernate": "KEYPRESSES:2106",
    "xmusic": "KEYPRESSES:2108",
}
ADVANCE_COMMAND_DICT = {
    str(
        {
            "action": 20000,
            "controlCmd": {
                "data": "command_holder",
                "delayTime": 0,
                "mode": 5,
                "time": 0,
                "type": 0,
            },
            "msgid": "2",
        }
    )
}
