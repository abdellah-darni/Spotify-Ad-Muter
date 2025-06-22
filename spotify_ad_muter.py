import time 
import subprocess
import json


POLL_INTERVAL = 1.0

SPOTIFY_APP_CLASS = "Spotify"



def set_mute(state: bool):
    flag = '1' if state else '0'
    subprocess.call(['pactl', 'set-sink-mute', '@DEFAULT_SINK@', flag])


def get_spotify_window_title():
    
    try:
        out = subprocess.check_output(["hyprctl","clients","-j"]).decode('utf-8')
        clients = json.loads(out)

        for w in clients:
            if w.get('class').lower() == SPOTIFY_APP_CLASS.lower():
                return w.get('title','')
    except Exception as e:
        print(f"[ERROR] Hyprland IPC : {e}")
    return ''


def is_ad_playing():
    title = get_spotify_window_title()
    if not title:
        return False

    if 'Advertisement' in title:
        return True
    return False


def main():
    last_played_is_muted = None
    print("Starting Spotify ad muter...")
    while True:
        ad = is_ad_playing()
        current_title = get_spotify_window_title()
        print(f"Current Playing: {current_title}")
        if ad and last_played_is_muted is not True:
            print(f"Ad detected (title: {current_title}), muting audio.")
            set_mute(True)
            last_played_is_muted = True
        elif not ad and last_played_is_muted is not False:
            print(f"Music playing (title: {current_title}), unmuting audio.")
            set_mute(False)
            last_played_is_muted = False
        time.sleep(POLL_INTERVAL)

if __name__ == '__main__':
    main()
