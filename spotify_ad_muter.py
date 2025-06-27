import time 
import subprocess
import json


POLL_INTERVAL = 1.0

SPOTIFY_APP_CLASS = "Spotify"


def input_to_list_of_dict(input):
    segments = input.split("Sink Input #")

    list_of_dict = []

    for segment in segments:
        lines = segment.strip().split("\n")

        if lines and lines[0]:
            seg_dict = {}
            propreties_dict = {}
        
            seg_dict["Sink Input"] = lines[0].strip()

            for line in lines[1:]:
                line = line.strip()

                if line.startswith("Properties: "):
                    continue
                elif line:
                    key_value = line.split(":", 1)
                    if len(key_value) == 2:
                        seg_dict[key_value[0].strip()] = key_value[1].strip()
        
            for line in lines:
                line = line.strip()

                if line.startswith("Properties: "):
                    continue
                elif line:
                    if "=" in line:
                        key_value = line.split("=", 1)
                        if len(key_value) == 2:
                            propreties_dict[key_value[0].strip()] = key_value[1].strip().strip('"')

            if propreties_dict:
                seg_dict["Properties"] = propreties_dict

            list_of_dict.append(seg_dict)

    return list_of_dict

            

def set_mute(state: bool):
    flag = '1' if state else '0'

    try :
        out = subprocess.check_output(['pactl','list','sink-inputs']).decode('utf-8')
        proc_output = input_to_list_of_dict(out)
        #print(proc_output)
        for stream in proc_output:
            prop = stream['Properties']
            #print(prop)
            if prop["application.name"] == "spotify":
               stream_id = stream['Sink Input']
               subprocess.call(['pactl', 'set-sink-input-mute', stream_id, flag])
               print(f"Spotify stream, id : {stream_id}")
    except Exception as e:
        subprocess.call(['pactl', 'set-sink-mute', '@DEFAULT_SINK@', flag])
        print(f"failed to detect Spotify stream, switching to System stream: {e}")
           
    


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
        #print(f"Current Playing: {current_title}")
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
