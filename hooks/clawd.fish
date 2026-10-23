# Clawd reacts when a long command finishes: ok or fail.
# Install: ln -s (realpath hooks/clawd.fish) ~/.config/fish/conf.d/clawd.fish
status is-interactive; or exit

function __clawd_postexec --on-event fish_postexec
    set -l code $status
    set -q CLAWD_CMD_MS; or set -l CLAWD_CMD_MS 5000
    test "$CMD_DURATION" -ge $CLAWD_CMD_MS; or return
    test $code -eq 130; and return   # interrupted with Ctrl-C
    set -l run (set -q XDG_RUNTIME_DIR; and echo $XDG_RUNTIME_DIR; or echo /tmp)/clawd
    test -d $run; or return
    if test $code -eq 0
        touch $run/ev-ok
    else
        touch $run/ev-fail
    end
end
