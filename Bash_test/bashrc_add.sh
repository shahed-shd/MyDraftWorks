# This file can be included in .bashrc file

# Custom prompt for bash
export PS1="\n\[\e[00;32m\]\u\[\e[0m\]\[\e[00;37m\]@\[\e[0m\]\[\e[0;33m\]\h\[\e[0m\]\[\e[00;37m\] \t \[\e[0m\]\[\e[00;36m\]\w\[\e[0m\]\[\e[01;37m\] \[\e[0m\]\n$ "

# Used to add a path to PATH
pathadd() {
    if [ -d "$1" ] && [[ ":$PATH:" != *":$1:"* ]]; then
        PATH="${PATH:+"$PATH:"}$1"
    fi
}

