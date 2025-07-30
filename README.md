# 🧪 intel-simics-dmlc-projects

A collection of sample Simics DMLC (Device Modeling Language Compiler) projects designed to help you build and test custom Simics device models on Windows using standalone MinGW-w64.

---

## 📁 Project 1: `sample-mydevice`

A basic Simics device module to demonstrate:
- Custom device creation using DMLC
- Manual build setup using `mingw32-make`
- Simics script execution and memory-mapped register testing

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

## 📚 How to Use

See [`README.md`](my-intel-simics-project-1/README.md) inside `my-intel-simics-project-1/` for full setup and build instructions.

---

## 📦 Repository Layout

