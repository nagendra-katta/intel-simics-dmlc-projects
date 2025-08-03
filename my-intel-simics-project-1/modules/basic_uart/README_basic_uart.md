# Simics DML Device: `basic_uart`

This is a basic UART simulation module for Simics written in DML 1.4. It demonstrates memory-mapped I/O using a simple UART device that supports:

- A **Transmit Register (TX)** for writing a byte
- A **Status Register (STAT)** for checking the TX_READY status

---

## 🛠️ Setup Steps

### 1. Create the device module skeleton

```bash
bin\project-setup.bat --device myuart
```

This generates the `modules/myuart/` directory with build scaffolding.

---


## 📄 2. Add DML Device Logic (`basic_uart.dml`)

```dml
dml 1.4;

device basic_uart;

param desc = "Basic UART simulation device";
param documentation = "Implements basic UART Tx/Rx with status and control.";

saved uint8 tx_data;
saved uint8 status;
saved uint8 ret;

bank uart_regs {
    register TX size 1 @ 0x00 is (write) {
        method write(uint64 val) {
            tx_data = val;
            log info: "UART TX: Sent byte 0x%x", tx_data;
            status |= 0x01;  // Set TX_READY
        }
    }

    register STAT size 1 @ 0x04 is read {
        method read() -> (uint64) {
            ret = status;
            status &= ~0x01;  // Clear TX_READY after read
            return ret;
        }
    }
}
```

---

## 🧱 3. Compile the module

```bash
make myuart
```

> ✅ Ensure `make` runs from the root Simics project directory.

---

## 🧪 4. Test Script (`targets/vacuum/test_uart.simics`)

```tcl
run-script "%script%/vacuum.simics"

# Load and create device
load-module basic_uart
@SIM_create_object("basic_uart", "uart0")

# Map device memory
phys_mem.add-map uart0.bank.uart_regs 0x1000 0x100 priority = 1

# View device
list-objects basic_uart

# Test write
phys_mem.write 0x1000 0xAA -b 1

# Test read (STAT register at 0x1004)
phys_mem.read 0x1004 -b 1
phys_mem.read 0x1004 -b 1
```

---

## ✅ Expected Behavior

```text
[uart0.bank.uart_regs info] UART TX: Sent byte 0xaa
1 (BE)   # TX_READY is set
0 (BE)   # TX_READY cleared after read
```

---

## ⚠️ Common Errors & Debugging

### ❌ `syntax error at 'val'`
**Cause**: Incorrect DML method syntax like:
```dml
method write (uint64 val) { // ❌ Incorrect
    tx_data = (uint8)val;  // ❌ Incorrect
}
```

**Fix**:
- Do not cast explicitly using C-style syntax.
- Use:
```dml
method write(uint64 val) { // ✅ No space between write and '('
    tx_data = val;         // ✅ Let DML handle the conversion
}
```


| ❌ Error | 🔍 Cause | ✅ Fix |
|--------|-------|------|
| `4 byte write access... outside registers` | Simics default write is 4 bytes | Use `-b 1` in `phys_mem.write` |
| `Failed writing memory at address ... nothing mapped` | Device wasn't properly mapped | Ensure `phys_mem.add-map` is done **before** write |
| `list-objects uart0` shows error | Wrong usage | Use `list-objects myuart` to view all devices of that class |

---

## 📌 Notes

- Even if only 2 registers (1 byte each) are used, devices are mapped in aligned chunks like `0x100` or `0x1000`.
- Use `-b 1` to write/read 1 byte. Misaligned access or default `-l` (4 bytes) may cause `spec-viol` errors.

---

## ✅ Working Example

```bash
simics targets/vacuum/test_uart.simics
```

```simics
phys_mem.write 0x1000 0x33 -b 1
[uart0.bank.uart_regs info] UART TX: Sent byte 0x33

phys_mem.read 0x1004 -b 1
1 (BE)

phys_mem.read 0x1004 -b 1
0 (BE)
```

---

## 📂 Directory Structure

```
my-intel-simics-project-1/
├── modules/
│   └── basic_uart/
│       └── basic_uart.dml
├── targets/
│   └── vacuum/
│       └── test_uart.simics
```

---

## 🔚 Conclusion

This UART simulation is a great starting point for understanding:
- Register banking in DML
- Saved variables
- Simics memory mapping and device interaction

You can now extend this by adding:
- RX register and data path
- Interrupt handling
- Loopback or DMA support

---