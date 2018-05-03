#!/usr/bin/env python3
import coloredlogs
import logging
import signal
import requests
import configparser
import json
import sys

METADATA = {
  "version": "psn-client v0.1",
  "doc": """
PubSubNet CLIent for testing and hacking

Usage: client.py [options]

General
  -h,       --help          Show this help
  -v,       --version       Print the program version
  -q=<num>, --noise=<num>   Verbosity, where 0 is quietest and 4 is loudest
  -n,       --no-commit     Dry run: Open all files and databases as read-only
                            All web requests will be spoofed and probably fail

Configuration
  -c=<file>, --config=<file>  Use a different global configuration file
                              If <file> is blank no config is read / written
                              Otherwise the default of ~/psn-client.* is used
  -C=<fmt>,  --cfgfmt=<fmt>   Force config file format instead of guessing
                              Case-insensitive one of 'json' or 'ini'
  -d=<dir>,  --dir=<dir>      Use a different data and config directory
                              If <dir> is blank no user data is read or written
                              Otherwise the default of ~/.psn-client/ is used

Logging
  -l=[file], --log=[file]     Write a new logfile, possibly called "file"

Anti-security (unsafe)
  -S=<flags>,  --insecurity=<flags>  Be unsafe as specified by <flags>:
                t don't enforce SSL (TLS)
                p print and log client passwords and secrets in plain text
                c skip and disable all encryption and signature protections
                s like -S=tpc but disables even more

Option values configured in the default INI or JSON config file will be
  overridden by option values given on the command line

"""
}
__version__ = METADATA["version"]


global logger


def interface():
    pass


def sigterm_handler(signo, stack_frame):
    print()
    global logger
    logger.critical("exiting")
    sys.exit(0)


def entry():
    from docopt import docopt
    from pprint import pprint
    args = docopt(METADATA["doc"], version=METADATA["version"])
    if args["-v"]:
        print(METADATA["version"])
        sys.exit(0)

    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)
    coloredlogs.install(
        level={4: "NOTSET", 3: "CRITICAL", 2: "WARNING", 1: "INFO", 0: ""}
              .get(int(args["-q"][1:])),  # noqa
        fmt="%(name)s[%(process)d] %(levelname)s %(message)s"
    )
    global logger
    logger = logging.getLogger("client")

    pprint(args)


if __name__ == '__main__':
    entry()
