# These configs are to be kept in zshrc file (such as, ~/.zshrc)
# to configure powerlevel9k theme


ZSH_THEME="powerlevel9k/powerlevel9k"


# The following options are powerlevel9k related
POWERLEVEL9K_DISABLE_RPROMPT=false
POWERLEVEL9K_PROMPT_ON_NEWLINE=true
POWERLEVEL9K_RPROMPT_ON_NEWLINE=true
POWERLEVEL9K_MULTILINE_LAST_PROMPT_PREFIX="▶ "
POWERLEVEL9K_MULTILINE_FIRST_PROMPT_PREFIX=""
POWERLEVEL9K_PROMPT_ADD_NEWLINE=true
# POWERLEVEL9K_PROMPT_ADD_NEWLINE_COUNT=1               # Ddefaults to 1
POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context dir vcs)
POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(status history time virtualenv)
POWERLEVEL9K_VIRTUALENV_BACKGROUND='023'
POWERLEVEL9K_VIRTUALENV_FOREGROUND='123'
# POWERLEVEL9K_COLOR_SCHEME='light'
POWERLEVEL9K_DIR_HOME_BACKGROUND='121'
POWERLEVEL9K_DIR_HOME_SUBFOLDER_BACKGROUND='121'
POWERLEVEL9K_DIR_ETC_BACKGROUND='121'
POWERLEVEL9K_DIR_DEFAULT_BACKGROUND='121'


# In plugins section, virtualenv needs to be added to show activated virtualenv in right prompt
plugins=(git virtualenv)