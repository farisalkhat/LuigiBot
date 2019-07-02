from db import gachadatabase

def gacha_allowed(SERVERID,CHANNELID):
    if gachadatabase.get_gacha_channel([SERVERID,CHANNELID]):
        return True
    return False