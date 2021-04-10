def readable_hex(color):
    return(int(hex(int(color, 16)), 0))

def cleanup_channel_id(channel_id):
    channel_id = channel_id.replace('<', '')
    channel_id = channel_id.replace('>', '')
    channel_id = channel_id.replace('#', '')
    channel_id = int(channel_id)
    return channel_id    