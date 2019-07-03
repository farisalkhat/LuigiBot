from db import database

def permission(serverid,channelid):
    if database.get_botchannel([serverid,channelid]):
        return True
    return False


