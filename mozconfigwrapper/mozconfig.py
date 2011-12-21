#!/usr/bin/env python
from optparse import OptionParser
import shutil
import sys
import os

"""
Utility to make working with mozconfigs easier
"""

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

def mozconfig(arguments=sys.argv[1:]):
    parser = OptionParser(description=__doc__, usage="%prog [options]")
    parser.add_option("-l",
                      dest="ls",
                      action="store_true",
                      default=False,
                      help="lists all available mozconfigs")
    parser.add_option('-e', '--edit',
                      dest="edit",
                      action="store_true",
                      default=False,
                      help="opens the mozconfig for editing"),
    opt, args = parser.parse_args(arguments)

    current = os.getenv('MOZCONFIG', '')
    if not opt.ls and not opt.edit:
        if current == '':
            print "No mozconfig activated"
        else:
            print current
        return

    if opt.ls and os.path.isdir(mozconfigdir):
        for f in os.listdir(mozconfigdir):
            if f not in special_files:
                if current != '' and f == os.path.basename(current):
                    f += "*"
                print f

    if opt.edit:
        if current == '':
            print "No mozconfig activated"
        else:
            _edit(current)



def _edit(mozconfig):
    editor = os.getenv('EDITOR')
    if not editor:
        print "Can't open editor, EDITOR environment variable not set"
    else:
        cmd = editor + ' ' + mozconfig
        os.system(cmd)


if __name__ == '__main__':
    sys.exit(mozconfig())
