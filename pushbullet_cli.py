#!/usr/bin/env python

import argparse
from os import getenv
from typing import *

import requests
from dotenv import load_dotenv

# load necessary environment variables
load_dotenv()
PUSHBULLET_API_KEY = getenv("PUSHBULLET_API_KEY")


class Device:
    """Class representing a device"""

    def __init__(self, device_info: dict[str, Any]):
        self.info = device_info

    def __getattr__(self, key):
        return self.info[key]

    def print(self) -> None:
        print(f"{self.nickname:<20} | {self.kind:<10}")


class PushbulletDevices:
    @staticmethod
    def get_device_list() -> list[dict[str, Any]]:
        """Returns the list of devices attached to the user's account"""

        headers = {"Access-Token": PUSHBULLET_API_KEY}
        req = requests.get("https://api.pushbullet.com/v2/devices", headers=headers)

        # get list of devices
        response = req.json()
        return [Device(device) for device in response["devices"] if device["active"]]

    @classmethod
    def print_device_list(cls) -> None:
        # print list of devices
        for device in cls.get_device_list():
            device.print()


class PushbulletPushes:
    @staticmethod
    def post_note(device: Optional[str], title: str, body: str) -> bool:
        """Pushes a notification to a device"""

        content = {"type": "note", "title": title, "body": body}
        # if device is specified, add it to the request content
        # otherwise, leave it out to push to all devices
        if device is not None:
            content["device_iden"] = device

        headers = {
            "Access-Token": PUSHBULLET_API_KEY,
            "Content-Type": "application/json",
        }

        req = requests.post(
            "https://api.pushbullet.com/v2/pushes", headers=headers, json=content
        )

        return req.status_code == requests.codes.ok


class Handler:
    @staticmethod
    def post_handler(args: argparse.Namespace):
        """Handles the options given to the 'post' subparser"""

        # find the iden str of the specified device:
        device_iden = None
        if args.device is not None:
            try:
                device_iden = next(
                    filter(
                        lambda device: device.nickname == args.device,
                        PushbulletDevices.get_device_list(),
                    )
                ).iden
            except StopIteration:
                print("Error: couldn't find device {args.device}. Available devices:")
                PushbulletDevices.print_device_list()
                exit(1)

        PushbulletPushes.post_note(device_iden, args.title, args.body)

    @staticmethod
    def devices_handler(args: argparse.Namespace):
        """Handles the options given to the 'devices' subparser"""

        PushbulletDevices.print_device_list()


def main() -> None:
    # define parsers
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    subparsers.required = True

    post_parser = subparsers.add_parser("post", help="Posts a notification")
    post_parser.add_argument(
        "-t", "--title", help="Title of the notificatiton", type=str, required=True
    )
    post_parser.add_argument(
        "-b", "--body", help="Body of the notificatiton", type=str, required=True
    )
    post_parser.add_argument(
        "-d", "--device", help="Name of the receiving device", type=str
    )
    post_parser.set_defaults(func=Handler.post_handler)

    devices_parser = subparsers.add_parser(
        "devices", help="Lists devices attached to the account"
    )
    devices_parser.set_defaults(func=Handler.devices_handler)

    # parse arguments and dispatch to subparser callbacks
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
