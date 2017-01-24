#!/usr/bin/env python3

import fritzconnection
from flask import Flask, jsonify
from flask.ext.cache import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
cache.init_app(app)


@app.route("/status", methods=['GET'])
@cache.cached(timeout=1)
def status():
    fc = fritzconnection.FritzConnection(address='10.0.0.1')
    link = fc.call_action('WANCommonInterfaceConfig', 'GetCommonLinkProperties')
    connection = fc.call_action('WANIPConnection', 'GetStatusInfo')
    speeds = fc.call_action('WANCommonInterfaceConfig', 'GetAddonInfos')
    ext_v4 = fc.call_action('WANIPConnection', 'GetExternalIPAddress')['NewExternalIPAddress']
    ipv6 = fc.call_action('WANIPConnection', 'X_AVM_DE_GetIPv6Prefix')

    json = dict()
    json['modelname'] = fc.modelname
    json['physical'] = dict()
    json['physical']['connected'] = link['NewPhysicalLinkStatus'] == 'Up'
    json['physical']['type'] = link['NewWANAccessType']
    json['physical']['rate'] = dict()
    json['physical']['rate']['up'] = link['NewLayer1UpstreamMaxBitRate'] / 8
    json['physical']['rate']['down'] = link['NewLayer1DownstreamMaxBitRate'] / 8
    json['logical'] = dict()
    json['logical']['connected'] = connection['NewConnectionStatus'] == 'Connected'
    json['logical']['lasterror'] = connection['NewLastConnectionError']
    json['logical']['uptime'] = connection['NewUptime']
    json['logical']['ipv4'] = ext_v4
    json['logical']['ipv6'] = dict()
    json['logical']['ipv6']['prefix'] = ipv6['NewIPv6Prefix']
    json['logical']['ipv6']['length'] = ipv6['NewPrefixLength']
    json['logical']['ipv6']['valid_lft'] = ipv6['NewValidLifetime']
    json['logical']['ipv6']['preferred_lft'] = ipv6['NewPreferedLifetime']
    json['rate'] = dict()
    json['rate']['up'] = speeds['NewByteSendRate']
    json['rate']['down'] = speeds['NewByteReceiveRate']
    json['total'] = dict()
    json['total']['up'] = speeds['NewTotalBytesSent']
    json['total']['down'] = speeds['NewTotalBytesReceived']

    return jsonify(json)

if __name__ == "__main__":
    app.run()
