#!/usr/bin/python3.6
from aiohttp import web
import csv
import json
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

json_data = {"result": []}
with open(f"{base_dir}/dummy_data.csv", "r") as f:
    reader = list(csv.reader(f))
    head = reader[0]
    for row in reader[1:]:
        json_data["result"].append({k: v for k, v in zip(head, row)})

with open(f"{base_dir}/dummy_data.csv", "r") as f:
    csv_data = f.read()


async def serve_dummy_data(request):
    # resolve query params
    tm = request.rel_url.query["tm"]
    rpc_data = request.rel_url.query["rpc"]

    # get outputType
    rpc_data = json.loads(rpc_data)
    output_type = rpc_data.get("params", {}).get("outputType")
    if output_type == "json":
        os.sys.stdout.wrtie("json output")
        return web.json_response(data=json_data)
    elif output_type == "csv":
        os.sys.stdout.wrtie("csv output")
        return web.Response(text=csv_data)
    else:
        return web.Response(text=f"not support outputType: '{output_type}'", status=400)


if __name__ == "__main__":
    app = web.Application()
    app.router.add_route("GET", "/vnm-api/index.php", serve_dummy_data)
    web.run_app(app, host="0.0.0.0", port=80)
