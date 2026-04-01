# mozconfigwrapper
[![PyPI version](https://badge.fury.io/py/mozconfigwrapper.svg)](https://badge.fury.io/py/mozconfigwrapper)
[![CI](https://github.com/ahal/mozconfigwrapper/actions/workflows/ci.yml/badge.svg)](https://github.com/ahal/mozconfigwrapper/actions/workflows/ci.yml)

Mozconfigwrapper is a Python + shell tool to manager your [mozconfigs](https://firefox-source-docs.mozilla.org/setup/configuring_build_options.html).
Mozconfigwrapper hides all your mozconfigs away in a configurable directory (defaults to ~/.mozconfigs)
and allows you to easily create, switch, delete and edit them. Mozconfigs remain active across shell sessions.

## Installation

Mozconfigwrapper is on PyPi as the `mozconfigwrapper` pacakge. The recommended method to install it is via [uv](https://docs.astral.sh/uv/getting-started/installation/):

    uv tool install mozconfigwrapper

Then open your ~/.bashrc file (or equivalent) and add the line:

    source $(which mozconfigwrapper.sh)

Finally run:

    source ~/.bashrc

## Usage

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


## Configuration

#### mozconfig location

By default mozconfigs are stored in the ~/.mozconfigs directory, but you can override this by setting the
$BUILDWITH_HOME environment variable.
e.g, add:

    export BUILDWITH_HOME=~/my/custom/mozconfig/path

to your ~/.bashrc file (or equivalent).

#### buildwith command

When running the buildwith command, `export MOZCONFIG=<path to mozconfig>` is run by default.
You can use any other command by overriding the ``BUILDWITH_COMMAND`` environment variable.
For example, if you put this in your ~/.bashrc file (or equivalent):

    export BUILDWITH_COMMAND="export MOZCONFIG=#1 && launchctl setenv MOZCONFIG #1"

buildwith will also set the MOZCONFIG environment variable in launchctl (useful when running Android Studio).
All occurences of ``#1`` will be replaced by the path to the mozconfig file.

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
