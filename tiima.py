#!/usr/bin/env python3

import argparse
import sys
import requests
import json
from bs4 import BeautifulSoup


def stamp(user, password, company, action):
    session = requests.Session()
    response = session.get("https://www.tiima.com/Login")
    cookies = session.cookies
    soup = BeautifulSoup(response.text, "html.parser")
    rvt = soup.find("input", {"name": "__RequestVerificationToken"})["value"]
    data = {
        "__RequestVerificationToken": rvt,
        "UserName": user,
        "Password": password,
        "CustomerIdentifier": company,
    }
    x = session.post("https://www.tiima.com/Login", data=data)
    soup = BeautifulSoup(x.text, "html.parser")
    form = soup.find("form", {"name": "tiima"})
    fields = form.findAll("input")
    formdata = dict((field.get("name"), field.get("value")) for field in fields)
    formdata["AjaxRequest"] = 1
    formdata["FieldAction"] = action
    formdata["StampReasonCodeId"] = 1
    response = session.post(
        "https://www.tiima.com/Tiima/workhours/work_time_stamp.asp", data=formdata
    )

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.findAll("table")[1].findAll("table")[6]
    rows = table.findAll("tr")
    del rows[0:2]
    for row in rows:
        cols = row.findAll("td")
        cols = [ele.get_text().strip() for ele in cols]
        print(" ".join([ele for ele in cols if ele]))


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="action", choices=["in", "out"], help="Action")
    parser.add_argument("-u", "--user", required=True)
    parser.add_argument("-p", "--password", required=True)
    parser.add_argument("-c", "--company", required=True)

    args = parser.parse_args()
    actions = {
        "in": "action_check_in",
        "out": "action_check_out",
        # Add other actions
    }

    stamp(args.user, args.password, args.company, actions.get(args.action))


if __name__ == "__main__":
    main(sys.argv[1:])
