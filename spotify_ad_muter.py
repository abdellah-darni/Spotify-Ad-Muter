import platform



def main():

    system = platform.system()
    if system == 'Darwin':
        from MacOSMonitor import MacOSSpotifyMonitor
        print(f"[INFO] {system} ")
        mac = MacOSSpotifyMonitor()
        mac.run()
    elif system == 'Linux':
        from HyprlandMonitor import HyprlandSotifyMonitor
        print(f"[INFO] {system} ")
        hypr = HyprlandSotifyMonitor()
        hypr.run()

if __name__ == '__main__':
    main()
