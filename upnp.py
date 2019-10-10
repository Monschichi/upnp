#!/usr/bin/env python3

from flask import (
    Flask,
    jsonify,
    render_template,
)
from fritzconnection import FritzConnection, fritzconnection

app = Flask(__name__, static_url_path='/static')
fc = FritzConnection()


@app.route('/status', methods=['GET'])
def status():
    global fc
    try:
        link = fc.call_action('WANCommonIFC', 'GetCommonLinkProperties')
        connection = fc.call_action('WANIPConn', 'GetStatusInfo')
        ext_v4 = fc.call_action('WANIPConn', 'GetExternalIPAddress')['NewExternalIPAddress']
        ipv6 = fc.call_action('WANIPConn', 'X_AVM_DE_GetIPv6Prefix')
        speeds = fc.call_action('WANCommonIFC', 'GetAddonInfos')

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
        json['voip'] = dict()
        json['voip']['dns'] = [speeds['NewVoipDNSServer1'], speeds['NewVoipDNSServer2']]
        json['dns'] = [speeds['NewDNSServer1'], speeds['NewDNSServer2']]
        json['RoutedBridgedModeBoth'] = speeds['NewRoutedBridgedModeBoth']
        json['upnp'] = dict()
        json['upnp']['enabled'] = speeds['NewUpnpControlEnabled'] == '1'

        return jsonify(json)
    except fritzconnection.ServiceError:
        fc = FritzConnection()
        return jsonify(dict())


@app.route('/', methods=['GET'])
def index():
    return render_template('fritz.htm')


if __name__ == '__main__':
    app.run()
