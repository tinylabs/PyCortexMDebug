#
# Load the appropriate vendor file based on chipset string.
# To accomplish this we do a reverse search starting from
# most specific to most generic. We stop after the
# first successful match.
#
# ie: STM32F40x will override STM32.
# This allows proper inheritance to override specific
# chipset differences.
#
import os
import importlib

from cmdebug.periph import get_periphs

def VendorMod (periph, name=''):

    # Instantiate dict cache
    if not hasattr (VendorMod, 'mod'):
        VendorMod.mod = {}

    # Return cached object
    if periph in VendorMod.mod:
        return VendorMod.mod[periph]
    
    # Load best match vendor peripheral access module
    for n in range (len (name), 1, -1):
        path = os.path.join (os.path.dirname(__file__), name[0:n] + '.py')
        if os.path.exists (path):
            mod = importlib.import_module \
                ('cmdebug.vendor.{}'.format (name[0:n]))

            # Check if peripheral is defined in module
            if hasattr (mod, name[0:n] + '_' + periph):
                print ('Loaded: {} {}'.format (name[0:n], periph))
                # Store common name => [mod, name]
                VendorMod.mod[periph] = [mod, name[0:n]]
                return [mod, name[0:n]]
        
    # Not found
    return None


def VendorPeriph (periph):

    # Get mod
    mod, name = VendorMod (periph)
    
    # Check for periph return peripheral class
    if mod and hasattr (mod, name + '_' + periph):
        p = getattr (mod, name + '_' + periph)
        return p

    # Not found
    return None

# Load all peripherals
def VendorInit (name):
    for periph in get_periphs():
        VendorMod (periph, name)

    # Init chipset
    chip = VendorPeriph ('Chipset')
    chip (name)
