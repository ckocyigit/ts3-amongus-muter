#!/usr/bin/python3

import ts3

with ts3.query.TS3Connection("192.168.178.200") as ts3conn:
    try:
        ts3conn.login(
            client_login_name="serveradmin",
            client_login_password="hRhTjxM9"
        )
    except ts3.query.TS3QueryError as err:
        print("Login failed:", err.resp.error["msg"])
        exit(1)

    ts3conn.use(sid=1)

    resp = ts3conn.clientlist()

    clientlist = resp.parsed

    for client in clientlist:
        if client["cid"] == "71":
            servergruppen = ts3conn.servergroupsbyclientid(cldbid=client["client_database_id"]).parsed
            hasGrp = False
            for gruppe in servergruppen:
                if gruppe["sgid"] == "51":
                    hasGrp = True
            if hasGrp:
                ts3conn.servergroupdelclient(sgid=51, cldbid=client["client_database_id"])
            else:
                ts3conn.servergroupaddclient(sgid=51, cldbid=client["client_database_id"])
