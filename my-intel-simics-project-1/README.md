# ✅ Simics DMLC Build Setup (Windows)

This guide documents the working setup for building Simics DMLC modules on Windows using the **Simics Public Release 7.38.0**, **MSYS2**, and a **standalone MinGW-w64 compiler**.

---

## 🧱 Prerequisites

 ✅ **Intel® Simics® Public Release** (Installed using Package Manager)
 ✅ **MSYS2** (https://www.msys2.org/)
 ✅ **Standalone MinGW-w64 toolchain**  

- Not MSYS2's `usr/bin/gcc`, which gives:
  
  ```
  Only MinGW/GCC is supported on Windows
  ```

- You **downloaded and extracted** a working MinGW-w64 build into:
  
  ```
  C:\msys64\mingw64
  ```
  
  ➡ Your Simics project directory:  
  `C:\Users\nagen\simics-projects\my-intel-simics-project-1`

---

## 🌐 Environment Variable Setup

Set the following system/user environment variables:

### ➕ Add to PATH

```
C:\msys64\mingw64\bin
```

### 🔧 Define New Variables

```
SIMICS_BASE = C:/Users/nagen/AppData/Local/Programs/Simics/simics-7.38.0
SIMICS_PROJECT = C:\Users\nagen\simics-projects\my-intel-simics-project-1
```

---

## 🛠️ Simics Installation Steps

### 1. Download the following files from the link below:

- `intel-simics-package-manager`
- `simics-7-packages`

🔗 [https://lemcenter.intel.com/productDownload/?Product=256660e5-a404-4390-b436-f64324d94959](https://lemcenter.intel.com/productDownload/?Product=256660e5-a404-4390-b436-f64324d94959)

### 2. Install Simics Package Manager

- Right-click and **run as administrator**.
- Follow the prompts.

For more details, refer to the official guide:\
🔗 [https://www.intel.com/content/www/us/en/developer/articles/guide/simics-simulator-installation.html](https://www.intel.com/content/www/us/en/developer/articles/guide/simics-simulator-installation.html)

### 3. Open Simics Package Manager (run as administrator)

- From Windows Start Menu.
- Follow the on-screen steps.

### 4. Create a New Project

### 5. Select the required packages and proceed with the installation.

### 6. Download GRML ISO Image ***(Steps 6–8 Optional for GRML OS)***

- Download `grml-full-2025.05-amd64` from:\
  🔗 [https://grml.org/download/](https://grml.org/download/)

### 7. Copy the Image   ***(Optional for GRML OS)***

- Move the downloaded image to:
  
  ```
  C:\Users\<username>\AppData\Local\Programs\Simics\simics-qsp-x86-7.27.0\targets\qsp-x86\images\
  ```

### 8. Modify YAML File   ***(Optional for GRML OS)***

- Go to:
  
  ```
  C:\Users\<username>\AppData\Local\Programs\Simics\simics-qsp-x86-7.27.0\targets\qsp-x86
  ```

- Open the file `firststeps.target.yml`

- Replace the INCLUDE section with the following:

```lisp
if (params.get machine:software:linux:os_image) == NIL {
    local $default_image_url = "https://download.grml.org/grml-full_2025.05-amd64.iso"
    local $image = "grml-full-2025.05-amd64.iso"
    local $grml_in_proj = (lookup-file -query $image)
    local $grml_in_tree = (lookup-file -query "%simics%/targets/qsp-x86/images/" + $image)
    local $grml = $grml_in_proj or $grml_in_tree

    if not $grml {
        local $msg = ("ERROR: 'os_image' not set, and the default image" +
                      " could not be found.\n" +
                      "Please download \"" + $image + "\" from:\n\n    " +
                      $default_image_url +
                      "\n\nand place it in the project folder.")
        interrupt-script $msg -error
    }

    params.setdefault machine:software:linux:os_image $grml
}

run-script script = "%script%/firststeps-hardware.yml" namespace = machine:hardware
run-script script = "%script%/firststeps-network.yml" namespace = machine:network
run-script script = "%script%/firststeps-software.yml" namespace = machine:software

local $system = (params.get machine:system:name)
$system->system_info = (params.get machine:system:info)

run-script "%simics%/targets/common/rw-state.yml" namespace = persistent_state
```

---

## 📁 Directory Layout

```
C:\
├── msys64\
│   └── mingw64\        ← your working standalone MinGW-w64 GCC
│       └── bin\gcc.exe
├── Users\nagen\
│   └── simics-projects\
│       └── my-intel-simics-project-1\
│           ├── GNUmakefile
│           ├── config.mk           ← auto-generated
│           ├── config-user.mk      ← you created this manually
│           ├── compiler.mk         ← you edited this
│           ├── modules\
│           │   └── dmlc\           ← DML code goes here
│           └── targets\
│               └── vacuum\
│                   └── mydevice.simics
```

---

---

## ✅ Working Steps to Build `dmlc`

### 1. Simics Installation (as per Intel Guide)

Install:

- Simics Package Manager
- Simics Core Packages using `.ispm` bundle
- Create project from the package manager

➡ Your Simics project directory:  
`C:\Users\nagen\simics-projects\my-intel-simics-project-1`

---

### 2. Install MinGW-w64 Standalone (Not MSYS2 GCC)

❌ **Do not use** MSYS2 GCC (`/usr/bin/gcc`)  
✅ **Instead**, install a standalone MinGW-w64 build.

- Download from [https://winlibs.com](https://winlibs.com) or similar
- Extract to:  
  `C:\msys64\mingw64`

---

## 🔧 Edits You Made

### 3. ✅ `compiler.mk` — Set proper GCC path

```makefile
ifeq (default,$(origin CC))
    CC=C:\msys64\mingw64\bin\gcc.exe
    CXX=C:\msys64\mingw64\bin\g++.exe
endif
```

---

### 4. ✅ `config-user.mk` — Basic Setup for build

```makefile
SIMICS_BASE = C:\Users\nagen\AppData\Local\Programs\Simics\simics-7.38.0
SIMICS_PROJECT = C:\Users\nagen\simics-projects\my-intel-simics-project-1
HOST_TYPE = win64
```

---

### 5. Place Your DMLC Code

Repo : https://github.com/intel/device-modeling-language
Place your custom DML code here:

```bash
C:\Users\nagen\simics-projects\my-intel-simics-project-1\modules\dmlc\
```

---

### 6. ✅ `GNUmakefile` — Add `dmlc` build rule

```makefile
MAKE_HOST := mingw32-make 4.4.1   ***(Optional)***


.PHONY: dmlc

dmlc:
    $(MAKE) -C modules/dmlc

.PHONY: default
default: all
```

---

### 7. Build Your DML Module

```cmd
cd C:\Users\nagen\simics-projects\my-intel-simics-project-1
make dmlc
```

✅ Output should show successful DML compilation and Tests are OK.

---

### 8. ✅ After Building `dmlc`, Update `config-user.mk` with DMLC_DIR

To use the compiled DMLC module with Simics, add this line:

```makefile
DMLC_DIR = $(SIMICS_PROJECT)\$(HOST_TYPE)\bin
```

This ensures the DMLC Python bindings and libraries are correctly located during Simics runtime.

---

---

---

### Create Device Skeleton

### 1. Create Device Skeleton

Use Simics helper to generate your device structure:

```bash
bin\project-setup.bat --device mydevice
```

---

### 2. Add Your DML Code

Update the generated DML file in:

```bash
modules/mydevice/mydevice.dml
```

Sample content:

```tcl
dml 1.4;

device mydevice;
param desc = "sample DML device";
param documentation = "This is a very simple device.";

bank regs {
    register counter size 4 @ 0x0000 is (read) {
        method read() -> (uint64) {
            log info: "read from counter";
            return 42;
        }
    }
}
```

---

### 3. Build Your Module

From your project directory:

```bash
make mydevice
```

---

### 4. Create Configuration Script

Create a file named `mydevice.simics` inside:

```bash
targets/vacuum/
```

Sample content:

```tcl
run-script "%script%/vacuum.simics"
@SIM_create_object("mydevice", "dev1")
phys_mem.add-map dev1.bank.regs 0x1000 0x100
```

> ⚠️ Ensure `"mydevice"` matches the class name in your DML code.

---

### 5. Launch Simics and Run Your Device

```bash
simics.bat targets\vacuum\mydevice.simics
```

Expected output:

```
simics> phys_mem.read 0x1000 -l
[dev1.bank.regs info] read from counter
42 (LE)
```

✅ Success! You have built and interacted with a working custom device!

---

---

## ⚠️ Troubleshooting Summary

| ❌ Issue                                                                                   | ✅ Fix                                                                                                                                                                                  |
| ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `make binary does not appear to be a MingW make`                                          | Set `MAKE_HOST := mingw32-make 4.4.1` in `config-user.mk` or rename `mingw32-make.exe` to `make.exe`                                                                                   |
| `Only MingW/GCC is supported on Windows`                                                  | Use standalone MinGW-w64 (not MSYS2 `/usr/bin/gcc.exe`)                                                                                                                                |
| `No rule to make target 'dmlc'`                                                           | Add manual `dmlc` rule in `GNUmakefile`                                                                                                                                                |
| `C:\MinGW\bin\gcc.exe` not found                                                          | Override `CC` and `CXX` in `compiler.mk`                                                                                                                                               |
| `api-versions.mk: No such file`                                                           | Use valid Simics SDK environment and correct config                                                                                                                                    |
| `No class simple_device found`                                                            | DML class name mismatch — check the `create_object` line                                                                                                                               |
| `No target ...simics found`                                                               | Filename or path is wrong — verify spelling/case                                                                                                                                       |
| `touch` or `cp` command fails during DML build `process_begin: CreateProcess(...) failed` | Indicates wrong shell or environment; use MSYS2 MinGW64 only. Some MSYS2 installations lack essential UNIX tools — re-run `pacman -Syu` and install `make`, `gcc`, `cp`, `touch`, etc. |

Add these steps to your `pacman` setup for error  `process_begin: CreateProcess(...) failed`:

```bash
pacman -Syu
pacman -S make gcc
pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-gcc-objc
```

Or install [Git for Windows](https://git-scm.com/download/win) and use **Git Bash** for a working Unix-like shell with `touch`, `cp`, `make`, etc.

---

---

---

## ✅ Final Checklist

- [x] MSYS2 installed and updated
- [x] Standalone MinGW-w64 compiler at `C:\msys64\mingw64`
- [x] `compiler.mk` points to correct GCC
- [x] `config-user.mk` defines `SIMICS_BASE` and `HOST_TYPE`
- [x] `GNUmakefile` has `dmlc` rule
- [x] `make mydevice` builds successfully
- [x] Device runs with Simics and `phys_mem.read` shows correct value
