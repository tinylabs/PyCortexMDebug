#!/usr/bin/env python3
#
# Script to interact with external SPI flash
# on STM32 microcontrollers
#

import gdb
import re
import svd_hw

class SPI:

    # Takes periph str and comma separated list of pins
    def __init__ (self, periph, pins):

        # Save peripheral
        self.periph = periph

        # Get base device
        self.base = svd_hw().find (self.periph)
        
        # Extract port
        self.idx = periph[-1]

        # Create GPIOs
        self.gpios = [GPIO (x) for x in pins.split(',')]
        
        # Get global enable register
        self.en = svd_hw().find ('spi{}en'.format (self.idx))
        
        # Get data reg
        dr = self.base.find ('dr')
        # Get data field (same name)
        self.dr = dr.find ('dr')
        
    def enable (self):
        self.en.set (1)

    def disable (self):
        self.en.set (0)

    def div (self, n):
        pass

    def transfer (self, dout=[], din=0):
        # Send data out
        for do in dout:
            self.dr.set (do)
        # Flush receive buffer
        self.dr.get ()
        resp = []
        # Write dummy bytes to get response
        for n in range (din):
            self.dr.set (0)
            resp.append (self.dr.get ())
        return resp
    
class SPICmd (gdb.Command):
    """Access SPI peripheral"""

    def __init__ (self):
        super (SPIFlashCmd, self).__init__ ("spi", gdb.COMMAND_USER )
                
    def usage (self, cmd=''):

        if cmd == 'config':
            gdb.write ('Usage: spiflash config cs=PBn spi=PBx,PBy,PBz\n')
        elif cmd == 'read':
            gdb.write ('Usage: spiflash read <addr> <len> [filename]\n')
        else:
            pass
        
    def invoke (self, args, from_tty):

        # Check usage
        if args == None:
            self.usage ()
            return
        
        # Parse args
        args = args.split (' ')
        cmd = args.pop (0).lower()
        
        # Handle config
        if cmd == 'config':
            if len (args) != 2:
                self.usage (cmd)
                return
            
            # Parse args
            for arg in args:
                (k, v) = arg.split('=')
                if k.lower() == 'cs':
                    self.cs = GPIO (v.lower())
                elif k.lower().startswith ('spi'):
                    self.spi = SPI (k.lower(), v.lower())
                else:
                    self.usage (cmd)
                    return
                
            # Probe for flash
            self.Probe ()

        elif cmd == 'read':
            if len (args) != 2 and len (args) != 3:
                self.usage (cmd)
                return

            # Get address
            addr = int (args[0], 0)

            # Get length
            length = int (args[1], 0)

            # Read memory
            mem = self.Read (addr, length)
            cnt = 0
            for m in mem:
                if cnt and (cnt % 16) == 0:
                    gdb.write ("\n")
                gdb.write ("{:02X} ".format (m))
                cnt += 1
            gdb.write ("\n")
            
        elif cmd == 'dump':
            pass

        elif cmd == 'restore':
            pass
        

# Register command when file is sourced
if __name__ == '__main__':
    SPICmd ()
