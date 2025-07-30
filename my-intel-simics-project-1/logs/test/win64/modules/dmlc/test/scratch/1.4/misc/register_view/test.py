testname = 'register_view'
scratchdir = 'C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\logs\\test\\win64\\modules\\dmlc\\test\\scratch\\1.4/misc/register_view'
basedir = 'C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\1.4\\misc'
SIM_add_module_dir(scratchdir)
SIM_module_list_refresh()
try:
    SIM_load_module('dml-test-register_view')
except:
    run_command('list-failed-modules -v')
    raise
obj = SIM_create_object('test', 'obj', [])
print('running', 'C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\1.4\\misc\\T_register_view.py')
import sys
sys.path.append('C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\common')
sys.path.append('C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\1.4\\misc')
SIM_source_python('C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\1.4\\misc\\T_register_view.py')
SIM_quit(0)
