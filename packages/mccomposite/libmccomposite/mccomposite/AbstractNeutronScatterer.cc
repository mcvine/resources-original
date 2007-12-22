// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                         (C) 2005 All Rights Reserved  
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


#include "mccomposite/AbstractNeutronScatterer.h"
#include "mccomposite/CompositeNeutronScatterer_Impl.h"


struct mccomposite::AbstractNeutronScatterer::Details {
  Details( AbstractNeutronScatterer & scatterer ) 
    : composite( scatterer.shape(), scatterers, geometer )
  {
    scatterers.push_back( &scatterer );
  }

  CompositeNeutronScatterer_Impl::scatterercontainer_t scatterers;
  CompositeNeutronScatterer_Impl::geometer_t geometer;
  CompositeNeutronScatterer_Impl composite;
};



mccomposite::AbstractNeutronScatterer::AbstractNeutronScatterer
(const AbstractShape & shape)
  : m_shape( shape ),
    m_details( new Details(*this) )
{
}

mccomposite::AbstractNeutronScatterer::~AbstractNeutronScatterer
()
{
}

const mccomposite::AbstractShape & mccomposite::AbstractNeutronScatterer::shape
() const
{
  return m_shape;
}

void
mccomposite::AbstractNeutronScatterer::scatter
(mcni::Neutron::Event & ev)
{
  m_details->composite.scatter( ev );
}

double
mccomposite::AbstractNeutronScatterer::calculate_attenuation
(const mcni::Neutron::Event & ev, const geometry::Position & end) const
{
  return 1.;
}

void
mccomposite::AbstractNeutronScatterer::scatterM
(const mcni::Neutron::Event & ev, mcni::Neutron::Events &evts)
{
  m_details->composite.scatterM(ev, evts);
}

mccomposite::AbstractNeutronScatterer::InteractionType
mccomposite::AbstractNeutronScatterer::interactM_path1
(const mcni::Neutron::Event & ev, mcni::Neutron::Events &evts)
{
  mcni::Neutron::Event newev = ev;
  InteractionType ret = interact_path1(newev);
  evts.push_back( newev );
  return ret;
}



// version
// $Id: AbstractNeutronScatterer.cc 591 2006-09-25 07:17:26Z linjiao $

// End of file 