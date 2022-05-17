from pypozyx import PozyxSerial, get_first_pozyx_serial_port, UWBSettings, SingleRegister, NetworkID

from load_localization_settings import load_anchors, load_settings

anchors = load_anchors()
new_settings = load_settings()

# Identyfication of tag connected to the computer
serial_port = get_first_pozyx_serial_port()
if serial_port is not None:
    pozyx = PozyxSerial(serial_port)
else:
    print("No Pozyx port was found")
    exit(-1)

network_id = NetworkID()
me = pozyx.getNetworkId(network_id)

print("Default UWB Settings:")
uwb_settings = UWBSettings()
pozyx.getUWBSettings(uwb_settings)
print(uwb_settings)

print(f"\nDevice {hex(me)} is connected to network.")

# Identyfication of devices in network
devices = []
for anchor in anchors:
    devices.append(anchor.network_id)

connected = 1
for d in devices:
    who_am_i = SingleRegister()
    pozyx.getWhoAmI(who_am_i, remote_id=d)
    if who_am_i == 0x43:
        connected += 1
        print(f"Device {hex(d)} is connected to network.")
    else:
        print(f"Device {hex(d)} is not connected!!!")


print(f"{connected}/{len(devices) + 1} devices connected to network.\n")

# We should change remote devices settings at first because we will lose communication after that change.
settings_set = 0
for d in devices:
    uwb_settings = UWBSettings(
        channel=new_settings["channel"],
        prf=new_settings["pulse_repetition_frequecy"],
        plen=new_settings["preamble_length"],
        gain_db=new_settings["gain"],
        bitrate=new_settings["bitrate"])
    ret = pozyx.setUWBSettings(uwb_settings, remote_id=d)
    if ret == 1:
        settings_set += 1
        print(f"Settings for device {hex(d)} changed succefully.")
    elif ret == 0:
        print(f"Cannot change settings for device {hex(d)}.")
    else:
        print(f"Timeout for device {hex(d)}.")

# At the end we change settings of the device connected to computer.
uwb_settings = UWBSettings(
    channel=new_settings["channel"],
    prf=new_settings["pulse_repetition_frequecy"],
    plen=new_settings["preamble_length"],
    gain_db=new_settings["gain"],
    bitrate=new_settings["bitrate"]
)
ret = pozyx.setUWBSettings(uwb_settings)
if ret == 1:
    print(f"Settings for device {hex(me)} changed succefully.\n")
elif ret == 0:
    print(f"Cannot change settings for device {hex(me)}.\n")
else:
    print(f"Timeout for device {hex(me)}.\n")

# Connection test after settings change.
connected = 1
for d in devices:
    who_am_i = SingleRegister()
    pozyx.getWhoAmI(who_am_i, remote_id=d)
    if who_am_i == 0x43:
        connected += 1
        print(f"Device {hex(d)} is connected to network.")
    else:
        print(f"Device {hex(d)} is not connected!!!")
print(f"{connected}/{len(devices) + 1} devices connected to network.\n")

# New settings print.
uwb_settings = UWBSettings()
pozyx.getUWBSettings(uwb_settings)
print("New settings:")
print(uwb_settings)
