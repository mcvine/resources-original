#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def componentfactory( category, type ):
    from components import componentfactory
    from components.Registry import NotRegisteredError
    try: f = componentfactory( category, type )
    except NotRegisteredError: f = defaultcomponentfactory( category, type )
    return f


def printcomponentinfo( category, type ):
    import components
    if components.registered( category, type ):
        from components import componentinfo
        info = componentinfo( category, type )
    else:
        from utils.parsers import parseComponent
        path = defaultcomponentpath( category, type )
        info = parseComponent( path )
    print info
    return


def listallcomponentcategories( ):
    defaultcategories = listalldefaultcomponentcategories()
    import components
    categoriesinregistry = components.categoriesInRegistry()
    return uniquelist( defaultcategories + categoriesinregistry )


def listcomponentsincategory( category ):
    defaultcomponents = listdefaultcomponentsincategory( category )
    import components 
    registered = components.registeredComponentsInCategory( category )
    return uniquelist( defaultcomponents + registered )


def uniquelist( l ):
    return [ u for u in l if u not in locals()['_[1]'] ]


def defaultcomponentfactory( category, type ):
    path = defaultcomponentpath( category, type )
    from wrappers import wrap
    wrap( path, category )
    from components import componentfactory
    return componentfactory( category, type )


def listalldefaultcomponentcategories( ):
    libdir = defaultcomponentlibrarypath()
    import os
    from os.path import isdir, join
    excluded = ['CVS', 'data']
    items = os.listdir( libdir )
    items = filter(
        lambda item:
        not item.startswith( '.' ) and item not in excluded and isdir( join(libdir, item) ),
        items )
    return items


def listdefaultcomponentsincategory( category ):
    path = defaultcategorypath( category )
    import os
    from os.path import isfile, join
    excluded = ['CVS']
    items = os.listdir( path )
    postfix = '.comp'
    items = filter(
        lambda item:
        not item.startswith( '.' ) and item not in excluded and isfile( join(path, item) ) \
        and item.endswith( postfix ),
        items )
    return [item[: -len(postfix) ] for item in items]


def defaultcategorypath( category ):
    libdir = defaultcomponentlibrarypath()
    import os
    path = os.path.join( libdir, category )
    if not os.path.exists( path ) or not os.path.isdir(path):
        raise "default component category %s does not exist. Cannot find %s" % (
            category, path )
    return path


def defaultcomponentpath( category, type ):
    libdir = defaultcomponentlibrarypath()
    import os
    path = os.path.join( libdir, category, '%s.comp' % type )
    if not os.path.exists( path ) or not os.path.isfile(path):
        raise "default component (%s, %s) does not exist. Cannot find %s" % (
            category, type, path )
    return path


def defaultcomponentlibrarypath( ):
    from utils.xos import getEnv
    var = 'MCSTAS_COMPONENT_LIBDIR'
    path = getEnv( var, None )
    if path is None:
        raise "Please specify the default path to mcstas component library "\
              "as environment variable %r.\n"\
              "For example, in bash environment, do\n"\
              "  $ export %s=/.../mcstas/lib/mcstas\n"\
              % (var, var)
    return path

    
# version
__id__ = "$Id$"

# End of file 