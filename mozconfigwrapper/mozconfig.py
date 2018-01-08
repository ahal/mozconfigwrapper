#!/usr/bin/env python
"""
Utility to make working with mozconfigs easier
"""

import shutil
import subprocess
import sys
import os
from argparse import ArgumentParser

here = os.path.dirname(os.path.realpath(__file__))
mozconfigdir = os.getenv('BUILDWITH_HOME', os.path.expanduser("~/.mozconfigs"))
special_files = ['.template', '.active']


def mkmozconfig(name):
    if not os.path.isdir(mozconfigdir):
        os.makedirs(mozconfigdir)

    mozconfig = os.path.join(mozconfigdir, name)
    template = os.path.join(mozconfigdir, '.template')
    if not os.path.isfile(template):
        shutil.copyfile(os.path.join(here, 'template'), template)
    shutil.copyfile(template, mozconfig)

    f = open(mozconfig, 'r')
    lines = f.readlines()
    f.close()
    lines = [line.rstrip() + name + '\n' if line.find("MOZ_OBJDIR") != -1
             else line for line in lines]
    f = open(mozconfig, 'w')
    f.writelines(lines)
    f.close()


def mozconfig(args=sys.argv[1:]):
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-l", "--list",
                        dest="ls",
                        action="store_true",
                        default=False,
                        help="lists all available mozconfigs")
    parser.add_argument('-e', '--edit',
                        dest="edit",
                        action="store_true",
                        default=False,
                        help="opens the active mozconfig for editing")
    args = parser.parse_args(args)

    current = os.getenv('MOZCONFIG', '')
    if not args.ls and not args.edit:
        if current == '':
            print("No mozconfig activated")
        else:
            print(current)
        return

    if args.ls and os.path.isdir(mozconfigdir):
        for f in sorted(os.listdir(mozconfigdir)):
            if f not in special_files:
                if current != '' and f == os.path.basename(current):
                    f += "*"
                print(f)

    if args.edit:
        if current == '':
            print("No mozconfig activated")
        else:
            _edit(current)


def _edit(mozconfig):
    editor = os.getenv('EDITOR')
    if not editor:
        print("Can't open editor, EDITOR environment variable not set")
    else:
        subprocess.call([editor, mozconfig])


if __name__ == '__main__':
    sys.exit(mozconfig())
