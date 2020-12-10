#!/usr/bin/python3

import ts3
import asyncio
import websockets
import json

teamspeakIP = "192.168.178.200"
teamspeakUser = "serveradmin"
teamspeakPassword = "hRhTjxM9"
teamspeakSID = 1
teamspeakAmongUsChannelID = "71"
teamspeakAmongUsServerGroupID = "51"
amongUsApiServerIP = "localhost"
amongUsApiServerPort = "42069"



def mute():
    with ts3.query.TS3Connection(teamspeakIP) as ts3conn:
        try:
            ts3conn.login(
                client_login_name=teamspeakUser,
                client_login_password=teamspeakPassword
            )
        except ts3.query.TS3QueryError as err:
            print("Login failed:", err.resp.error["msg"])
            exit(1)

        ts3conn.use(sid=teamspeakSID)

        resp = ts3conn.clientlist()

        clientlist = resp.parsed

        for client in clientlist:
            if client["cid"] == teamspeakAmongUsChannelID:
                servergruppen = ts3conn.servergroupsbyclientid(cldbid=client["client_database_id"]).parsed
                hasGrp = False
                for gruppe in servergruppen:
                    if gruppe["sgid"] == teamspeakAmongUsServerGroupID:
                        hasGrp = True
                if hasGrp:
                    ts3conn.servergroupdelclient(sgid=teamspeakAmongUsServerGroupID,
                                                 cldbid=client["client_database_id"])
                else:
                    ts3conn.servergroupaddclient(sgid=teamspeakAmongUsServerGroupID,
                                                 cldbid=client["client_database_id"])


def handleEvent(event):
    jsonMSG = json.loads(event)
    print(jsonMSG)
    if jsonMSG["EventID"] == 0:
        mute()
    pass


async def client():
    async with websockets.connect('ws://{}:{}/api'.format(amongUsApiServerIP, amongUsApiServerPort)) as websocket:
        while True:
            handleEvent(await websocket.recv())


asyncio.get_event_loop().run_until_complete(client())
