# © 2023 Intel Corporation

simics_add_module(uart_core
  CLASSES uart_core
  SOURCES uart_core.dml module_load.py
  SIMICS_API 7
)
add_subdirectory(test)
