import datetime
import os
import pynvim


@pynvim.plugin
class TimeKeeper(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.working = False

    @pynvim.command('ToggleWorking', nargs='*', range='')
    def command_toggle(self, args, range):
        # FIXME: timezones and all that
        now = datetime.datetime.now()
        action = 'stopped' if self.working else 'started'
        log_line = '{} at {}'.format(action, now)
        with open(os.path.expanduser('~/timekeeping.txt'), 'a') as f:
            f.write(log_line + '\n')
        self.working = not self.working


# overview: track work sessions. each work session has start and end datetime, optional start and end notes
# save each transition in a log file for later perusal, update statusline
# parsing logfile on startup can go later if more material is needed
