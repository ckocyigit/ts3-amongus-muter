#!/usr/bin/python3

import ts3
import asyncio
import websockets
import json

with open('config.json', 'r') as f:
    config = json.load(f)
    print("Loading config file: ", config)

teamspeakIP = config["teamspeakIP"]
teamspeakUser = config["teamspeakUser"]
teamspeakPassword = config["teamspeakPassword"]
teamspeakSID = config["teamspeakSID"]
teamspeakAmongUsChannelID = config["teamspeakAmongUsChannelID"]
teamspeakAmongUsServerGroupID = config["teamspeakAmongUsServerGroupID"]
amongUsApiServerIP = config["amongUsApiServerIP"]
amongUsApiServerPort = config["amongUsApiServerPort"]

deaths = list()


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
                for gruppe in servergruppen:
                    if gruppe["sgid"] == teamspeakAmongUsServerGroupID:
                        pass
                    else:
                        ts3conn.servergroupdelclient(sgid=teamspeakAmongUsServerGroupID,
                                                     cldbid=client["client_database_id"])


def demute():
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
                for gruppe in servergruppen:
                    if gruppe["sgid"] == teamspeakAmongUsServerGroupID:
                        ts3conn.servergroupdelclient(sgid=teamspeakAmongUsServerGroupID, cldbid=client["client_database_id"])


def handleEvent(event):
    jsonMSG = json.loads(event)
    event = jsonMSG["EventID"]
    eventData = jsonMSG["EventData"]
    print(jsonMSG)

    if event == 0:
        newstate = json.loads(eventData)["NewState"]
        if newstate == 1:
            mute()
        elif newstate == 2:
            demute()
    elif event == 1:
        deathstate = json.loads(eventData)
        deaths.append(deathstate["Name"])
        print("added {} to deathsarray".format(deathstate["Name"]))
        # jemand ist gestorben
        pass
    elif event == 2:
        # kp
        pass
    elif event == 3:
        # {'EventID': 3, 'EventData': '{"GameOverReason":1,"PlayerInfos":[{"Name":"not hamses","IsImpostor":true},{"Name":"H2theUBERT","IsImpostor":true},{"Name":"monokel","IsImpostor":true},{"Name":"Pottsau","IsImpostor":true},{"Name":"Adrian","IsImpostor":true},{"Name":"Red","IsImpostor":true}]}'}
        # "GameOverReason":0 imposter wins
        # "GameOverReason":1 crew wins
        demute()


async def client():
    async with websockets.connect('ws://{}:{}/api'.format(amongUsApiServerIP, amongUsApiServerPort)) as websocket:
        while True:
            handleEvent(await websocket.recv())


asyncio.get_event_loop().run_until_complete(client())
