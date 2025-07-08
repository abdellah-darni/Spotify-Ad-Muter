import subprocess
import time


class WindowsSpotifyMonitor:

    POLL_INTERVAL = 1.0

    def __init__(self):
        self.is_muted = False
        self.current_title = None


    def get_spotify_window_title(self):

        ps_command = "Get-Process | Where-Object {$_.ProcessName -eq 'Spotify' -and $_.MainWindowTitle} | Select-Object -First 1 | ForEach-Object {$_.MainWindowTitle}"

        try:
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return result.stdout.strip()
        except Exception as e:
            print(f"[ERROR] {e}")

        return ''


    def set_mute(self, state: bool):

        flag = '1' if state else '0'

        try:
            subprocess.call(['nircmd', 'mutesysvolume', flag])
            if flag :
                print(f"Ad detected: {self.current_title}, muting audio.")
            else:
                print(f"Music playing: {self.current_title}, unmuting audio.")

        except Exception as e:
            print(f"[ERROR] {e}")


    def is_ad_playing(self):
        title = self.get_spotify_window_title()
        if not title:
            return False
        return 'Advertisement' in title


    def run(self):
        print("Starting  Spotify ad muter for Windows...")
        print("Note: The current version for windows mute the entire System not just Spotify!!")
        print("Note: For this to work you need to install NirCmd")
        print("--------------")

        last_played = None
        while True:
            ad = self.is_ad_playing()
            self.current_title = self.get_spotify_window_title()

            if (self.current_title != last_played):
                last_played = self.current_title
                print(f"Current title: {self.current_title}")
                print("---")

            if ad and self.is_muted is not True:
                self.set_mute(True)
                self.is_muted = True
            elif not ad and self.is_muted is not False:
                self.set_mute(False)
                self.is_muted = False

            time.sleep(self.POLL_INTERVAL)