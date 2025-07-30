testname = 'par_over_endian'
scratchdir = 'C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\logs\\test\\win64\\modules\\dmlc\\test\\scratch\\1.2/registers/par_over_endian'
basedir = 'C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\1.2\\registers'
SIM_add_module_dir(scratchdir)
SIM_module_list_refresh()
try:
    SIM_load_module('dml-test-par_over_endian')
except:
    run_command('list-failed-modules -v')
    raise
obj = SIM_create_object('test', 'obj', [])
print('running', 'C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\1.2\\registers\\T_par_over_endian.py')
import sys
sys.path.append('C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\common')
sys.path.append('C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\1.2\\registers')
SIM_source_python('C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\1.2\\registers\\T_par_over_endian.py')
SIM_quit(0)
