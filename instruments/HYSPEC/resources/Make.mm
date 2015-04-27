# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                        California Institute of Technology
#                        (C) 2006-2013  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

PROJECT = mcvine/instruments/HYSPEC

# directory structure

#--------------------------------------------------------------------------
all: export
#

CP_RF = rsync -a


EXPORT_SHAREDIR=$(EXPORT_ROOT)/share
SHARE_DEST =  $(EXPORT_SHAREDIR)/$(PROJECT)

export:: export-package-data

export-package-data:: $(EXPORT_DATADIRS)
	mkdir -p $(SHARE_DEST); \
	$(CP_RF) ./ $(SHARE_DEST)/


# version
# $Id: Make.mm 744 2010-12-09 15:11:58Z linjiao $

# End of file
