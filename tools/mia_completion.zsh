#compdef mia

# Zsh completion for MIA.
#
# Copy this file into the site-functions folder as `_mia`:
#   `cp mia_completion.zsh /usr/share/zsh/site-functions/_mia`
# Or you can use a symbolic link:
#   `ln -s ~/mission-impossible-android/tools/mia_completion.zsh /usr/share/zsh/site-functions/_mia`
#

# Sub-commands for `mia definition`
_mia_cmd__definition() {
    local -a _definition_cmds
    _definition_cmds=(
        'create:Creates a definition.'
        'configure:Configures a definition.'
        'lock:Creates a lock file for the applications.'
        'dl-apps:Downloads the applications using data from the lock file.'
        'dl-os:Show information on how to download and verify an OS zip.'
        'extract-update-binary:Extract the update-binary from the CyanogenMod zip file.'
        'update-from-template:Update definition from template'
    )
}

# Commands for `mia`
_mia_command() {
    local -a _mia_cmds
    _mia_cmds=(
        'build:Build an update.zip file.'
        'clean:Cleanup the current workspace.'
        'definition:Create and configure a definition for a new update.zip file based on existing templates.'
        'install:Install the OS and the built update.zip file onto the device.'
    )

    if (( CURRENT == 1 )); then
        _describe -t commands 'mia commands' _mia_cmds
    else
        local curcontext="$curcontext"
        local cmd="${${_mia_cmds[(r)$words[1]:*]%%:*}}"
        if (( $#cmd )); then
            if (( $+functions[_mia_cmd__$cmd] )); then
                _mia_cmd__$cmd
            else
                _message "no more options"
            fi
        else
            _message "unknown mia command: $words[1]"
        fi
    fi
}

# Main arguments list.
_mia_arglist=(
    '--commands[Displays a list of available commands or sub-commands.]'
    '--options[Displays a list of global or command specific options.]'
    '--quiet[Restrict output to warnings and errors.]'
    '--verbose[Spew out even more information than normal.]'
    '--help[Show this screen.]'
    '--version[Show version.]'
    '*::mia commands:_mia_command'
)

# Main function.
_mia_autocomplete() {
    _arguments -s $_mia_arglist
}

case "$service" in
    mia)
        _mia_autocomplete "$@" && return 0
    ;;
esac
