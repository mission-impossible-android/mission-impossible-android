#compdef mia

# Zsh completion for MIA.
#
# Copy this file into the site-functions folder as `_mia`:
#   `cp mia_completion.zsh /usr/share/zsh/site-functions/_mia`
# Or you can use a symbolic link:
#   `ln -s ~/mission-impossible-android/tools/mia_completion.zsh /usr/share/zsh/site-functions/_mia`
#

# Determine the path to the MIA command.
MIA=$(command -v mia)
if [ ! -x "$MIA" ]
then
    return 1
fi

# Try to describe available sub-commands, if any.
_mia_sub_commands() {
    local -a _available_sub_commands

    # Available sub-commands.
    IFS=$'\n'
    _available_sub_commands=($($MIA --commands $1 | sed -e "/^Available sub-commands:$/d" -e :a -e 's/^ \+\([a-z-]\+\) \+/\1:/g' -e 's/ \+/ /g' -e :p | xargs -n1 -d "\n"))
    unset IFS

    _describe -t commands "$1 sub-commands" _available_sub_commands
}

# Try to describe available command options, if any.
_mia_command_options() {
    local -a _available_command_options

    # Get available sub-commands.
    IFS=$'\n'
    _available_command_options=($($MIA --options definition | sed -e "/^Command options:$/d" -e :a -e 's/^ \+\([^ ]\+\) \+\(.*\)/\1[\2]/g' -e 's/ \+/ /g' -e :p | xargs -n1 -d "\n"))
    unset IFS

    _describe -t commands "$1 command options" _available_command_options
}

# Describe the global mia commands.
_mia_command() {
    local -a _mia_cmds

    # Available commands.
    IFS=$'\n'
    _mia_cmds=($($MIA --commands | sed -e "/^Available commands:$/d" -e :a -e 's/^ \+\([a-z-]\+\) \+/\1:/g' -e 's/ \+/ /g' -e :p | xargs -n1 -d "\n"))
    unset IFS

    if (( CURRENT == 1 )); then
        _describe -t commands 'mia commands' _mia_cmds
    elif (( CURRENT == 2 )); then
        local curcontext="$curcontext"
        local cmd="${${_mia_cmds[(r)$words[1]:*]%%:*}}"
        echo "> $cmd"

        if (( $#cmd )); then
            # Try to describe available sub-commands, if any.
            _mia_sub_commands $cmd
        else
            _message "unknown mia command: $words[1]"
        fi
    elif (( CURRENT == 3 )); then
        _mia_sub_commands ${words[1]}
    else
        _message "unknown mia command: $words[1]"
    fi
}

# Main function.
_mia_autocomplete() {
    local -a _mia_args_list

    # Describe the global options.
    IFS=$'\n'
    _mia_args_list=($($MIA --options | sed -e "/^Global options:$/d" -e :a -e 's/^ \+\([a-z-]\+\) \+\(.*\)/\1[\2]/g' -e 's/ \+/ /g' -e :p | xargs -n1 -d "\n"))
    unset IFS

    # Describe the global commands list.
    _mia_args_list+=('*::mia commands:_mia_command')
    _arguments -s $_mia_args_list
}

case "$service" in
    mia)
        _mia_autocomplete "$@" && return 0
    ;;
esac
