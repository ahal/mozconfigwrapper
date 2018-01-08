# Mozconfigwrapper
[![Build Status](https://travis-ci.org/ahal/mozconfigwrapper.svg?branch=master)](https://travis-ci.org/ahal/mozconfigwrapper)
[![PyPI version](https://badge.fury.io/py/mozconfigwrapper.svg)](https://badge.fury.io/py/mozconfigwrapper)

Mozconfigwrapper is just like [virtualenvwrapper](http://www.doughellmann.com/projects/virtualenvwrapper/)
except for [mozconfigs](https://developer.mozilla.org/en/Configuring_Build_Options).
Mozconfigwrapper basically hides all your mozconfigs away in a configurable directory (defaults to ~/.mozconfigs)
and allows you to easily create, switch, delete and edit them. Mozconfigs remain active across terminal sessions.

# Installation Instructions

First make sure you have [pip](http://pip.readthedocs.org/en/latest/installing.html) installed.

Follow these simple steps to get mozconfigwrapper running:

    sudo pip install mozconfigwrapper

Then open your ~/.bashrc file (or equivalent) and add the line:

    source /usr/local/bin/mozconfigwrapper.sh

Note: mozconfigwrapper.sh may be in a different location on your system,
use `which mozconfigwrapper.sh` to find it.

Finally run:

    source ~/.bashrc

Mozconfigwrapper is now installed.

# Usage

You can create, remove, switch, list and edit mozconfigs.

To build with (activate) a mozconfig named foo, run:

    buildwith foo

To create a mozconfig named foo, run:

    mkmozconfig foo

To delete a mozconfig named foo, run:

    rmmozconfig foo

To see the currently active mozconfig, run:

    mozconfig

To list all mozconfigs, run:

    mozconfig -l

To edit the currently active mozconfig, run (the $EDITOR variable must be set):

    mozconfig -e


# Configuration

#### mozconfig location

By default mozconfigs are stored in the ~/.mozconfigs directory, but you can override this by setting the
$BUILDWITH_HOME environment variable.
e.g, add:

    export BUILDWITH_HOME=~/my/custom/mozconfig/path

to your ~/.bashrc file (or equivalent).

#### buildwith command

When running the buildwith command, `export MOZCONFIG=<path to mozconfig>` is run by default.
You can run any other command by overriding the ``BUILDWITH_COMMAND``.
For example, if you put this in your ~/.bashrc file (or equivalent):

    export BUILDWITH_COMMAND="export MOZCONFIG=#1; launchctl setenv MOZCONFIG #1"

buildwith will also set the MOZCONFIG environment variable in launchctl (useful when running Android Studio).
All `#1` occurences will be replaced by the path to the mozconfig file.

#### mozconfig template

When you make a new mozconfig, it will be populated with some basic build commands and the name of the mozconfig
will be appended to the end of the OBJDIR instruction. You can modify what gets populated by default by editing
the ~/.mozconfigs/.template file. For example, if I wanted my default configuration to store object directories
in a folder called objdirs and enable debugging and tests, I'd edit the ~/.mozconfigs/.template file to look like:

    mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/objdirs/
    ac_add_options --enable-application=browser
    ac_add_options --enable-debug
    ac_add_options --enable-tests

Now if I ran the command 'mkmozconfig foo', foo would be populated with the above and have the word 'foo'
appended to the first line.
