#!/usr/bin/env python3

import argparse
import json
import sys

import requests
from bs4 import BeautifulSoup

API_URL = "https://www.tiima.com/rest/api/mobile"
API_KEY = "ADD_API_KEY_HERE!!!"
COMPANY = "ADD_COMPANY_ID_HERE"


def login(user, password):
    json = {
        "username": user,
        "password": password,
        "clientVersion": "0.1",
        "deviceType": "Android",
        "deviceDescription": "Oneplus 3T",
    }
    resp = requests.post(API_URL + "/user/login", json=json, auth=(COMPANY, API_KEY))
    return resp.json()


def stamp(token, url, json):
    headers = {"X-Tiima-Token": token, "X-Tiima-Language": "fi"}
    resp = requests.post(
        API_URL + url, json=json, auth=(COMPANY, API_KEY), headers=headers
    )
    return resp.json()


def action_check_in(token):
    json = {"reasonCode": 1}
    resp = stamp(token, "/user/enter", json)
    print(resp)


def action_check_out(token):
    json = {"reasonCode": 1}
    resp = stamp(token, "/user/leave", json)
    print(resp)


def action_to_lunch(token):
    resp = stamp(token, "/user/toLunch", {})
    print(resp)


def action_from_lunch(token):
    resp = stamp(token, "/user/fromLunch", {})
    print(resp)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        dest="action", choices=["in", "out", "lunch", "back"], help="Action"
    )
    parser.add_argument("-u", "--user", required=True)
    parser.add_argument("-p", "--password", required=True)

    args = parser.parse_args()
    actions = {
        "in": "action_check_in",
        "out": "action_check_out",
        "lunch": "action_to_lunch",
        "back": "action_from_lunch",
        # Add other actions
    }

    user = login(args.user, args.password)
    globals()[actions.get(args.action)](user.get("token"))


if __name__ == "__main__":
    main(sys.argv[1:])
