/* module_id.c - automatically generated, do not edit */

#include <simics/build-id.h>
#include <simics/base/types.h>
#include <simics/util/help-macros.h>

#if defined(SIMICS_7_API)
#define BUILD_API "7"
#elif defined(SIMICS_6_API)
#define BUILD_API "6"
#else
#define BUILD_API "?"
#endif

#define EXTRA "                                           "

EXPORTED const char _module_capabilities_[] =
	"VER:" SYMBOL_TO_STRING(SIM_VERSION_COMPAT) ";"
	"ABI:" SYMBOL_TO_STRING(SIM_VERSION) ";"
	"API:" BUILD_API ";"
	"BLD:" "0" ";"
	"BLD_NS:__simics_project__;"
	"BUILDDATE:" "1753892025" ";"
	"MOD:" "mydevice" ";"
	"CLS:mydevice" ";"
	"HOSTTYPE:" "win64" ";"
	"THREADSAFE;"
	EXTRA ";";
EXPORTED const char _module_date[] = "Wed Jul 30 21:43:45 2025";
extern void _initialize_mydevice_dml(void);
extern void init_local(void) {}
EXPORTED void _simics_module_init(void);
extern void sim_iface_wrap_init(void);

extern void init_local(void);

void
_simics_module_init(void)
{

	_initialize_mydevice_dml();
	init_local();
}
