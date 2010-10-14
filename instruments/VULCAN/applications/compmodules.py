# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
Sets name relations between McStas component and VNF neutron component

Example: "SNS_source4" -> "./vnfb/vnfb/dom/neutron_experiment_simulations/neutron_components/SNSModerator"

Notes:
    - Dom names that match McStas names are not included in this dictionary
"""

IMPORT_DICT     = {
    "SNS_source4":          "SNSModerator",
    "Collimator_linear":    "CollimatorLinear",     # not exist
    "L_monitor":            "LMonitor",    
    "Guide_gravity":        "GuideGravity",         # not exist
    "PSD_monitor":          "PSDMonitor",           # not exist
    "Monitor_nD":           "NDMonitor",            # not exist
    "V_sample":             "VanadiumPlate",
    "PSD_TEW_monitor":      "PSD_TEWMonitor"        # not exist
}

# Parameters dictionary for job builder
COMPVAR     = "component"
PARAMS_DICT      = {
    "xmin":     "%s.x_min" % COMPVAR,
    "xmax":     "%s.x_max" % COMPVAR,
    "ymin":     "%s.y_min" % COMPVAR,
    "ymax":     "%s.y_max" % COMPVAR,
    "filename": "outputfilename(%s)" % COMPVAR
}
__date__ = "$Oct 1, 2010 6:23:27 PM$"


