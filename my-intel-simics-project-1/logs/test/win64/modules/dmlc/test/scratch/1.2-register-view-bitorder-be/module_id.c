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
	"BLD_NS:__dmlc_tests__;"
	"BUILDDATE:" "1753860165" ";"
	"MOD:" "dml-test-1.2-register-view-bitorder-be" ";"
	"CLS:test" ";"
	"HOSTTYPE:" "win64" ";"
	"PY_MINOR_VERSION:9;"
	EXTRA ";";
EXPORTED const char _module_date[] = "Wed Jul 30 12:52:45 2025";
extern void _initialize_T_1_2_register_view_bitorder_be(void);
extern void init_local(void) {}
EXPORTED void _simics_module_init(void);
extern void sim_iface_wrap_init(void);

extern void init_local(void);

void
_simics_module_init(void)
{

	_initialize_T_1_2_register_view_bitorder_be();
	init_local();
}
