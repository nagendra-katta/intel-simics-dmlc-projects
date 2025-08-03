# © 2023 Intel Corporation

simics_add_module(basic_uart
  CLASSES basic_uart
  SOURCES basic_uart.dml module_load.py
  SIMICS_API 7
)
add_subdirectory(test)
