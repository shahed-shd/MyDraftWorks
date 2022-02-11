opt_will_force=false
opt_will_prepend=false
opt_is_verbose=false
opt_dir_path=''


function __usage() {
    echo "Usage: $( basename $0 ) [-f|--force] [-a|--append|-p|--prepend] DIR_PATH"

	echo $'\nAdd DIR_PATH to the PATH environment variable.'

	echo "
options     long options                 Meaning
 -f         --force                 Force to append or prepend.
                                    If DIR_PATH exists in PATH, then remove it and append or prepend.
 -a         --append
 -p         --prepend               Specify to append or prepend. If not specified, 'append' is selected.
 -v         --verbose               Explain what is being done.
 -h         --help                  Display this help and exit.


Exit status:
    0       Program ran without any error.
    1       Unrecognized or too many options/arguments encountered in command.
    2       DIR_PATH not a directory path.
    3       DIR_PATH already in PATH and not forcing.
"
}


function __log() {
    # 1st arg: e, w, i, d for error, warning, info, debug
    # 2nd arg: the message to log

    if "$opt_is_verbose" ; then
        echo $2
    fi
}


function __parse_opts() {
    while [[ $# > 0 ]] ; do
        case "$1" in
            -f | --force )
                opt_will_force=true
                shift
                ;;
            -a | --append )
                opt_will_prepend=false
                shift
                ;;
            -p | --prepend )
                opt_will_prepend=true
                shift
                ;;
            -v | --verbose )
                opt_is_verbose=true
                shift
                ;;
            -h | --help )
                __usage
                break
                ;;
            -- )
                shift
                break
                ;;
            * )
                if [[ $# != 1 ]] ; then
                    __log 'e' "$( basename $0 ): Argument error";
                    exit 1
                else
                    opt_dir_path="$1"
                    shift
                fi
                ;; 
        esac
    done
}


function __go() {
    local PATH_VAL="$PATH"

    if [ -d "$opt_dir_path" ] ; then
        if "$opt_will_force" ; then
            # Remove if found in middle (not at any end).
            PATH_VAL="${PATH_VAL//:$opt_dir_path:/:}"
            
            if "$opt_will_prepend" ; then
                # Remove from end
                PATH_VAL="${PATH_VAL%:$opt_dir_path}"
            else
                # Remove from beginning
                PATH_VAL="${PATH_VAL#$opt_dir_path:}"
            fi
        fi
    
        # If not in PATH_VAL
        if [[ ":$PATH_VAL:" != *":$opt_dir_path:"* ]] ; then
            if "$opt_will_prepend" ; then
                # Prepend
                PATH_VAL="$opt_dir_path:${PATH_VAL:+"$PATH_VAL"}"
            else
                # Append
                PATH_VAL="${PATH_VAL:+"$PATH_VAL"}:$opt_dir_path"
            fi
        else
            __log 'i' "$opt_dir_path is already in PATH and not forcing"
            return 3
        fi
    else
        __log 'e' "$opt_dir_path is not a directory"
        return 2
    fi
    
    echo "$PATH_VAL"
}


__parse_opts "$@"
__go

