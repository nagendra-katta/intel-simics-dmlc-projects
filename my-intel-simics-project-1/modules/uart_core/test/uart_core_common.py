# © 2010 Intel Corporation

import simics

# Extend this function if your device requires any additional attributes to be
# set. It is often sensible to make additional arguments to this function
# optional, and let the function create mock objects if needed.
def create_uart_core(name = None):
    '''Create a new uart_core object'''
    uart_core = simics.pre_conf_object(name, 'uart_core')
    simics.SIM_add_configuration([uart_core], None)
    return simics.SIM_get_object(uart_core.name)
