testname = 'checkpointing'
scratchdir = 'C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\logs\\test\\win64\\modules\\dmlc\\test\\scratch\\1.4/hooks/checkpointing'
basedir = 'C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\1.4\\hooks'
SIM_add_module_dir(scratchdir)
SIM_module_list_refresh()
try:
    SIM_load_module('dml-test-checkpointing')
except:
    run_command('list-failed-modules -v')
    raise
obj = SIM_create_object('test', 'obj', [])
print('running', 'C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\1.4\\hooks\\T_checkpointing.py')
import sys
sys.path.append('C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\common')
sys.path.append('C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\1.4\\hooks')
SIM_source_python('C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\1.4\\hooks\\T_checkpointing.py')
SIM_quit(0)
