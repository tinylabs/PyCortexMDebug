#!/usr/bin/env python3
#
# Script to interact with external SPI flash
# on STM32 microcontrollers
#

import gdb
import re

class svd_hw:

    # HW types
    TYPE_ROOT       = 0
    TYPE_PERIPHERAL = 1
    TYPE_REGISTER   = 2
    TYPE_FIELD      = 3
    
    def __init__ (self, node=[]):

        # Check if svd module is loaded and svd is parsed
        resp = gdb.execute ('svd', True, True)
        if resp.startswith ('Undefined'):
            raise ImportError ("Please source: PyCortexMDebug/scripts/gdb.py first.")
        elif resp.startswith ('Usage:'):
            raise ImportError ("Must load SVD first with svd_load.")
        if not node:
            self.root = []
            self.hwtype = self.TYPE_ROOT
        else:
            self.root = node

            # Get type in hierarchy
            res = gdb.execute ('svd /n' + str(' '.join (self.root)), True, True)
            if res.startswith ('Registers'):
                self.hwtype = self.TYPE_PERIPHERAL
            elif res.startswith ('Fields'):
                self.hwtype = self.TYPE_REGISTER
            elif res.startswith ('Cluster'):
                self.hwtype = self.TYPE_FIELD
            
    def get (self):
        # Cannot get value of peripheral or root
        if (self.hwtype == self.TYPE_ROOT) or (self.hwtype == self.TYPE_PERIPHERAL):
            return
        # Search up one layer
        match = self.root[-1]
        lines = gdb.execute ('svd' + ' '.join(self.root[:-1]), True, True).splitlines()
        for line in lines:
            res = re.search (r"\s+([a-zA-z0-9]+):\s+([0-9]+).+", line)
            if res and res.group (1) == match:
                return int (res.group (2))

    def set (self, val):
        if self.hwtype == self.TYPE_FIELD:
            #print ('svd ' + str(self) + ' ' + str(val))
            gdb.execute ('svd ' + str(self) + ' ' + str(val), True, True)

    def noaccess (self, sub=''):
        if self.root:
            return gdb.execute ('svd /n' + str(self) + ' ' + sub, True, True)
        else:
            return gdb.execute ('svd' + str(self) + ' ' + sub, True, True)
        
    def __str__ (self):
        return ' '.join (self.root)

    def __getitem__ (self, n):
        lines = self.noaccess().splitlines()
        if n+1 >= len (lines):
            raise IndexError
        res = re.search (r"\s+([a-zA-z0-9]+):.+", lines[n+1])
        return res.group (1)
    
    def __iter__ (self):
        self.n = 0
        return self

    def __next__ (self):
        try:
            ret = self[self.n]
        except IndexError:
            raise StopIteration
        self.n += 1
        return ret
    
    def find (self, field):
        # Check sub nodes for match
        for node in self:
            #print ("{} <=> {}".format (node.lower(), field))
            if node.lower() == field:
                return svd_hw ([str(self)] + [str(node)])
        # Recurse down one level
        for node in self:
            child = svd_hw ([str(self)] + [str(node)])
            res = child.find (field)
            if res:
                return res
        return None
