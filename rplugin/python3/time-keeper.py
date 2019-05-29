import datetime
import os
import pynvim

def get_now():
    # FIXME: timezones and all that
    return datetime.datetime.now()


@pynvim.plugin
class TimeKeeper(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.working = False

    @pynvim.command('TrackWorkToggle', nargs='*', range='')
    def command_work_toggle(self, args, range):
        now = get_now()
        action = 'stopped' if self.working else 'started'
        log_line = '{} at {}\n'.format(action, now)
        with open(os.path.expanduser('~/timekeeping-worktoggle.txt'), 'a') as f:
            f.write(log_line)
        self.nvim.out_write(log_line)
        self.working = not self.working


    # setting nargs to 1 combines multiple words into one string
    @pynvim.command('TrackWorkEvent', nargs='1', range='')
    def command_work_event(self, args, range):
        message = args[0]
        log_line = '{} : {}\n'.format(get_now(), message)
        with open(os.path.expanduser('~/timekeeping-workevents.txt'), 'a') as f:
            f.write(log_line)
        self.nvim.out_write(log_line)


    # setting nargs to 1 combines multiple words into one string
    @pynvim.command('TrackTodo', nargs='1', range='')
    def command_todo(self, args, range):
        message = args[0]
        log_line = '[ ] {} ({})\n'.format(message, get_now())
        with open(os.path.expanduser('~/todo.txt'), 'a') as f:
            f.write(log_line)
        self.nvim.out_write(log_line)

# overview: track work sessions. each work session has start and end datetime, optional start and end notes
# save each transition in a log file for later perusal, update statusline
# parsing logfile on startup can go later if more material is needed
