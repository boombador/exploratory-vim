import ast
import pynvim

def analyze(root_node):
    """
    toplevel statements -> class def -> body of class ->
    """
    return 'There are {} AST nodes under the root of this document'.format(
            len(root_node.body))


@pynvim.plugin
class Graphify(object):

    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command('Graphify', nargs='*', range='')
    def command_graphify(self, args, range):
        buffer = self.nvim.current.buffer
        buffer_contents = str.join('\n', buffer[:])
        root_node = ast.parse(buffer_contents)
        result_message = analyze(root_node)
        self.nvim.out_write(result_message)
