#!/usr/bin/env bash
#
# Bash completion for MIA.
#
# Add the script to your .bashrc file:
#   `source mia.bash_complition.sh`
# Or you can copy the file into the bash completion:
#   `cp mia.bash_complition.sh /etc/bash_completion.d/`
#
# TODO: Implement properly in python.
#

_mia() {
    _init_completion || return

    # The MIA executable.
    MIA="${COMP_WORDS[0]}"

    # The path to the `ls` executable.
    LS=`which ls`

    # Array variable storing the possible completions.
    COMPREPLY=()

    # Available commands and global options.
    local COMMANDS=`${MIA} --commands  2>&1 | sed -e "/Available commands:/d" | awk -F '  ' '{print $3}'`
    local OPTIONS=`${MIA} --options  2>&1 | sed -e "/Global options:/d" -e "s/,//g" | awk -F '  ' '{print $3}'`

    # Variable containing the current and previous words.
    local cur="${COMP_WORDS[$COMP_CWORD]}"
    local prev="${COMP_WORDS[$COMP_CWORD-1]}"

    # @TODO: Find a better way to determine the command.
    local command=''
    for index in ${!COMP_WORDS[*]}; do
        # Ignore programm name.
        if [[ ${index} -eq 0 ]]; then
            continue
        fi

        for c in ${COMMANDS[@]}; do
            if [[ "$c" == "${COMP_WORDS[$index]}" ]]; then
                command="${COMP_WORDS[${index}]}"
            fi
        done
    done

    # Deal with the completion of the global options.
    if [[ "$command" == '' ]]; then
        COMPREPLY=( $(compgen -W "$OPTIONS" -- "$cur" ) )
    fi

    # Deal with the completion of the first command.
    if [[ $COMP_CWORD -eq 1 || ("$command" == '' && "$prev" == -*) ]]; then
        # Merge to commands to the list of options, if any.
        COMPREPLY=( ${COMPREPLY[*]} $(compgen -W "$COMMANDS" -- "$cur" ) )
        return 0
    fi

    case "$command" in
        build | clean | install | definition)
            if [[ "$prev" == "$command" ]]; then
                # Display subcommands before all other arguments and options.
                subc=`${MIA} --commands ${command}  2>&1 | sed -e "/Available sub-commands:/d" | awk -F '  ' '{print $3}'`
            fi

            opts=`${MIA} --options ${command}  2>&1 | sed -e "/Command options:/d" -e "s/,//g" -e "s/=<\w\+>//g" | awk -F '  ' '{print $3}'`

            defs=`${LS} definitions`
            if [[ "${prev}" =~ "${defs}" ]]; then
                defs=''
            fi

            COMPREPLY=($(compgen -W "${subc} ${opts} ${defs}" -- ${cur}))
        ;;
        definition)
            if [[ "$prev" == "$command" ]]; then
                # Display subcommands before all other arguments and options.
                subc=`${MIA} --commands ${command}  2>&1 | sed -e "/Available sub-commands:/d" | awk -F '  ' '{print $3}'`
            else
                opts=`${MIA} --options ${command}  2>&1 | sed -e "/Command options:/d" -e "s/,//g" -e "s/=<\w\+>//g" | awk -F '  ' '{print $3}'`

                defs=`${LS} definitions`
                if [[ "${prev}" =~ "${defs}" ]]; then
                    defs=''
                fi
            fi

            COMPREPLY=($(compgen -W "${subc} ${opts} ${defs}" -- ${cur}))
        ;;
        --commands | --options)
            # The display the list of available commands.
            COMPREPLY=( $(compgen -W "$COMMANDS" -- "$cur") )
        ;;
    esac

    return 0
} &&
complete -F _mia mia
