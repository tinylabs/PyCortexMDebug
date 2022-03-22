#
# Base chipset class
# Handle CPU and on-chip memory resources
#

from cmdebug.utils.GDBCommand import GDBCommand
import gdb

class Chipset (GDBCommand):
    """Configure/Query loaded chipset"""
    
    def __init__ (self, chip_id):
        # Decode chip ID
        self.decode (chip_id)

        # Install GDB command
        super().__init__ ('chipset')

    # Decode chip id into properties
    def decode (self, chip_id):

        # Save chip ID
        self.chip_id = chip_id.lower()

        # Dict for property storage
        self.prop = dict()
        
        # Decode args
        n = 0
        for f in self.decoder:
            if isinstance (f[1], dict):
                self.prop[f[0]] = f[1][self.chip_id[n]]
                n += 1
            else:
                end = min (len (self.chip_id), n + f[1])
                self.prop[f[0]] = self.chip_id[n:end].upper()
                n = end
            if n >= len (self.chip_id):
                break

    def chip_id (self):
        return self.chip_id

    def probe (self):
        gdb.write ('probe() not implemented.\n')
    
    def __str__ (self):
        if self.prop:
            # Get length of longest key
            pad = max (len (x) for x in self.prop.keys())
            _ = '{} : {}\n'.format ('chipset'.ljust (pad), self.chip_id)
            for k,v in self.prop.items():
                _ += '{} : {}\n'.format (k.ljust(pad), v)
            return _

    def invoke (self, args, from_tty):
        if len (args):
            # Compare with current chip id

            # Decode new chip id
            self.decode (args)

            # Update drivers if necessary

        # Just dump current chipset info
        else:
            gdb.write (str(self))
