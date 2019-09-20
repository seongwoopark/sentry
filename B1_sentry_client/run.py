#!/usr/bin/python3.6
import aiohttp
import asyncio
import csv
from datetime import datetime, timezone, timedelta
import json
import os
from yarl import URL

"""
To understand real sentry server behaviour, please refer following link on your browser, 
http://192.168.0.96/vnm-api/help.php
there is a lot of helpful description and docs
"""

base_dir = "/var/sentry.d"
# base_dir = os.path.dirname(os.path.abspath(__file__))     # current file path, use this if you want to save file here

server_addresses = [
    #### Mocked Sentry Server ip address list ####
    # "127.0.0.1",
    # "127.0.0.1",
    # "127.0.0.1",

    #### Real Sentry Server ip address list ####
    "192.168.0.96",
    "192.168.0.97",   # NOTE: not working with user: "Administrator" password: "none!!"
    "192.168.0.106"
]
auth = aiohttp.BasicAuth(login="Administrator", password="none!!")


async def fetch_sentry_data(session, ip_address, now, retry=0):
    # setup request data
    headers = {
        "Content-Type": "text/html; charset=UTF-8",
        "Referer": f"http://{ip_address}/vnm-api/api_test.php?id_json_rpc",
    }
    rpc_data = {
        "id": 1,
        "jsonrpc": 2.0,
        "method": "Report.GetPortStatistics",
        "params": {
            "outputType": "json",
            "fromDate": now.strftime("%m/%d/%y"),
            "fromTime": now.strftime("%I:%M:%S %p"),
            "toDate": (now + timedelta(minutes=5)).strftime("%m/%d/%y"),
            "toTime": (now + timedelta(minutes=5)).strftime("%I:%M:%S %p"),
            "span": "5 minutes",
            "types": [1, 2, 3],
            "availabilityProduct": "sentry"
        }
    }
    query_params = {
        "tm": str(now.timestamp()), "rpc": json.dumps(rpc_data)
    }
    url = URL(f"http://{ip_address}/vnm-api/index.php").update_query(query_params)

    # get request
    async with session.get(url=url, headers=headers) as response:
        # failed check
        response.raise_for_status()

        # success
        response = await response.json()
        if response.get("code") == -32000 and retry < 7:
            await asyncio.sleep(2**retry)
            return await fetch_sentry_data(session=session, ip_address=ip_address, now=now, retry=retry + 1)
        return response


async def main():
    # get current time as KST
    now = datetime.now(tz=timezone(timedelta(hours=9)))

    # request to all of sentry servers
    async with aiohttp.ClientSession(auth=auth) as session:
        responses = await asyncio.gather(
            *[fetch_sentry_data(session=session, ip_address=ip_address, now=now) for ip_address in server_addresses],
            return_exceptions=True
        )

    # post process
    results = []
    failed = []
    can_be_retried = []
    for response, ip_address in zip(responses, server_addresses):
        # failed
        if not isinstance(response, dict):
            failed.append((ip_address, response))
            continue
        # success
        result, code = response.get("result"), response.get("code")
        if result:
            results.extend(result)
        elif code == -32000:
            can_be_retried.append(ip_address)

    # system out for log
    for ip_address, response in failed:
        os.sys.stderr.write(f"[ERROR] {ip_address} is not working, response: {response}\n")
    for ip_address in can_be_retried:
        os.sys.stderr.write(f"[WARNING] {ip_address} need to be retried\n")

    # write data
    if results:
        with open(f"{base_dir}/{now.strftime('%Y%m%d_%H%M%S')}_complete.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            for row in results:
                writer.writerow(row)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
