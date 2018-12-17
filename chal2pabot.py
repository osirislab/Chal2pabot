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
from art import *

def parse_args():
    parser=argparse.ArgumentParser(description='Chal2pa motherf*cker')
    parser.add_argument(
        '--init',
        dest='init',
        default=False,
        action='store_true',
        help='init state for program to set up challenge map (challenge checking does not run)'
    )
    parser.add_argument(
        '--debug',
        dest='debug',
        default=False,
        action='store_true',
        help='doesn\'t bitch in slack'
    )
    parser.add_argument(
        '-p', '--path',
        dest='path',
        type=str,
        default='./',
        help='path to repo (containing challenge.json\'s), or challenge_map.json file'
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
        default='https://hooks.slack.com/services/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',
        help='slack hook url for chal2pa to bitch to when a challenge is down'
    )
    return parser.parse_args()

args=parse_args()

SLACK_URL = '' #'https://hooks.slack.com/services/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'
PATH=args.path
INIT=args.init
DEBUG=args.debug
TIMEOUT=args.timeout
OFFLINE_CHALLENGES = set()
CHALLENGE_MAP = dict()

def find_ips(path):
    global CHALLENGE_MAP
    if os.path.isfile('path'):
        try:
            CHALLENGE_MAP=json.loads(open(path).read())
        except Json.decoder.JSONDecodeError as e:
            print('JSONDecodeError', e)
            exit(1)
    elif os.path.isdir(path):
        challenge_jsons = glob('{}/**/challenge.json'.format(REPO_PATH),recursive=True)
        for challenge_json in challenge_jsons:
            chal_data=json.loads(open(challenge_json).read())
            if 'name' in chal_data and 'url' in chal_data:
                CHALLENGE_MAP[chal_data['name']] = chal_data['url']
    print('Generating state.json with CHALLENGE_MAP:', json.dumps(CHALLENGE_MAP,indent=4))
    write_state()

def write_state():
    state_data = {
        'OFFLINE_CHALLENGES': list(OFFLINE_CHALLENGES),
        'CHALLENGE_MAP'     : CHALLENGE_MAP
    }
    with open('state.json', 'w') as f:
        json.dump(
            state_data,
            f,
            indent=4,
        )

def load_state():
    global OFFLINE_CHALLENGES, CHALLENGE_MAP
    if 'state.json' not in ls():
       write_state()
    with open('state.json', 'r') as f:
        state_data = json.loads(f.read())
        OFFLINE_CHALLENGES = set (state_data['OFFLINE_CHALLENGES'])
        CHALLENGE_MAP      = dict(state_data['CHALLENGE_MAP'])


def startup(init=False):
    if init:
        find_ips()
    load_state()

def check_http(url):
    try:
        return requests.get(url, timeout=TIMEOUT).status_code == 200
    except:
        return False


def check_sock(url):
    try:
        url, port = url.split(':')
        sock = socket.socket()
        sock.settimeout(TIMEOUT)
        sock.connect((url, int(port)))
        sock.send('chal2pabot\n'.encode())
        sock.recv(1024)
        return True
    except:
        return False


def check_chals():
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


def display_chal_report(chals):
    print('-' * 40)
    print('report: {}'.format(str(datetime.datetime.now())))
    for chal_name, is_running in chals.items():
        if is_running:
            symbol = plus
        else:
            symbol = minus
        print(symbol, CHALLENGE_MAP[chal_name], chal_name)


def send_slack(msg):
    print(msg)
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
    write_state()
    rep = 'Chalenges are down!\n' + '\n'.join(
        '-' + name + ' ' + url for name, url in  errors
    )
    if count > 0:
        if not DEBUG:
            send_slack(rep)


def check():
    chals = check_chals()
    if False in list(chals.values()):
        report_error(chals)
    display_chal_report(chals)
    

if __name__ == "__main__":
    print(gen_ascii('chal2pabot', font='starwars', c='yellow', frame='red'))
    startup(INIT)
    while True:
        check()
        time.sleep(30)
