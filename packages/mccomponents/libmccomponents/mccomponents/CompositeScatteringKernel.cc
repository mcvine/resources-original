// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                        (C) 2007  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#include "mccomposite/mccomposite.h"
#include "mccomponents/random.h"
#include "mccomponents/CompositeScatteringKernel.h"


struct mccomponents::CompositeScatteringKernel::Details{
  random::Generator random_number_generator;
};


// meta-methods
mccomponents::CompositeScatteringKernel::CompositeScatteringKernel
( const kernels_t & kernels )
  : m_kernels(kernels),
    m_details(new Details)
{
}

mccomponents::CompositeScatteringKernel::~CompositeScatteringKernel
()
{
}

// methods
double 
mccomponents::CompositeScatteringKernel::absorption_coefficient
( const mcni::Neutron::Event & ev )
{
  double ret = 0.;
  for (size_t i=0; i<m_kernels.size(); i++) 
    ret += m_kernels[i]->absorption_coefficient( ev );
  return ret;
}

double
mccomponents::CompositeScatteringKernel::scattering_coefficient
( const mcni::Neutron::Event & ev ) 
{
  double ret = 0.;
  for (size_t i=0; i<m_kernels.size(); i++) 
    ret += m_kernels[i]->scattering_coefficient( ev );
  return ret;
}

void mccomponents::CompositeScatteringKernel::scatter
( mcni::Neutron::Event & ev )
{
  size_t n = m_kernels.size();

  size_t index = size_t( m_details->random_number_generator.generate(0,n) );
  
  ev.probability *= n;
  ev.probability *= m_kernels[index]->scattering_coefficient( ev ) / scattering_coefficient(ev);
  m_kernels[index]->scatter( ev );
}

void mccomponents::CompositeScatteringKernel::absorb
( mcni::Neutron::Event & ev )
{
  size_t n = m_kernels.size();

  size_t index = size_t( m_details->random_number_generator.generate(0,n) );
  
  ev.probability *= n;
  ev.probability *= m_kernels[index]->absorption_coefficient( ev ) / absorption_coefficient(ev);
  m_kernels[index]->absorb( ev );
}


// version
// $Id$

// End of file 