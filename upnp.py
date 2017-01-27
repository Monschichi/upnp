#!/usr/bin/env python3

import fritzconnection
from flask import Flask, jsonify
from flask.ext.cache import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
cache.init_app(app)
fc = fritzconnection.FritzConnection(address='10.0.0.1')


@cache.cached(timeout=5, key_prefix='link')
def get_link():
    return fc.call_action('WANCommonInterfaceConfig', 'GetCommonLinkProperties')


@cache.cached(timeout=10, key_prefix='connection')
def get_connection():
    return fc.call_action('WANIPConnection', 'GetStatusInfo')


@cache.cached(timeout=20, key_prefix='ipv4')
def get_ipv4():
    return fc.call_action('WANIPConnection', 'GetExternalIPAddress')['NewExternalIPAddress']


@cache.cached(timeout=20, key_prefix='ipv6')
def get_ipv6():
    return fc.call_action('WANIPConnection', 'X_AVM_DE_GetIPv6Prefix')


@cache.cached(timeout=0.9)
@app.route("/status", methods=['GET'])
def status():
    link = get_link()
    connection = get_connection()
    ext_v4 = get_ipv4()
    ipv6 = get_ipv6()
    speeds = fc.call_action('WANCommonInterfaceConfig', 'GetAddonInfos')

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
