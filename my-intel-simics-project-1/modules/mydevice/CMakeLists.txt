# © 2023 Intel Corporation

simics_add_module(mydevice
  CLASSES mydevice
  SOURCES mydevice.dml module_load.py
  SIMICS_API 7
)
add_subdirectory(test)
