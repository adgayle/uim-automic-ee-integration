#!/usr/bin/env python
'''Send data to Automic Event Engine'''

from optparse import OptionParser
import logging
import json
import configparser
import time
import requests
import datetime
import os
import sys

def send_alarm(api, alarm_data):
    '''Sends UIM alarm data to the Automic Event Engine via API

    Parameters:
        api (dict) of strings containing information to connect to the Automic Event Engine
        alarm_data (dict) of strings containing alarm details to send

    Returns:
        Nothing
    '''
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': ''
    }
    headers['Authorization'] = api['api_key']

    try:
        response = requests.post(
            api['url'],
            headers=headers,
            data=json.dumps(alarm_data)
        )
        logging.debug('The response from the get alarms was %s', response.text)
        if response.status_code == 200:
            logging.info('Successfully posted alarm data')
        else:
            logging.critical('Failed to post alarm data')

    except:
        logging.exception('Failed to call the Automic Event Engine API')
        print('Exception')


def main():
    '''Send data to Automic Event Engine'''

    exe_path = os.path.dirname(sys.executable)
    log_file = os.path.join(exe_path, 'aee-alarm-integration.log')

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'
    )

    usage = 'Usage: %prog [options] arg'
    parser = OptionParser(usage)
    parser.add_option(
        '-d', '--device', type='string', action='store',
        help='Device source of alarm'
    )
    parser.add_option(
        '-n', '--nimid', type='string', action='store',
        help='NIMID of alarm'
    )
    parser.add_option(
        '-s', '--severity', type='string', action='store',
        help='Severity text of alarm'
    )
    parser.add_option(
        '-m', '--message', type='string', action='store',
        help='Message text of alarm'
    )
    parser.add_option(
        '-t', '--time_received', type='string', action='store',
        help='Time alarm recieved'
    )
    (options, _) = parser.parse_args()

    
    a_time = datetime.datetime.fromtimestamp(1536083397).isoformat()
    alarm_data = {
        'type': '',
        'timestamp': '',
        'values': {
            'hostname': '',
            'nimid': '',
            'severity': '',
            'message': ''
        }
    }
    alarm_data['type'] = 'SIMPLE.EVENT'
    alarm_data['timestamp'] = a_time
    alarm_data['values']['hostname'] = options.device
    alarm_data['values']['nimid'] = options.nimid
    alarm_data['values']['severity'] = options.severity
    alarm_data['values']['message'] = options.message

    config = configparser.ConfigParser()
    config_file = os.path.join(exe_path, 'config.ini')
    config.read(config_file)
    automic_ee = {}
    automic_ee['api_key'] = config.get('automic', 'api_key')
    automic_ee['url'] = config.get('automic', 'url')
    send_alarm(automic_ee, alarm_data)



if __name__ == '__main__':
    main()