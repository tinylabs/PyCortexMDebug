#
# GDB command base class
#
import gdb

class GDBCommand (gdb.Command):
    """GDB command helper base class"""
    
    def __init__ (self, name, arg_list=None):
        self.name = name
        self.arg_list = arg_list
        # Install command
        gdb.Command.__init__ (self, name, gdb.COMMAND_USER)
        
    def complete (self, text, word):
        '''GDB command completion helper'''
        args = gdb.string_to_argv (text)

        # TODO: implement completion based on arglist
        return gdb.COMPLETE_NONE
    
    def invoke (self, args, from_tty):
        gdb.write ('{} invoke() not implemented.\n'.format (self.name))
        
