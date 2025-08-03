# © 2010 Intel Corporation

import stest
import info_status
import simics
import basic_uart_common

# Verify that info/status commands have been registered for all
# classes in this module.
info_status.check_for_info_status(['basic_uart'])

# Create an instance of each object defined in this module
dev = basic_uart_common.create_basic_uart()

# Run info and status on each object. It is difficult to test whether
# the output is informative, so we just check that the commands
# complete nicely.
for obj in [dev]:
    for cmd in ['info', 'status']:
        try:
            simics.SIM_run_command(obj.name + '.' + cmd)
        except simics.SimExc_General as e:
            stest.fail(cmd + ' command failed: ' + str(e))
