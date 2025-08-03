# 🧪 intel-simics-dmlc-projects

A collection of sample Simics DMLC (Device Modeling Language Compiler) projects designed to help you build and test custom Simics device models on Windows using standalone MinGW-w64.

---

## 📁 Projects

### 1. `mydevice`
A basic Simics device module to demonstrate:
- Custom device creation using DMLC
- Manual build setup using `mingw32-make`
- Simics script execution and memory-mapped register testing

### 2. `basic_uart`
A simple UART (Universal Asynchronous Receiver-Transmitter) implementation featuring:
- Basic TX functionality
- Memory-mapped register interface
- Simple status tracking

### 3. `uart_core`
An advanced UART implementation with:
- Full TX/RX functionality with status management
- Overrun detection and error handling
- Comprehensive logging system
- CLI-accessible data injection interface
- Complete test suite with multiple scenarios

---

## 📖 What's Included

- `my-intel-simics-project-1/`  
  Complete setup for a custom Simics DMLC module called `mydevice`.

---

## 📌 Features

- ✅ Setup using Simics 7.38.0 (Public Release)
- ✅ Standalone MinGW-w64 integration (not MSYS2 GCC)
- ✅ Manual build rules with `GNUmakefile`, `compiler.mk`, `config-user.mk`
- ✅ Verified DMLC build and Simics simulation with `phys_mem` mapping
- ✅ GRML ISO configuration steps included (optional for QSP)

---

## 🚀 Next Projects (Planned)

- Advanced interrupt controller simulation
- Memory-mapped I/O device with internal state machines
- Timer/RTC simulation modules
- DMA and I/O bus device simulations

---

## 📚 Documentation & Setup

For detailed documentation and setup instructions, refer to:

- [`README.md`](my-intel-simics-project-1/README.md) - Main project setup and Sample device implementation guide
- [`README_basic_uart.md`](my-intel-simics-project-1/modules/basic_uart/README_basic_uart.md) - Basic UART implementation guide
- [`README_uart_core.md`](my-intel-simics-project-1/modules/uart_core/README_uart_core.md) - Advanced UART implementation and testing guide
---

