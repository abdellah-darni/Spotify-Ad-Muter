# Spotify Ad Muter

A Python script that automatically detects and mutes Spotify advertisements across multiple platforms.

## Features

- **Automatic Ad Detection**: Monitors Spotify for advertisement playback
- **Cross-Platform Support**: Works on macOS, Hyprland (Linux), and Windows
- **Lightweight**: Runs efficiently in the background
- **Non-Intrusive**: Automatically unmutes when ads finish

## Platform Support

| Platform | Status | Notes                                                                     |
|----------|--------|---------------------------------------------------------------------------|
| macOS | ✅ Full Support | Could Mutes only Spotify application and falls back to system-wide muting |
| Hyprland | ✅ Full Support | Could Mutes only Spotify application and falls back to system-wide muting |
| Windows | ⚠️ Limited Support | Only system-wide muting (requires NirCmd)                                 |
| Other Linux | ❌ Not Supported | Only works on Hyprland                                                    |

## Known Limitations

- **Windows**: Currently mutes the entire system instead of just Spotify due to Windows audio API limitations (requires NirCmd utility). Uses PowerShell Get-Process commands for window title detection.
- **Linux**: Only supports Hyprland window manager - does not work on other Linux desktop environments. Requires `hyprctl` for window title detection.

## Requirements

- Python 3.6+ (uses only standard library modules)
- Spotify desktop application  
- Platform-specific system dependencies:
  - **macOS**: No additional requirements
  - **Hyprland (Linux)**: PulseAudio utilities
  - **Windows**: NirCmd utility (for audio control)

## Installation

### macOS
```bash
# Clone the repository
git clone https://github.com/abdellah-darni/Spotify-Ad-Muter.git
cd Spotify-Ad-Muter

# No additional Python packages needed (uses standard library only)

# Run the script
python spotify_ad_muter.py
```

### Hyprland (Linux)
```bash
# Clone the repository
git clone https://github.com/abdellah-darni/Spotify-Ad-Muter.git
cd Spotify-Ad-Muter

# No additional Python packages needed (uses standard library only)

# Ensure you have the necessary audio control packages
sudo pacman -S pulseaudio-utils  # For Arch-based systems
# or
sudo apt install pulseaudio-utils  # For Debian-based systems

# Run the script
python spotify_ad_muter.py
```

### Windows
```bash
# Clone the repository
git clone https://github.com/abdellah-darni/Spotify-Ad-Muter.git
cd Spotify-Ad-Muter

# No Python package dependencies required (uses only standard library)
# All dependencies are built-in: platform, time, subprocess, json

# Download and install NirCmd (required for Windows audio control)
# Visit: https://www.nirsoft.net/utils/nircmd.html
# Download nircmd.zip and extract nircmd.exe to your system PATH
# Or place nircmd.exe in the same directory as the script

# Run the script (Administrator privileges may be required)
python spotify_ad_muter.py
```

## Usage

1. **Start Spotify**: Ensure the Spotify desktop application is running
2. **Run the Script**: Execute the Python script in your terminal
3. **Background Operation**: The script will run in the background, monitoring for ads
4. **Automatic Muting**: When an ad is detected, audio will be muted automatically
5. **Auto-Unmute**: Audio will be restored when the ad finishes


## How It Works

The script monitors Spotify's window title through platform-specific system commands to detect when advertisements are playing:

### Detection Method
1. **macOS**: Uses AppleScript commands to read the Spotify window title
2. **Hyprland**: Uses `hyprctl` commands to get window information for the Spotify process
3. **Windows**: Uses `Get-Process` PowerShell commands to read window titles

### Ad Detection Logic
- Monitors the Spotify window title continuously
- Detects advertisement patterns in the window title text
- When an ad is detected in the title, triggers the muting process

### Muting Process
1. **macOS & Hyprland**: Attempts to mute only the Spotify application, falls back to system-wide muting if needed
2. **Windows**: Uses NirCmd to perform system-wide muting (application-specific muting not currently supported)
3. **Restoration**: Continuously monitors for the end of the advertisement and automatically unmutes when regular music playback resumes




## Disclaimer

This tool is for educational and personal use only. It interacts with Spotify's desktop application and system audio controls. Use responsibly and in accordance with Spotify's Terms of Service.

## Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Make sure you're using a supported platform

---
