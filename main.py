import platform


def main():

    system = platform.system()
    if system == 'Darwin':
        from MacOSMonitor import MacOSSpotifyMonitor
        mac = MacOSSpotifyMonitor()
        mac.run()
    elif system == 'Linux':
        from HyprlandMonitor import HyprlandSotifyMonitor
        hypr = HyprlandSotifyMonitor()
        hypr.run()
    elif system == 'Windows':
        from WindowsMonitor import WindowsSpotifyMonitor
        win = WindowsSpotifyMonitor()
        win.run()

if __name__ == '__main__':
    main()
