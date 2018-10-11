#!/usr/bin/env python3

SLACK_URL = 'https://hooks.slack.com/services/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'
REPO_PATH = '~/osiris/RED'
DEBUG = False
TIMEOUT = 10


import requests
import socket
import time
import datetime
import json
from glob import glob
from os import listdir as ls
from art import *

OFFLINE_CHALLENGES = set()
CHALLENGE_MAP = dict()

def load_ips():
    global CHALLENGE_MAP
    if os.path.isfile('ip.json'):
        print(warning, 'reading from challenge_map.json')
        CHALLENGE_MAP = json.loads(open('challenge_map.json').read())
    else:
        challange_jsons = glob('{}/*/challange.json'.format(REPO_PATH))
        for challange_json in challange_jsons:
            chal_data=json.loads(open(challange_json).read())
            if 'name' in chal_data and 'url' in chal_data:
                CHALLENGE_MAP[chal_data['name']] = chal_data['url']

def write_state():
    state_data = {
        'OFFLINE_CHALLENGES': list(OFFLINE_CHALLENGES),
    }
    with open('state.json', 'w') as f:
        json.dump(
            state_data,
            f,
            indent=4,
        )

def load_state():
    if 'state.json' not in ls():
       write_state()
    global OFFLINE_CHALLENGES
    with open('state.json', 'r') as f:
        OFFLINE_CHALLENGES = set(json.loads(f.read())['OFFLINE_CHALLENGES'])

def startup():
    load_ips()
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
        sock.send('blah\n'.encode())
        sock.recv(1024)
        return True
    except:
        pass
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
    startup()
    while True:
        check()
        time.sleep(30)
