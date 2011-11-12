Mozconfigwrapper is just like [virtualenvwrapper](http://www.doughellmann.com/projects/virtualenvwrapper/)
except for [mozconfigs](https://developer.mozilla.org/en/Configuring_Build_Options). 
Mozconfigwrapper basically hides all your mozconfigs away in a configurable directory (defaults to ~/.mozconfigs) 
and allows you to easily create, switch, delete and edit them. Mozconfigs remain active across terminal sessions.
Mozconfigwrapper is currently Unix only.

# Installation Instructions

First make sure you have [setuptools](http://pypi.python.org/pypi/setuptools) installed.

Follow these simple steps to get mozconfigwrapper running:
 
    sudo easy_install pip
    sudo pip install mozconfigwrapper

Then open your ~/.bashrc file and add the line:

    # may be in a different location on your system
    # use 'which mozconfigwrapper.sh' to find it
    source /usr/local/bin/mozconfigwrapper.sh

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

By default mozconfigs are stored in the ~/.mozconfigs directory, but you can override this by setting the 
$BUILDWITH_HOME environment variable.
e.g, add:

    export BUILDWITH_HOME=~/my/custom/mozconfig/path 

to your ~/.bashrc file.

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
