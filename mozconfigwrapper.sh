# -*- mode: shell-script -*-

function mozconfigwrapper_buildwith_home {
    typeset buildwith_home=$BUILDWITH_HOME
    if [ "$buildwith_home" = "" ]
    then
        buildwith_home="$HOME/.mozconfigs"
        export BUILDWITH_HOME=$buildwith_home
    fi
}

function buildwith {
    mozconfigwrapper_buildwith_home
    typeset name="$1"
    
    if [ ! -f "$BUILDWITH_HOME/$name" ]
    then 
        echo "Error: $BUILDWITH_HOME/$name does not exist"
        return 1
    fi

    mozconfig="$BUILDWITH_HOME/$name"
    echo "$name" > "$BUILDWITH_HOME/.active"
    export MOZCONFIG=$mozconfig

    if [ ! "$2" = "silent" ]
    then
        echo "$MOZCONFIG"
    fi
    return 0
}

function mkmozconfig {
    mozconfigwrapper_buildwith_home
    typeset name="$1"

    mozconfig="$BUILDWITH_HOME/$name"
    python -c "from mozconfigwrapper import mkmozconfig; mkmozconfig('$name')"
    echo "Created: $mozconfig"
    buildwith $name "silent"
}

function rmmozconfig {
    mozconfigwrapper_buildwith_home
    typeset name="$1"

    if [ ! -f "$BUILDWITH_HOME/$name" ]
    then
        echo "Error: $BUILDWITH_HOME/$name does not exist"
        return 1
    fi

    mozconfig="$BUILDWITH_HOME/$name"
    rm $mozconfig
    echo "Removed: $mozconfig"
}

# Set up tab completion
# Adapted from virtualenvwrapper (written by Doug Hellman and Arthur Koziel)
function mozconfigwrapper_setup_tab_completion {
    if [ -n "$BASH" ] ; then
        _mozconfigs() {
            local cur="${COMP_WORDS[COMP_CWORD]}"
            COMPREPLY=( $(compgen -W "`mozconfigwrapper_list_mozconfigs`" -- ${cur}) )
        }
        complete -o default -o nospace -F _mozconfigs buildwith rmmozconfig
    elif [ -n "$ZSH_VERSION" ] ; then
        _mozconfigs() {
            reply=( $(mozconfigwrapper_list_mozconfigs) )
        }
        compctl -K _mozconfigs buildwith rmmozconfig
    fi
}

# List the available mozconfigs.
function mozconfigwrapper_list_mozconfigs {
    # NOTE: DO NOT use ls here because colorized versions spew control characters
    #       into the output list.
    # echo seems a little faster than find, even with -depth 3.
    mozconfigwrapper_buildwith_home || return 1
    (echo "$BUILDWITH_HOME"/*) 2>/dev/null \
		| command \fmt -w 1 \
		| command \sed -e "s!^$BUILDWITH_HOME\/!!" \
		| (unset GREP_OPTIONS; command \egrep -v '^\*$') 2>/dev/null
}

mozconfigwrapper_buildwith_home
mozconfigwrapper_setup_tab_completion

if [ -f "$BUILDWITH_HOME/.active" ]
then
    active=`cat $BUILDWITH_HOME/.active`
    if [ ! $active = "" ]
    then
        buildwith "$active" "silent"
    fi
fi
