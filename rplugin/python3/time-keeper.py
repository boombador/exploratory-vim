import datetime
import os
import pynvim

def get_now():
    # FIXME: timezones and all that
    return datetime.datetime.now()


@pynvim.plugin
class Tracker(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.initialized = False

    def _initialize(self):
        if not self.initialized:
            # computationally expensive startup logic goes here
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

    @pynvim.command('TrackerEvent', nargs='1', range='')
    def command_event(self, args, range):
        self._initialize()
        message = args[0]
        log_line = '{} : {}\n'.format(datetime.datetime.now(), message)
        with open(os.path.expanduser('{}/events.txt'.format(self.root)), 'a') as f:
            f.write(log_line)
        self.nvim.out_write(log_line)

    @pynvim.command('TrackerToggle', nargs='*', range='')
    def command_toggle(self, args, range):
        self._initialize()
        message = str.join(' ', args)
        now = datetime.datetime.now()
        action = 'stopped' if self.working else 'started'
        log_line = '{} at {} - {}\n'.format(action, now, message)
        with open(os.path.expanduser('{}/toggles.txt'.format(self.root)), 'a') as f:
            f.write(log_line)
        self.nvim.out_write(log_line)
        self.working = not self.working

    @pynvim.command('TrackerTodo', nargs='1', range='')
    def command_todo(self, args, range):
        self._setup()
        message = args[0]
        log_line = '[ ] {} ({})\n'.format(message, datetime.datetime.now())
        with open(os.path.expanduser('{}/todo.txt'.format(self.root)), 'a') as f:
            f.write(log_line)
        self.nvim.out_write(log_line)
