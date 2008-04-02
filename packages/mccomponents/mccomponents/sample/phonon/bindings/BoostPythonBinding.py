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



from mccomponents.homogeneous_scatterer.bindings.BoostPythonBinding \
     import BoostPythonBinding, extend

import mccomponents.mccomponentsbp as b
import mccomposite.mccompositebp as b1


class New:

    def ndarray( self, npyarr ):
        '''create boost python instance of NdArray object
    arguments:
        npyarr: numpy array. it must be a contiguous array.
        '''
        import numpy
        assert npyarr.dtype == numpy.double, "only work for double array for this time"
        
        import numpyext
        ptr = numpyext.getdataptr( npyarr )
        
        import bpext
        wp = bpext.wrap_native_ptr( ptr )
        
        shape = b.vector_uint( 0 )
        for i in npyarr.shape: shape.append( i )

        factory = 'new_NdArray_dblarr_%d' % len(shape)
        a1 = getattr(b,factory)( wp, shape )
        a1.origin = npyarr # keep a reference to avoid seg fault
        return a1


    def atomicscatterer(
        self, position, mass,
        coherent_scattering_length, coherent_cross_section):
        
        '''create a boost python object of AtomicScatterer

    position: position of atom (unit: angstrom)
    mass: mass of atom
    coherent_scattering_length: (unit: fm)
    coherent_cross_section: (unit: barn)
    '''
        position = self.position( *position )
        return b.AtomicScatterer(
            position, mass, coherent_scattering_length, coherent_cross_section )


    def atomicscatterer_fromSite(self, site):
        '''create a boost python object of AtomicScatterer

    site: a crystal.Site instance
    '''
        position = site.getPosition()
        atom = site.getAtom()
        mass = atom.mass
        coh_xs = atom.average_neutron_coh_xs

        # !!!!!!!
        # the following is a hack. should get it directly from atom
        from math import sqrt, pi
        coh_b = sqrt( coh_xs * 100 /4/pi )

        #
        return self.atomicscatterer(
            position, mass, coh_b, coh_xs )


    def linearlyinterpolateddos(
        self, e0, de, n, Z):
        '''create boost python object of LinearlyInterpolatedDOS
        
        e0: minimum phonon energy. float
        de: phonon energy step. float
        n: number of points.
        Z: values of DOS at the energy points defined by (e0, de, n)
        '''
        Z1 = b.vector_double( n )
        for i in range(n): Z1[i] = Z[i]
        
        return b.LinearlyInterpolatedDOS_dbl( e0, de, n, Z1 )


    def dos_fromhistogram( self, doshist ):
        assert doshist.__class__.__name__ == 'Histogram', "%s is not a histogram" % (doshist,)
        energies = doshist.energy
        e0 = energies[0]
        de = energies[1] - energies[0]
        n = len(energies)
        Z = doshist.I
        return self.linearlyinterpolateddos( e0, de, n, Z )


    def dwfromDOS(self, dos, mass, temperature, nsampling):
        '''create boost python object of DWFromDOS
    dos: DOS bp object
    mass: mass of atoms in unit cell
    temperature: temperature (K)
    nsampling: number of sampling points
    '''
        ret = b.DWFromDOS_dbl(dos, nsampling)
        ret.calc_DW_core( mass, temperature )
        return ret
    

    def linearlyinterpolatableaxis( self, min, step, n):
        '''create boost python object of LinearlyInterpolatableAxis.

    min: minimum
    step: step size
    n: max = min+step*n (max is included in axis)
        '''
        return b.LinearlyInterpolatableAxis_dbl( min, step, n )


    def linearlyinterpolateddispersion(
        self, 
        natoms, Qaxes, eps_npyarr, E_npyarr ):
        dim = len(Qaxes)
        f = getattr(self, 'linearlyinterpolateddispersion_%sd' % dim)
        return f( natoms, Qaxes, eps_npyarr, E_npyarr )
    

    def linearlyinterpolateddispersion_3d(
        self, 
        natoms, Qaxes, eps_npyarr, E_npyarr ):
        '''create boost python object of LinearlyInterpolatedDispersion_3D
        
    natoms: number of atoms in the unit cell
    Qaxes: a 3-tuple of Q axes. Each item is a 3-tuple of (min, step, n)
        Example: [ (-10., 1., 20), (-10., 1., 20), (-10., 1., 20) ]
        n is number of points on axis.
    eps_npyarr: numpy array of poloarization. shape  must be
        nQx, nQy, nQz, nBranches, nAtoms, 3, 2 
    E_npyarr: numpy array of phonon energy. shape  must be
        nQx, nQy, nQz, nBranches 
    '''
        #c++ engine require Qmax = Qmin + n * step, and that means n+1 Q points
        for i,axis in enumerate(Qaxes):
            Qaxes[i] = axis[0], axis[1], axis[2]-1
            continue
        
        Qx_axis = self.linearlyinterpolatableaxis( *(Qaxes[0]) )
        Qy_axis = self.linearlyinterpolatableaxis( *(Qaxes[1]) )
        Qz_axis = self.linearlyinterpolatableaxis( *(Qaxes[2]) )
        
        eps_arr = self.ndarray( eps_npyarr )
        E_arr = self.ndarray( E_npyarr )
        
        disp = b.LinearlyInterpolatedDispersionOnGrid_3D_dblarrays(
            natoms, Qx_axis, Qy_axis, Qz_axis, eps_arr, E_arr )
        return disp


    def phonon_coherentinelastic_polyxtal_kernel(
        self,
        dispersion, dw_calctor,
        unitcell, 
        temperature, Ei,  max_omega, max_Q,
        nMCsteps_to_calc_RARV):

        unitcell_vol = unitcell.getVolume()
        
        atoms = [ self.atomicscatterer_fromSite( site ) for site in unitcell ]
        atom_vector = b.vector_AtomicScatterer(0)
        for atom in atoms: atom_vector.append( atom )
        
        return b.Phonon_CoherentInelastic_PolyXtal_kernel(
            dispersion, atom_vector, unitcell_vol, dw_calctor,
            temperature, Ei, max_omega, max_Q,
            nMCsteps_to_calc_RARV)

    pass # end of BoostPythonBinding


extend( New )



# method __getitem__ to replace the boost python generated __getitem__
def bp_ndarray_getitem(self, indexes):
    cindexes = b.vector_uint( 0 )
    for ind in indexes: cindexes.append( ind )
    return self._getitem_bp( cindexes )


# go thru ndarray bp types and change interfaces
def _fix_bp_ndarray_interface( ):
    for i in range( 1,7 ):
        clsname = 'NdArray_dblarr_%d' % i
        cls = getattr( b, clsname )
        cls._getitem_bp = cls.__getitem__
        cls.__getitem__ = bp_ndarray_getitem
        continue
    return


_fix_bp_ndarray_interface()
        

# version
__id__ = "$Id$"

# End of file 