from pypozyx import DeviceCoordinates, Coordinates, PozyxConstants
import csv
import yaml

def load_anchors() -> list:
    anchors = []
    with open('anchors.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader, None) 
        for row in csv_reader:
            id = int(row[0], 16)
            isAnchor = bool(row[1])
            x = int(float(row[2]) * 1000)
            y = int(float(row[3]) * 1000)
            z = int(float(row[4]) * 1000)

            coordinates = Coordinates(x, y, z)
            anchors.append(DeviceCoordinates(network_id=id, flag=isAnchor, pos=coordinates))

            if isAnchor == 1:
                dev_str = 'anchor'
            else:
                dev_str = 'tag'

            print(f"[{id} as {dev_str}]:\tx:{x}\ty={y}\tz={z}")

        print(f'Anchors loaded succesfully.')
    return anchors


def load_settings() -> dict:
    with open('settings.yaml') as file:
        loader = yaml.load(file, Loader=yaml.FullLoader)

    if(int(loader['channel']) in [2, 3, 4, 5, 7]):
        channel = int(loader['channel'])
    else:
        return None

    if(loader['bitrate'] == '110_kbps'):
        bitrate = PozyxConstants.UWB_BITRATE_110_KBPS
    elif(loader['bitrate'] == '6810_kbps'):
        bitrate = PozyxConstants.UWB_BITRATE_6810_KBPS
    elif(loader['bitrate'] == '850_kbps'):
        bitrate = PozyxConstants.UWB_BITRATE_850_KBPS
    else:
        return None
    
    if(loader['pulse_repetition_frequecy'] == '16_MHz'):
        pulse_repetition_frequecy = PozyxConstants.UWB_PRF_16_MHZ
    elif(loader['pulse_repetition_frequecy'] == '64_MHz'):
        pulse_repetition_frequecy = PozyxConstants.UWB_PRF_64_MHZ
    else: 
        return None

    if(int(loader['preamble_length']) == 64):
        preamble_length = PozyxConstants.UWB_PLEN_64
    elif(int(loader['preamble_length']) == 128):
        preamble_length = PozyxConstants.UWB_PLEN_128
    elif(int(loader['preamble_length']) == 256):
        preamble_length = PozyxConstants.UWB_PLEN_256
    elif(int(loader['preamble_length']) == 512):
        preamble_length = PozyxConstants.UWB_PLEN_512
    elif(int(loader['preamble_length']) == 1024):
        preamble_length = PozyxConstants.UWB_PLEN_1024
    elif(int(loader['preamble_length']) == 2048):
        preamble_length = PozyxConstants.UWB_PLEN_2048
    elif(int(loader['preamble_length']) == 4096):
        preamble_length = PozyxConstants.UWB_PLEN_4096
    else:
        return None

    gain = float(int(float(loader['gain']) / 0.5)) * 0.5
    if(gain < 0 or gain > 33.5):
        return None
    
    new_settings = {
        "channel": channel,
        "bitrate": bitrate,
        "pulse_repetition_frequecy": pulse_repetition_frequecy,
        "preamble_length": preamble_length,
        "gain": gain
    }

    return new_settings
