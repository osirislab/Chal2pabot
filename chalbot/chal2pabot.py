#!/usr/bin/env python3

import requests
import socket
import time
import datetime
import json
import argparse
import os
from glob import glob
from os import listdir as ls
from requests import get, post


def parse_args():
    parser=argparse.ArgumentParser(description='Chal2pa motherf*cker')
    parser.add_argument(
        '--debug',
        dest='debug',
        default=False,
        action='store_true',
        help='doesn\'t bitch in slack'
    )
    parser.add_argument(
        '-t', '--timeout',
        dest='timeout',
        type=int,
        default=10,
        help='timeout for challenge checking in seconds (default: 10)'
    )
    parser.add_argument(
        '-s', '--slack-url',
        dest='slack',
        type=str,
        default='',
        help='slack hook url for chal2pa to bitch to when a challenge is down'
    )
    return parser.parse_args()


args=parse_args()

SLACK_URL = args.slack
DEBUG=args.debug
TIMEOUT=args.timeout


def write_state():
    state_data = {
        'OFFLINE_CHALLENGES': list(OFFLINE_CHALLENGES),
        'CHALLENGE_MAP'     : CHALLENGE_MAP
    }
    post(
        'http://api:5000/chal/report',
        headers={'Content-Type':'application/json'},
        json=json.dump(state_data),
    )


def load_state():
    global OFFLINE_CHALLENGES, CHALLENGE_MAP
    state_data = get('http://api:5000/chal/list').json()
    OFFLINE_CHALLENGES = set (state_data['OFFLINE_CHALLENGES'])
    CHALLENGE_MAP      = dict(state_data['CHALLENGE_MAP'])


def check_http(url, n=0):
    if n == 3:
        return False
    try:
        return requests.get(url, timeout=TIMEOUT).status_code == 200
    except:
        return check_http(url, n+1)


def check_sock(url, n=0):
    if n == 3:
        return False
    try:
        url, port = url.split(':')
        sock = socket.socket()
        sock.settimeout(TIMEOUT)
        sock.connect((url, int(port)))
        sock.send('chal2pabot\n'.encode())
        sock.recv(1024)
        return True
    except:
        return check_sock(url, n+1)


def check_chals():
    global TIMEOUT
    chals = {}
    back_up = []
    for chal_name, url in CHALLENGE_MAP.items():
        chals[chal_name] = True
        if 'http' in url:
            func = check_http
        else:
            func = check_sock
        if not func(url):
            chals[chal_name] = False
        if chals[chal_name] and chal_name in OFFLINE_CHALLENGES:
            back_up.append(chal_name)
    if len(back_up) > 0:
        for name in back_up:
            OFFLINE_CHALLENGES.remove(name)
        write_state()
        report_up(back_up)
    return chals


def send_slack(msg):
    requests.post(
        SLACK_URL,
        json={'text':msg}
    )


def report_up(chal_list):
    msg = 'Chalenges are up!\n' + '\n'.join(
        '-' + name + ' ' + CHALLENGE_MAP[name] for name in chal_list
    )
    send_slack(msg)


def report_error(chals):
    errors=[]
    count=0
    for chal_name, is_active in chals.items():
        if not is_active and chal_name not in OFFLINE_CHALLENGES:
            count += 1
            errors.append((chal_name, CHALLENGE_MAP[chal_name],))
            OFFLINE_CHALLENGES.add(chal_name)
    rep = 'Challenges are down!\n' + '\n'.join(
        '-' + name + ' ' + url for name, url in  errors
    )
    if count > 0:
        if not DEBUG:
            send_slack(rep)


def check():
    chals = check_chals()
    if False in list(chals.values()):
        report_error(chals)


if __name__ == "__main__":
    load_state()
    check()
    write_state()
