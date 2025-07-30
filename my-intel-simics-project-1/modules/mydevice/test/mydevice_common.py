# © 2010 Intel Corporation

import simics

# Extend this function if your device requires any additional attributes to be
# set. It is often sensible to make additional arguments to this function
# optional, and let the function create mock objects if needed.
def create_mydevice(name = None):
    '''Create a new mydevice object'''
    mydevice = simics.pre_conf_object(name, 'mydevice')
    simics.SIM_add_configuration([mydevice], None)
    return simics.SIM_get_object(mydevice.name)
