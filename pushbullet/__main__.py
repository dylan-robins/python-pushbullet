#!/usr/bin/python3
import argparse

from .pushbullet import PushbulletDevices, PushbulletPushes


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
