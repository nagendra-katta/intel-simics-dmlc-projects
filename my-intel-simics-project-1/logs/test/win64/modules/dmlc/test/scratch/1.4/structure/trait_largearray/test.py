testname = 'trait_largearray'
scratchdir = 'C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\logs\\test\\win64\\modules\\dmlc\\test\\scratch\\1.4/structure/trait_largearray'
basedir = 'C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\1.4\\structure'
SIM_add_module_dir(scratchdir)
SIM_module_list_refresh()
print('running', 'C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\1.4\\structure\\T_trait_largearray.py')
import sys
sys.path.append('C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\common')
sys.path.append('C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\1.4\\structure')
SIM_source_python('C:\\Users\\nagen\\simics-projects\\my-intel-simics-project-1\\modules\\dmlc\\test\\1.4\\structure\\T_trait_largearray.py')
SIM_quit(0)
