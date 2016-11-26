#!/usr/bin/env python3

import fritzconnection
from flask import Flask
from flask import jsonify
from flask.ext.cache import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
cache.init_app(app)

fc  = fritzconnection.FritzConnection(address='10.0.0.1')

@app.route("/status",methods=['GET'])
@cache.cached(timeout=1)
def status():
    link = fc.call_action('WANCommonInterfaceConfig','GetCommonLinkProperties')
    connection = fc.call_action('WANIPConnection', 'GetStatusInfo')
    speeds = fc.call_action('WANCommonInterfaceConfig','GetAddonInfos')

    json = dict()
    json['physical'] = dict()
    json['physical']['connected'] = link['NewPhysicalLinkStatus'] == 'Up'
    json['physical']['type'] = link['NewWANAccessType']
    json['physical']['rate'] = dict()
    json['physical']['rate']['up'] = link['NewLayer1UpstreamMaxBitRate']/8
    json['physical']['rate']['down'] = link['NewLayer1DownstreamMaxBitRate']/8
    json['logical'] = dict()
    json['logical']['connected'] = connection['NewConnectionStatus'] == 'Connected'
    json['logical']['lasterror'] = connection['NewLastConnectionError']
    json['logical']['uptime'] = connection['NewUptime']
    json['rate'] = dict()
    json['rate']['up'] = speeds['NewByteSendRate']
    json['rate']['down'] = speeds['NewByteReceiveRate']
    json['total'] = dict()
    json['total']['up'] = speeds['NewTotalBytesSent']
    json['total']['down'] = speeds['NewTotalBytesReceived']

    return jsonify(json)

if __name__ == "__main__":
    app.run()
