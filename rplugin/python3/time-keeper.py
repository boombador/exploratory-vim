import datetime
import os
import pynvim

def get_now():
    # FIXME: timezones and all that
    return datetime.datetime.now()


@pynvim.plugin
class Tracker(object):

    def __init__(self, nvim):
        """
        should not do any significant processing on startup, defer to a helper
        _setup function which runs at most once
        """
        self.nvim = nvim
        self.initialized = False

    def _setup(self):
        if not self.initialized:
            # computationally expensive startup logic goes here, should be
            # called by functions that depend on it having been run
            self.working = False
            self.root = '~/tracking'
            with open(os.path.expanduser('{}/toggles.txt'.format(self.root)), 'r') as f:
                lines = f.readlines()
                if len(lines) > 0:
                    last_line = lines[-1]
                    first_word = str.split(last_line, ' ')[0]
                    if first_word == 'started':
                        self.working = True
            self.initialized = True

    @pynvim.command('TrackerToggle', nargs='*', range='')
    def command_toggle(self, args, range):
        self._setup()
        message = str.join(' ', args)
        if message:
            message = ' - {}'.format(message)
        now = datetime.datetime.now()
        action = 'stopped' if self.working else 'started'
        log_line = '{} at {}{}\n'.format(action, now, message)
        with open(os.path.expanduser('{}/toggles.txt'.format(self.root)), 'a') as f:
            f.write(log_line)
        self.nvim.out_write(log_line)
        self.working = not self.working

    # setting nargs to 1 combines multiple words into one string
    @pynvim.command('TrackerEvent', nargs='1', range='')
    def command_event(self, args, range):
        self._setup()
        message = args[0]
        log_line = '{} : {}\n'.format(datetime.datetime.now(), message)
        with open(os.path.expanduser('{}/events.txt'.format(self.root)), 'a') as f:
            f.write(log_line)
        self.nvim.out_write(log_line)

    # setting nargs to 1 combines multiple words into one string
    @pynvim.command('TrackerTodo', nargs='1', range='')
    def command_todo(self, args, range):
        self._setup()
        message = args[0]
        log_line = '[ ] {} ({})\n'.format(message, datetime.datetime.now())
        with open(os.path.expanduser('{}/todo.txt'.format(self.root)), 'a') as f:
            f.write(log_line)
        self.nvim.out_write(log_line)
