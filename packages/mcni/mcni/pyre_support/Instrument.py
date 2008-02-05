#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# meta class of instrument
class InstrumentAuditor(type):

    def __init__(cls, name, bases, dict):
        type.__init__(name, bases, dict)

        #find all components
        componentnames = dir(cls.Inventory)
        componentnames = filter(
            lambda name: isinstance(getattr(cls.Inventory, name), NeutronComponentFacility ),
            componentnames )

        #build the Geometer component
        declarations = [
            8*' ' + '%s = Register("%s")' % (name, name) for name in componentnames ]
        declarations = '\n'.join( declarations )
        from Geometer import Geometer as base, Register
        code = '''
class Geometer(base):
    class Inventory(base.Inventory):
%s
        pass
    pass
''' % declarations
        exec code in locals()

        #add geometer into inventory
        import pyre.inventory
        geometer = Geometer()
        cls.Inventory.geometer = pyre.inventory.facility(
            'geometer', default = geometer)
        return

    pass # end of InstrumentAuditor
from NeutronComponentFacility import NeutronComponentFacility
            


from pyre.applications.Script import Script as base

class Instrument( base ):

    class Inventory( base.Inventory ):

        import pyre.inventory
        
        #properties
        ncount = pyre.inventory.float('ncount', default = 10000)
        ncount.meta['tip'] = 'number of total neutrons generated by source'
        
        outputdir = pyre.inventory.str('output-dir', default = 'out')
        outputdir.meta['tip'] = 'output directory'

        overwrite_datafiles = pyre.inventory.bool(
            'overwrite-datafiles',  default = False)
        overwrite_datafiles.meta['tip'] = 'overwrite data files?'
        
        buffer_size = pyre.inventory.int  ('buffer_size', default = 1000)
        buffer_size.meta['tip']= 'size of neutron buffer'

        from List import List
        sequence = List( 'sequence', default = '' )
        sequence.meta['tip'] = 'sequence of neutron components in this instrument'

        #facilities

        #geometer. this is a place holder. should derive from Geometer
        #to create a new Geometer for the specific instrument.
        from Geometer import Geometer
        geometer = pyre.inventory.facility(
            'geometer', default = Geometer() )
        geometer.meta['tip'] = 'geometer of instrument'

        pass # end of Inventory


    def __init__(self, name):
        base.__init__(self, name)
        self._warning = journal.warning( name )
        return


    def main(self, *args, **kwds):
        neutron_components = self.neutron_components
        for comp in neutron_components:
            if comp not in self.sequence:  
                self._warning.log(
                    'component %s was not included in component sequence %s' % (
                    comp, self.sequence )
                    )
                pass
            continue

        for name in self.sequence:
            if name not in neutron_components:
                raise RuntimeError , "Neutron component %s specified in sequence %s does not " \
                      "correspond to any known simulation components: %s" % (
                    name, self.sequence, neutron_components )
            continue

        outputdir = self.outputdir
        if not self.overwrite_datafiles and os.path.exists( outputdir ):
            print "output directory %r exists. If you want to overwrite the output "\
                  "directory, please specify option --overwrite-datafiles." % outputdir

        if not os.path.exists( outputdir ):
            os.makedirs( outputdir )
            
        os.chdir( outputdir )

        import mcni
        components = [ neutron_components[ name ] for name in self.sequence ]
        instrument = mcni.instrument( components )

        geometer = self.geometer

        n = int(self.ncount / self.buffer_size)
        assert n>0
        for i in range(n):
            neutrons = mcni.neutron_buffer( self.buffer_size )
            mcni.simulate( instrument, geometer, neutrons )
            continue
        
        return


    def _configure(self):
        base._configure(self)
        self.geometer = self.inventory.geometer
        self.overwrite_datafiles = self.inventory.overwrite_datafiles
        self.outputdir = self.inventory.outputdir
        self.sequence = self.inventory.sequence
        self.ncount = self.inventory.ncount
        self.buffer_size = self.inventory.buffer_size

        neutron_components = {}
        for name in self.inventory.facilityNames():
            comp = self.inventory.getTraitValue( name )
            if isinstance(comp, McniComponent):
                neutron_components[ name ] = comp
                pass
            continue

        self.neutron_components = neutron_components
        
        return


    __metaclass__ = InstrumentAuditor

    pass # end of Instrument


from mcni.AbstractComponent import AbstractComponent as McniComponent
import os, journal


# version
__id__ = "$Id$"

# End of file 
