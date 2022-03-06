#!/usr/bin/env python3
#
# Script to interact with external SPI flash
# on STM32 microcontrollers
#

import gdb
import re

class SPIFlashCmd (gdb.Command):
    """Access external SPI flash"""

    def __init__ (self):
        super (SPIFlashCmd, self).__init__ ("spiflash", gdb.COMMAND_USER )

        # Persistent instances set via config
        self.cs = None
        self.spi = None
        self.init = False
        
    # Read/Write SPI regs
    def SPIFlashReg (self, cmd, addr, cnt):

        # Assert /cs
        self.cs.clr()

        # Send command
        resp = self.spi.transfer ([cmd,
                                   (addr >> 16) & 0xff,
                                   (addr >> 8) & 0xff,
                                   addr & 0xff], cnt)

        # Deassert /cs
        self.cs.set ()
        return resp
    
    # Get JEDEC ID
    def SPIFlashDeviceID (self):
        return self.SPIFlashReg (0x90, 0, 2)

    def Read (self, addr, cnt):

        # Assert /cs
        self.cs.clr()

        # Send FAST_READ command
        resp = self.spi.transfer ([0x0B,
                                   (addr >> 16) & 0xff,
                                   (addr >> 8) & 0xff,
                                   addr & 0xff,
                                   0,0,0,0,0,0,0,0], cnt)

        # Deassert /cs
        self.cs.set ()
        return resp
    
    def Probe (self):

        print ("Probing spiflash...")
        
        # Enable SPI
        self.spi.enable ()

        # Config GPIOs

        # Print flash ID
        flash_id = self.SPIFlashDeviceID()
        print ("Found spiflash: {:02X}{:02X}".format (flash_id[0], flash_id[1]))

        # Set initialized
        self.init = True

        # Leave enabled... TODO: have a cmd for restore
        
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
    SPIFlashCmd ()
