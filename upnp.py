#!/usr/bin/env python3

from flask import Flask, jsonify, render_template
from fritzconnection import FritzConnection

app = Flask(__name__, static_url_path='/static')
fc = FritzConnection()


def get_link():
    return fc.call_action('WANCommonInterfaceConfig', 'GetCommonLinkProperties')


def get_connection():
    return fc.call_action('WANIPConnection', 'GetStatusInfo')


def get_ip():
    return fc.call_action('WANIPConnection', 'GetExternalIPAddress')['NewExternalIPAddress'], fc.call_action(
        'WANIPConnection', 'X_AVM_DE_GetIPv6Prefix')


@app.route('/status', methods=['GET'])
def status():
    link = get_link()
    connection = get_connection()
    ext_v4, ipv6 = get_ip()
    speeds = fc.call_action('WANCommonInterfaceConfig', 'GetAddonInfos')
    packetsr = fc.call_action('WANCommonInterfaceConfig', 'GetTotalPacketsReceived')['NewTotalPacketsReceived']
    packetss = fc.call_action('WANCommonInterfaceConfig', 'GetTotalPacketsSent')['NewTotalPacketsSent']

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
    json['total']['bytes'] = dict()
    json['total']['bytes']['up'] = speeds['NewTotalBytesSent']
    json['total']['bytes']['down'] = speeds['NewTotalBytesReceived']
    json['total']['packets'] = dict()
    json['total']['packets']['up'] = packetss
    json['total']['packets']['down'] = packetsr
    json['voip'] = dict()
    json['voip']['dns'] = [speeds['NewVoipDNSServer1'], speeds['NewVoipDNSServer2']]
    json['dns'] = [speeds['NewDNSServer1'], speeds['NewDNSServer2']]
    json['RoutedBridgedModeBoth'] = speeds['NewRoutedBridgedModeBoth']
    json['upnp'] = dict()
    json['upnp']['enabled'] = speeds['NewUpnpControlEnabled'] == '1'

    return jsonify(json)


@app.route('/', methods=['GET'])
def index():
    return render_template('fritz.htm')


if __name__ == '__main__':
    app.run()
