#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2007-2011 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


standalone = True


import os, shutil
for entry in os.listdir('.'):
    if not entry.startswith('out-test'):
        continue
    if not os.path.isdir(entry):
        continue
    shutil.rmtree(entry)
    continue


import unittestX as unittest

class TestCase(unittest.TestCase):

    def test1(self):
        'ndmonitor: tof'
        cmd = 'mcvine-simulate -components=source,monitor --- -source=Source_simple -monitor="NDMonitor(tof)" -geometer.monitor="(0,0,10),(0,0,0)" -source.E0=100 -source.dE=10 -source.width=0.05 -source.height=0.05 -source.radius=0 -source.dist=9.5 -source.xw=0.05 -source.yh=0.05 -monitor.tofmin=0 -monitor.tofmax=0.005 -monitor.ntof=100 -monitor.filename=itof.h5 --output-dir=out-test1'
        import os
        if os.system(cmd):
            raise RuntimeError, "%r failed" % cmd
        return


    def test2(self):
        'ndmonitor: xdiv, x'
        cmd = 'mcvine-simulate -components=source,monitor --- -source=Source_simple -monitor="NDMonitor(x,divx)" -geometer.monitor="(0,0,10),(0,0,0)" -source.E0=100 -source.dE=10 -source.width=0.05 -source.height=0.05 -source.radius=0 -source.dist=9.5 -source.xw=0.05 -source.yh=0.05 -monitor.xmin=-0.1 -monitor.xmax=0.1 -monitor.nx=100  -monitor.divxmin=-0.01 -monitor.divxmax=0.01 -monitor.ndivx=100 -monitor.filename=ixdivx.h5 --output-dir=out-test2'
        import os
        if os.system(cmd):
            raise RuntimeError, "%r failed" % cmd
        return


    def test3(self):
        'ndmonitor: energy'
        cmd = 'mcvine-simulate -components=source,monitor --- -ncount=1e4 -buffer_size=1000 -source=MonochromaticSource -monitor="NDMonitor(energy)" -geometer.monitor="(0,0,1),(0,0,0)" -source.energy=60 -monitor.energymin=0 -monitor.energymax=100 -monitor.nenergy=100 -monitor.filename=ienergy.h5 --output-dir=out-test3'
        import os
        if os.system(cmd):
            raise RuntimeError, "%r failed" % cmd

        from histogram.hdf import load
        from histogram.hdf.utils import getOnlyEntry
        f = 'out-test3/ienergy.h5'
        h = load(f, getOnlyEntry(f))
        self.assertEqual( h[(58, 62)].sum() , (1., 1.e-4))
        return


    def test4(self):
        'ndmonitor: w'
        cmd = 'mcvine-simulate -components=source,monitor --- -ncount=1e4 -buffer_size=1000 -source=MonochromaticSource -monitor="NDMonitor(w)" -geometer.monitor="(0,0,1),(0,0,0)" -source.energy=60 -monitor.wmin=0 -monitor.wmax=100 -monitor.nw=100 -monitor.filename=iw.h5 --output-dir=out-test3'
        import os
        if os.system(cmd):
            raise RuntimeError, "%r failed" % cmd

        from histogram.hdf import load
        from histogram.hdf.utils import getOnlyEntry
        f = 'out-test3/iw.h5'
        h = load(f, getOnlyEntry(f))
        # self.assertEqual( h[(58, 62)].sum() , (1., 1.e-4))
        return


#    def test_sizes(self):
#        'ndmonitor: w; tests: xwidth, yheight'
#        cmd = 'mcvine-simulate -components=source,monitor --- -ncount=1e4 -buffer_size=1000 -source=MonochromaticSource -monitor="NDMonitor(w)" -geometer.monitor="(0,0,1),(0,0,0)" -source.energy=60 -monitor.wmin=0 -monitor.wmax=100 -monitor.nw=100 -monitor.filename=iw.h5 --output-dir=out-test3'
#        import os
#        if os.system(cmd):
#            raise RuntimeError, "%r failed" % cmd
#
#        from histogram.hdf import load
#        from histogram.hdf.utils import getOnlyEntry
#        f = 'out-test3/iw.h5'
#        h = load(f, getOnlyEntry(f))
#        # self.assertEqual( h[(58, 62)].sum() , (1., 1.e-4))
#        return

    


def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    #debug.activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id: MultiMonitors_TestCase.py 659 2010-10-24 18:20:07Z linjiao $"

# End of file 
