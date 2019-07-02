from db import gachadatabase
from db import database
def gacha_allowed(SERVERID,CHANNELID):
    if gachadatabase.get_gacha_channel([SERVERID,CHANNELID]):
        return True
    return False

def permission(serverid,channelid):
    if database.get_botchannel([serverid,channelid]):
        return True
    return False
