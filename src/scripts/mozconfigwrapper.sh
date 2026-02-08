# -*- mode: shell-script -*-

function mozconfigwrapper_buildwith_home {
    typeset buildwith_home=$BUILDWITH_HOME
    if [ "$buildwith_home" = "" ]
    then
        buildwith_home="$HOME/.mozconfigs"
        export BUILDWITH_HOME=$buildwith_home
    fi
}

# Detect if current directory is inside a gecko repository
function mozconfigwrapper_is_in_gecko {
    # Search up the directory tree for gecko markers
    typeset current="$PWD"
    while [ "$current" != "/" ]; do
        if [ -f "$current/mach" ] || [ -f "$current/moz.configure" ]; then
            return 0
        fi
        current=$(dirname "$current")
    done

    return 1
}

# Generate prompt prefix if BUILDWITH_SHOW_PROMPT is enabled
function mozconfigwrapper_prompt {
    # Only show prompt if explicitly enabled
    if [ -z "$BUILDWITH_SHOW_PROMPT" ]; then
        return
    fi

    # Only show if we have an active mozconfig and we're in a gecko repo
    if [ -n "$MOZCONFIG" ] && mozconfigwrapper_is_in_gecko; then
        typeset mozconfig_name=$(basename "$MOZCONFIG")
        typeset format="${BUILDWITH_PROMPT_FORMAT:-(%s) }"
        # Replace %s with mozconfig name
        printf "$format" "$mozconfig_name"
    fi
}

function buildwith {
    mozconfigwrapper_buildwith_home
    typeset name="$1"

    if [ -z "$name" ]
    then
        echo "Usage: buildwith <name>"
        return 1
    fi

    if [ ! -f "$BUILDWITH_HOME/$name" ]
    then
        echo "Error: $BUILDWITH_HOME/$name does not exist"
        return 1
    fi

    typeset export_command=$BUILDWITH_COMMAND
    if [ "$export_command" = "" ]
    then
        export_command="export MOZCONFIG=#1"
    fi

    if [ ! "$2" = "silent" ]
    then
        export_command="$export_command && echo #1"
    fi

    mozconfig="$BUILDWITH_HOME/$name"
    echo "$name" >| "$BUILDWITH_HOME/.active"
    eval ${export_command//\#1/$mozconfig}
    return 0
}

function mkmozconfig {
    mozconfigwrapper_buildwith_home
    typeset name="$1"

    if [ -z "$name" ]
    then
        echo "Usage: mkmozconfig <name>"
        return 1
    fi

    mozconfig="$BUILDWITH_HOME/$name"
    python3 -c "from mozconfigwrapper import mkmozconfig; mkmozconfig('$name')"
    echo "Created: $mozconfig"
    buildwith $name "silent"
}

function rmmozconfig {
    mozconfigwrapper_buildwith_home
    typeset name="$1"

    if [ -z "$name" ]
    then
        echo "Usage: rmmozconfig <name>"
        return 1
    fi

    if [ ! -f "$BUILDWITH_HOME/$name" ]
    then
        echo "Error: $BUILDWITH_HOME/$name does not exist"
        return 1
    fi

    mozconfig="$BUILDWITH_HOME/$name"

    # If we're removing the active mozconfig, unset it
    if [ "$MOZCONFIG" = "$mozconfig" ]
    then
        unset MOZCONFIG
        rm -f "$BUILDWITH_HOME/.active"
    fi

    rm "$mozconfig"
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

# Store original PS1 for zsh
_MOZCONFIGWRAPPER_ORIGINAL_PS1=""

# Set up prompt integration if BUILDWITH_SHOW_PROMPT is enabled
function mozconfigwrapper_setup_prompt {
    if [ -z "$BUILDWITH_SHOW_PROMPT" ]; then
        return
    fi

    if [ -n "$BASH" ]; then
        # For bash, we modify PS1 to include our prompt function
        # Only modify if not already present
        if [[ "$PS1" != *'$(mozconfigwrapper_prompt)'* ]]; then
            export PS1="\$(mozconfigwrapper_prompt)$PS1"
        fi
    elif [ -n "$ZSH_VERSION" ]; then
        # For zsh, save the original PS1 and add to precmd_functions array
        if [ -z "$_MOZCONFIGWRAPPER_ORIGINAL_PS1" ]; then
            _MOZCONFIGWRAPPER_ORIGINAL_PS1="$PS1"
        fi
        if [[ ! " ${precmd_functions[@]} " =~ " mozconfigwrapper_precmd " ]]; then
            precmd_functions+=(mozconfigwrapper_precmd)
        fi
    fi
}

# Zsh precmd hook to update PS1
function mozconfigwrapper_precmd {
    # Reconstruct PS1 from the original, preserving prompt expansions
    typeset prefix=$(mozconfigwrapper_prompt)
    if [ -n "$prefix" ]; then
        PS1="${prefix}${_MOZCONFIGWRAPPER_ORIGINAL_PS1}"
    else
        PS1="$_MOZCONFIGWRAPPER_ORIGINAL_PS1"
    fi
}

mozconfigwrapper_buildwith_home
mozconfigwrapper_setup_tab_completion
mozconfigwrapper_setup_prompt

if [ -f "$BUILDWITH_HOME/.active" ]
then
    active=`cat "$BUILDWITH_HOME/.active"`
    if [ ! $active = "" ]
    then
        buildwith "$active" "silent"
    fi
fi
