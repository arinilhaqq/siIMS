# This file must be used with "source bin/activate.csh" *from csh*.
# You cannot run it directly.
# Created by Davide Di Blasi <davidedb@gmail.com>.
# Ported to Python 3.3 venv by Andrew Svetlov <andrew.svetlov@gmail.com>

<<<<<<< HEAD
alias deactivate 'test $?_OLD_VIRTUAL_PATH != 0 && setenv PATH "$_OLD_VIRTUAL_PATH" && unset _OLD_VIRTUAL_PATH; rehash; test $?_OLD_VIRTUAL_PROMPT != 0 && set prompt="$_OLD_VIRTUAL_PROMPT" && unset _OLD_VIRTUAL_PROMPT; unsetenv VIRTUAL_ENV; unsetenv VIRTUAL_ENV_PROMPT; test "\!:*" != "nondestructive" && unalias deactivate'
=======
alias deactivate 'test $?_OLD_VIRTUAL_PATH != 0 && setenv PATH "$_OLD_VIRTUAL_PATH" && unset _OLD_VIRTUAL_PATH; rehash; test $?_OLD_VIRTUAL_PROMPT != 0 && set prompt="$_OLD_VIRTUAL_PROMPT" && unset _OLD_VIRTUAL_PROMPT; unsetenv VIRTUAL_ENV; test "\!:*" != "nondestructive" && unalias deactivate'
>>>>>>> 2ab9dc214f7f944aa2d8ff95f8c3a5da31f050d3

# Unset irrelevant variables.
deactivate nondestructive

<<<<<<< HEAD
setenv VIRTUAL_ENV "/Users/arinilhaq/Documents/Semester 6/Propensi/siIMS/d06-siims/env"
=======
setenv VIRTUAL_ENV "/Users/pavitamaheswariiswandaruputri/Documents/propensi/d06-siims/env"
>>>>>>> 2ab9dc214f7f944aa2d8ff95f8c3a5da31f050d3

set _OLD_VIRTUAL_PATH="$PATH"
setenv PATH "$VIRTUAL_ENV/bin:$PATH"


set _OLD_VIRTUAL_PROMPT="$prompt"

if (! "$?VIRTUAL_ENV_DISABLE_PROMPT") then
    set prompt = "(env) $prompt"
<<<<<<< HEAD
    setenv VIRTUAL_ENV_PROMPT "(env) "
=======
>>>>>>> 2ab9dc214f7f944aa2d8ff95f8c3a5da31f050d3
endif

alias pydoc python -m pydoc

rehash
