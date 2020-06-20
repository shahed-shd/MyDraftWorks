# This file contains common configurations for different shells, like bash, zsh.
# It can be included using 'source' command in rc files (like, .bashrc , .zshrc).
# 'source' command example: source "path/to/this/file"

# To add a path to PATH (bash, zsh supported)
pathadd() {
    if [ -d "$1" ] && [[ ":$PATH:" != *":$1:"* ]]; then
        PATH="${PATH:+"$PATH:"}$1"
    fi
}

