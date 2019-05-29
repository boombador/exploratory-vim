import pynvim

@pynvim.plugin
class TestPlugin(object):

    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function('TestFunction', sync=True)
    def testfunction(self, args):
        return 3

    @pynvim.command('TestCommand', nargs='*', range='')
    def testcommand(self, args, range):
        self.nvim.current.line = ('Command with args: {}, range: {}'
                                .format(args, range))
        self.nvim.out_write('Replaced current line with invocation summary\n')

    @pynvim.autocmd('BufEnter', pattern='*.py', eval='expand("<afile>")', sync=True)
    def on_bufenter(self, filename):
        self.nvim.out_write('TestPlugin is active while you\'ve entered file: ' + filename + '\n')
