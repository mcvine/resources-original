# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = mcstas2/utils
PACKAGE = parsers

RECURSE_DIRS = \
	pyparsing \

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	__init__.py \
	ComponentHeaderParser.py \
	ComponentInfo.py \
	ComponentParser.py \
	ShareIncludeParser.py \
	McStasComponentParser.py \


export:: export-package-python-modules 

# version
# $Id: Make.mm 312 2005-06-02 20:25:25Z linjiao $

# End of file
