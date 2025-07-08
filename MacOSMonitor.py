import time
import subprocess

class MacOSSpotifyMonitor():

    def __init__(self):
        self.is_muted = False
        self.spotify_volume = 50

    POLL_INTERVAL = 1.0

    def get_spotify_info(self):

        applescript = '''
            tell application "Spotify"
                if it is running then
                    try 
                        set trackName to name of current track
                        set playerState to player state as string
                        return trackName & " | " & playerState
                    on error 
                        return "No track playing"
                    end try 
                else
                    return "Spotify not running"
                end if
            end tell
        '''

        try:
            result = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
            if result.returncode == 0:
                output = result.stdout.strip()
                if output and output != "No track playing" and output != "Spotify not running":
                    parts = output.split(" | ")

                    return {'track' : parts[0],'state' : parts[1]}
            return None
        except Exception as e:
            print(f"[ERROR] osascript error: {e}")


    def get_spotify_volume(self):

        applescript = '''
        tell application "Spotify"
            if it is running then
                try 
                    set currentVolume to sound volume
                    return currentVolume
                on error 
                    return 100
                end try
            else 
                return 100
            end if 
        end tell
        '''

        try:
            result = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)

            if result.returncode == 0:
                return result.stdout.strip()
            return 100
        except Exception as e:
            print(f"[ERROR] osascript error: {e}")


    def mute(self):

        if not self.is_muted:
            self.spotify_volume = self.get_spotify_volume()

        spotify_applescript = '''
        tell application "Spotify"
            if it is running then
                try
                    set sound volume to 0
                    return "Spotify muted"
                on error 
                    return "Error muting Spotify"
                end try
            else
                return "Spotify not running"
            end if
        end tell
        '''

        system_applescript = '''
        set volume with output muted
        '''

        try:
            result = subprocess.run(['osascript', '-e', spotify_applescript], capture_output=True, text=True)

            if result.returncode == 0:
                self.is_muted = True
                print(f"Spotify muted")
                return True

            else:
                fallback = subprocess.run(['osascript', '-e', system_applescript], capture_output=True, text=True)

                if fallback.returncode == 0:
                    self.is_muted = True
                    print(f"System muted")
                    return True

        except Exception as e:
            print(f"[ERROR] muting : {e}")
        return False


    def unmute(self):

        if not self.is_muted:
            return True

        spotify_applescript = f'''
                tell application "Spotify"
                    if it is running then
                        try
                            set sound volume to {self.spotify_volume}
                            return "Spotify unmuted"
                        on error 
                            return "Error unmuting Spotify"
                        end try
                    else
                        return "Spotify not running"
                    end if
                end tell
                '''

        system_applescript = '''
                set volume without output muted
                '''

        try:
            result = subprocess.run(['osascript', '-e', spotify_applescript], capture_output=True, text=True)

            if result.returncode == 0:
                self.is_muted = False
                print(f"Spotify unmuted")
                return True

            else:
                fallback = subprocess.run(['osascript', '-e', system_applescript], capture_output=True, text=True)

                if fallback.returncode == 0:
                    self.is_muted = False
                    print(f"System unmuted")
                    return True

        except Exception as e:
            print(f"[ERROR] unmuting : {e}")
        return False


    def is_ad_playing(self):
        title = self.get_spotify_info()['track']

        if not title:
            return False

        if 'Advertisement' in title:
            return True
        return False


    def run(self):
        print("Starting Spotify ad muter...")
        while True:
            ad = self.is_ad_playing()
            current_title = self.get_spotify_info()['track']
            # print(current_title)
            if ad and self.is_muted is not True:
                print(f"Ad detected (title: {current_title}), muting audio.")
                self.mute()
            elif not ad and self.is_muted is not False:
                print(f"Music playing (title: {current_title}), unmuting audio.")
                self.unmute()
            time.sleep(self.POLL_INTERVAL)

