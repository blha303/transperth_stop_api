#!/usr/bin/env python3
from flask import *
from requests import get
from time import time

app = Flask(__name__)
cache = {}

def get_stop_info(stop):
    html = get("http://136213.mobi/Bus/StopResults.aspx", params={"SN": stop}).text
    if html.count('<div class="tpm_row_content"') <= 2:
        return {"error": "No services for that stop today"}
    stops = html.split("<div class=\"tpm_row_content\">")[1:-1]
    outp = {"results": []}
    for stop_html in stops:
        outp["results"].append([c.split("<br")[0] for c in stop_html.split("</strong> ")[1:]])
    return outp

@app.route("/<stop>")
def get_stop(stop):
    if stop in cache:
        if time() - cache[stop]["time"] <= 1800:
            outp = dict(cached=True, **cache[stop])
            outp.pop("time")
            return jsonify(outp)
    else:
        outp = get_stop_info(stop)
        cache[stop] = dict(time=time(), **outp)
        return jsonify(dict(cached=False, **outp))

if __name__ == "__main__":
    app.run(port=36381, debug=True)
