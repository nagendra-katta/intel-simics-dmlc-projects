testname = 'endian_int_aliasing'
scratchdir = 'C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\logs\\test\\win64\\modules\\dmlc\\test\\scratch\\1.4/statements/endian_int_aliasing'
basedir = 'C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\1.4\\statements'
SIM_add_module_dir(scratchdir)
SIM_module_list_refresh()
try:
    SIM_load_module('dml-test-endian_int_aliasing')
except:
    run_command('list-failed-modules -v')
    raise
obj = SIM_create_object('test', 'obj', [])
SIM_quit(0)
