# © 2010 Intel Corporation

import simics

# Extend this function if your device requires any additional attributes to be
# set. It is often sensible to make additional arguments to this function
# optional, and let the function create mock objects if needed.
def create_basic_uart(name = None):
    '''Create a new basic_uart object'''
    basic_uart = simics.pre_conf_object(name, 'basic_uart')
    simics.SIM_add_configuration([basic_uart], None)
    return simics.SIM_get_object(basic_uart.name)
