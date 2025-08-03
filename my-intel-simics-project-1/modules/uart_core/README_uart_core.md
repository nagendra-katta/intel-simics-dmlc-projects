# 🎯 UART Core Device - Complete Development Guide

This document provides a comprehensive guide to understanding and working with the UART Core device implementation in Intel Simics using DML 1.4. This guide is designed for new developers to understand the complete development process, including all challenges faced and solutions implemented. 

## 📑 Table of Contents

1. [🔍 Project Overview](#project-overview) 
2. [🏗️ Architecture and Design](#architecture-and-design) 
3. [🚀 Development Process](#development-process) 
4. [🔧 Error Fixes and Solutions](#error-fixes-and-solutions) 
5. [⚙️ Building and Testing](#building-and-testing) 
6. [📖 Usage Examples](#usage-examples) 
7. [🔌 Method Exposure Explanation](#method-exposure-explanation) 
8. [⭐ Advanced Features](#advanced-features) 
9. [❓ Troubleshooting](#troubleshooting) 

## 🔍 Project Overview

### 📱 What is This Project?

This project implements a **UART (Universal Asynchronous Receiver-Transmitter) Core device** using **DML 1.4** (Device Modeling Language) for Intel Simics simulation platform. The UART device simulates serial communication functionality with: 

- **TX (Transmit) Register**: For sending data out 
- **RX (Receive) Register**: For receiving data  
- **STATUS Register**: For checking device state 
- **Comprehensive Logging**: For debugging and monitoring 
- **External Data Injection**: For testing RX functionality 
  
  

### Key Features Implemented

- ✅ Memory-mapped register interface 
- ✅ TX/RX data handling with status management 
- ✅ Overrun detection and error handling 
- ✅ Comprehensive info-level logging for all operations 
- ✅ External method exposure for data injection 
- ✅ Complete test suite with multiple scenarios 

## 🏗️ Architecture and Design

### 📊 Register Layout

```
Base Address: 0x1000 (configurable via memory mapping) 
├── TX Register   (0x1000) - Write-only, 1 byte - Transmit data 
├── RX Register   (0x1001) - Read-only,  1 byte - Receive data   
└── STAT Register (0x1002) - Read-only,  1 byte - Status flags 
```

### Status Register Bit Layout

```
Bit Position: 7 6 5 4 3 2 1 0 
             [Reserved ] |O|R|T| 
                         | | |└── TX_READY  (0x01) - Transmission complete 
                         | |└──── RX_READY  (0x02) - Data available for reading 
                         |└────── OVERRUN   (0x04) - Data overwritten before read 
```

### Device State Variables

```dml
saved uint8 tx_data;    // Last transmitted data 
saved uint8 rx_data;    // Current received data buffer 
saved uint8 status;     // Status register value 
saved uint8 ret;        // Temporary variable for status reads 
```

**Why `saved`?** The `saved` keyword ensures these variables persist across Simics save/restore operations, maintaining device state consistency. 

## Complete DML Implementation

Below is the complete `uart_core.dml` file with detailed comments explaining each section: 

```dml
dml 1.4; 


device uart_core; 


param desc = "Basic UART simulation"; 


param documentation = "Simulates UART TX and RX"; 


// Device-scoped state variables (global to this device instance) 
// These persist across simulation saves/restores and are accessible from all methods 
saved uint8 tx_data;    // Last data written to TX register 
saved uint8 rx_data;    // Current data available in RX buffer 
saved uint8 status;     // Status register: bit 0=TX_READY, bit 1=RX_READY, bit 2=OVERRUN 
saved uint8 ret;        // Temporary variable for status register reads 


/** 
 * Device initialization method - called when device is created 
 * Sets up initial state and logs device configuration 
 */ 
method init() { 
    log info: "UART Core: Device initialized"; 
    log info: "UART Core: Register layout - TX:0x00, RX:0x01, STAT:0x02"; 
    log info: "UART Core: Status bits - TX_READY:0x01, RX_READY:0x02, OVERRUN:0x04"; 

    // Initialize all state variables to known values 
    status = 0;     // Clear all status bits 
    tx_data = 0;    // Clear TX data buffer 
    rx_data = 0;    // Clear RX data buffer 
    ret = 0;        // Clear temporary variable 
} 


/** 
 * UART register bank - contains all memory-mapped registers 
 * Base address mapping: TX=0x00, RX=0x01, STAT=0x02 
 */ 
bank uart_regs { 
    /** 
     * TX Register (Write-only) - Transmit Data Register 
     * Address: 0x00, Size: 1 byte 
     * Writing to this register simulates sending data via UART TX line 
     */ 
    register TX size 1 @ 0x00 is (write) { 
        method write(uint64 val) { 
            // Log the data being transmitted (hex + ASCII if printable) 
            log info: "UART TX: Writing data 0x%02x ('%c')", val, cast(val >= 32 && val <= 126 ? val : '?', int32); 

            // Store the transmitted data 
            tx_data = val; 

            // Set TX ready status bit (bit 0) to indicate transmission complete 
            status |= 0x01; // Set TX ready status 

            log info: "UART TX: Status updated to 0x%02x", status; 
        } 
    } 
    /** 
     * RX Register (Read-only) - Receive Data Register 
     * Address: 0x01, Size: 1 byte 
     * Reading from this register retrieves received data and clears RX ready status 
     */ 
    register RX size 1 @ 0x01 is (read) { 
        method read() -> (uint64) { 
            log info: "UART RX: Read attempt, current status 0x%02x", status; 

            // Check if RX data is available (bit 1 of status register) 
            if ((status & 0x02) != 0) { // Check if RX data is available 
                // Log the data being read (hex + ASCII if printable) 
                log info: "UART RX: Returning data 0x%02x ('%c')", rx_data, cast(rx_data >= 32 && rx_data <= 126 ? rx_data : '?', int32); 

                // Clear RX ready status bit (bit 1) - data has been consumed 
                status &= ~0x02; // Clear RX ready status 

                log info: "UART RX: Status cleared to 0x%02x", status; 
                return rx_data; 
            } else { 
                // No data available - return 0 
                log info: "UART RX: No data available, returning 0"; 
                return 0; // No data available 
            } 
        } 
    } 
    /** 
     * STAT Register (Read-only) - Status Register 
     * Address: 0x02, Size: 1 byte 
     * Bit layout: [7:3]=Reserved, [2]=OVERRUN, [1]=RX_READY, [0]=TX_READY 
     * Reading this register returns current status and clears some status bits 
     */ 
    register STAT size 1 @ 0x02 is (read) { 
        method read() -> (uint64) { 
            log info: "UART STAT: Reading status register, current value 0x%02x", status; 

            // Save current status value to return to caller 
            ret = status; 

            // Clear specific status bits after reading: 
            // - Clear TX ready bit (0x01) - indicates TX operation acknowledged 
            // - Clear overrun error bit (0x04) - error has been reported 
            // - Keep RX ready bit (0x02) - only cleared when RX data is actually read 
            status &= ~0x05; // Clear TX ready (bit 0) and overrun error (bit 2) after reading 

            log info: "UART STAT: Returning 0x%02x, status cleared to 0x%02x", ret, status; 
            return ret; 
        } 
    } 
} 


/** 
 * External method to inject received data into the UART 
 * This simulates data arriving on the UART RX line from an external source 
 *  
 * @param data: The byte of data to inject into the RX buffer 
 *  
 * Behavior: 
 * - Checks for overrun condition (previous data not yet read) 
 * - Sets overrun error bit if data is overwritten 
 * - Stores new data and sets RX ready status 
 */ 
method inject_rx_data(uint8 data) { 
    // Log the incoming data with current status 
    log info: "UART RX_INJECT: Injecting data 0x%02x ('%c'), current status 0x%02x",  
              data, cast(data >= 32 && data <= 126 ? data : '?', int32), status; 

    // Check if previous data hasn't been read yet (overrun condition) 
    // This happens when new data arrives before software reads the previous data 
    if ((status & 0x02) != 0) { 
        log info: "UART RX_INJECT: Overrun detected! Previous data 0x%02x not read yet", rx_data; 

        // Set overrun error bit (bit 2) to indicate data loss 
        status |= 0x04; // Set overrun error bit (bit 2) 
    } 

    // Store the new received data (overwrites previous if any) 
    rx_data = data; 

    // Set RX ready status bit (bit 1) to indicate data is available for reading 
    status |= 0x02; // Set RX ready status 

    log info: "UART RX_INJECT: Data stored, status updated to 0x%02x", status; 
} 


// Export the inject_rx_data method to make it accessible from Simics CLI 
export inject_rx_data as "inject_rx_data"; 


// Attribute to expose inject_rx_data functionality to Simics CLI 
attribute inject_data is (int64_attr) { 
    param desc = "Inject data into UART RX buffer (write-only)"; 

    method set(attr_value_t value) throws { 
        local uint8 data = SIM_attr_integer(value); 
        inject_rx_data(data); 
        // Don't store the value in val, as this is a write-only operation 
    } 
} 
```

### Key DML 1.4 Features Demonstrated

1. **Device Declaration**: `device uart_core;` - Defines the device class 
2. **Saved Variables**: `saved uint8 status;` - Persistent across save/restore 
3. **Method Definitions**: `method init()` - Device lifecycle methods 
4. **Register Banks**: `bank uart_regs { ... }` - Memory-mapped register groups 
5. **Register Types**: `register TX size 1 @ 0x00 is (write)` - Typed register definitions 
6. **Method Return Types**: `method read() -> (uint64)` - Explicit return type annotations 
7. **Logging**: `log info: "message";` - Built-in logging system 
8. **Type Casting**: `cast(expression, type)` - Explicit type conversions 
9. **Boolean Expressions**: `(status & 0x02) != 0` - Explicit boolean conversion 
10. **Export Declarations**: `export method_name as "external_name";` - Method exposure 
11. **Attributes**: `attribute inject_data is (int64_attr)` - CLI-accessible properties 
12. **Error Handling**: `throws` - Exception handling for attributes 

## 🚀 Development Process

### 📍 Phase 1: Initial Implementation

**Command:** 

```bash
# Navigate to project directory 
cd %SIMICS_PROJECT%\my-intel-simics-project-1 


# Build the module 
./bin/project-setup.bat --device uart_core 
```

**Initial Structure:** 

- Basic DML 1.4 device template 
- Simple register definitions 
- Basic read/write methods 

### Phase 2: Adding Comprehensive Logging

**Requirement:** "Add all log info" for debugging purposes 

**Implementation Strategy:** 

```dml
// Log format: Component: Action details with data 
log info: "UART TX: Writing data 0x%02x ('%c')", val,  
          cast(val >= 32 && val <= 126 ? val : '?', int32); 
```

**Why This Approach?** 

- **Structured logging**: Each log message identifies the component (TX/RX/STAT) 
- **Data visualization**: Shows both hex values and ASCII characters when printable 
- **State tracking**: Logs status changes and transitions 
- **Error detection**: Logs overrun and error conditions 

### Phase 3: Error Resolution and Compilation Fixes

Multiple compilation errors were encountered and resolved systematically. 

### Phase 4: Testing Infrastructure

Created comprehensive test script covering all functionality: 

- Register read/write operations 
- Data injection and retrieval 
- Error condition testing 
- Status bit verification 

### Phase 5: Method Exposure Implementation

Implemented external access to `inject_rx_data` method for testing and integration. 

## 🔧 Error Fixes and Solutions

### 🐛 Error 1: Boolean Condition Compilation Error

**Problem:** 

```dml
// Original problematic code 
if (status & 0x02) {  // Compiler error: expected boolean, got uint8 
```

**Error Message:** 

```
error: [boolean type expected] expected argument of type 'bool', got 'uint8' 
```

**Root Cause:** DML 1.4 requires explicit boolean conversion for conditional statements. 

**Solution:** 

```dml
// Fixed code with explicit boolean comparison 
if ((status & 0x02) != 0) {  // Explicitly compare to 0 for boolean result 
```

**Why This Fixes It:** The `!= 0` comparison returns a boolean type that DML 1.4 accepts in if conditions. 

### Error 2: Format Specifier Warnings

**Problem:** 

```dml
// Original problematic code   
log info: "UART TX: Writing data 0x%02x ('%c')", val, val; 
```

**Warning Message:** 

```
warning: format specifier %c expects type int32, got uint64 
```

**Root Cause:** DML logging expects specific types for format specifiers. `%c` expects `int32` but `val` is `uint64`. 

**Solution:** 

```dml
// Fixed code with explicit casting 
log info: "UART TX: Writing data 0x%02x ('%c')", val,  
          cast(val >= 32 && val <= 126 ? val : '?', int32); 
```

**Why This Works:** 

- `cast()` function explicitly converts types 
- Conditional expression shows printable characters or '?' for non-printable 
- `int32` matches the `%c` format specifier requirement 

### Error 3: Method Exposure Challenge

**Problem:** Need to expose `inject_rx_data` method for external access from Simics CLI. 

**Initial Attempt - Export Declaration:** 

```dml
export inject_rx_data as "inject_rx_data"; 
```

**Issue:** Export declarations alone don't provide CLI interface in DML 1.4. 

**Research Process:** 

1. Searched DML documentation for method exposure patterns 
2. Found attribute-based interface approach 
3. Located `int64_attr` template for numeric attributes 

**Final Solution - Attribute Interface:** 

```dml
// Attribute that wraps the inject_rx_data method 
attribute inject_data is (int64_attr) { 
    param desc = "Inject data into UART RX buffer (write-only)"; 

    method set(attr_value_t value) throws { 
        local uint8 data = SIM_attr_integer(value); 
        inject_rx_data(data); 
        // Don't store value - this is write-only operation 
    } 
} 
```

**Why This Approach?** 

- **CLI Accessible**: Attributes are directly accessible from Simics CLI 
- **Type Safe**: `int64_attr` template handles type conversion 
- **Write-Only**: Perfect for data injection operations 
- **Error Handling**: `throws` declaration handles type conversion errors 

**Usage from Simics CLI:** 

```bash
# Set attribute to inject data 
uart0->inject_data = 0x42 
```

## ⚙️ Building and Testing

### 🛠️ Build Commands

```bash
# Navigate to project root 
cd %SIMICS_PROJECT%\my-intel-simics-project-1 


# Clean previous build (if needed) 
./bin/project-setup.bat --clean-module uart_core 


# Build the UART core module 
./bin/project-setup.bat --build-module uart_core 


# Verify build success 
echo $LASTEXITCODE  # Should be 0 for success 
```

### Testing Commands

```bash
# Run comprehensive test script 
./simics targets/vacuum/uart_core.simics 


# Alternative: Interactive testing 
./simics targets/vacuum/vacuum.simics 
# Then in Simics CLI: 
load-module uart_core 
@SIM_create_object("uart_core", "uart0") 
phys_mem.add-map uart0.bank.uart_regs 0x1000 0x100 priority = 1 
```

### 📋 Expected Output

When running the test script (`uart_core.simics`), you should see output similar to:

```plaintext
Intel® Simics® Simulator 7 (build 7080 win64) © 2025 Intel Corporation

[uart0 info] UART Core: Device initialized
[uart0 info] UART Core: Register layout - TX:0x00, RX:0x01, STAT:0x02
[uart0 info] UART Core: Status bits - TX_READY:0x01, RX_READY:0x02, OVERRUN:0x04

=== Test 1: Initial Status Check ===
[uart0.bank.uart_regs info] UART STAT: Reading status register, current value 0x00
[uart0.bank.uart_regs info] UART STAT: Returning 0x00, status cleared to 0x00

=== Test 2: TX Register Write Test ===
[uart0.bank.uart_regs info] UART TX: Writing data 0xaa ('?')
[uart0.bank.uart_regs info] UART TX: Status updated to 0x01
[uart0.bank.uart_regs info] UART STAT: Reading status register, current value 0x01
[uart0.bank.uart_regs info] UART STAT: Returning 0x01, status cleared to 0x00

=== Test 3: RX Register Read Test (Empty) ===
[uart0.bank.uart_regs info] UART RX: Read attempt, current status 0x00
[uart0.bank.uart_regs info] UART RX: No data available, returning 0

=== Test 4: RX Data Injection Test ===
[uart0 info] UART RX_INJECT: Injecting data 0x42 ('B'), current status 0x00
[uart0 info] UART RX_INJECT: Data stored, status updated to 0x02
[uart0.bank.uart_regs info] UART RX: Returning data 0x42 ('B')
[uart0.bank.uart_regs info] UART RX: Status cleared to 0x00

=== Test 5: Overrun Condition Test ===
[uart0 info] UART RX_INJECT: Injecting data 0x43 ('C'), current status 0x00
[uart0 info] UART RX_INJECT: Data stored, status updated to 0x02
[uart0 info] UART RX_INJECT: Injecting data 0x44 ('D'), current status 0x02
[uart0 info] UART RX_INJECT: Overrun detected! Previous data 0x43 not read yet
[uart0 info] UART RX_INJECT: Data stored, status updated to 0x06

# ... More test output showing successful TX/RX operations ...

=== UART Core Testing Complete ===
All register operations have been tested successfully!
```

The output shows:
- ✅ Device initialization with correct register layout
- ✅ Status register behavior verification
- ✅ TX write operations with status updates
- ✅ RX operations with data injection
- ✅ Overrun detection and handling
- ✅ Comprehensive logging of all operations

### Test Scenarios Covered

1. **Initial Status Check** 
   
   ```bash
   phys_mem.read 0x1002 -b 1  # Should return 0x00 (all clear) 
   ```

2. **TX Register Write Test** 
   
   ```bash
   phys_mem.write 0x1000 0xAA -b 1  # Write data 
   phys_mem.read 0x1002 -b 1        # Check TX_READY status 
   ```

3. **RX Data Injection and Read** 
   
   ```bash
   uart0->inject_data = 0x42        # Inject 'B' 
   phys_mem.read 0x1002 -b 1        # Check RX_READY status   
   phys_mem.read 0x1001 -b 1        # Read injected data 
   ```

4. **Overrun Condition Test** 
   
   ```bash
   uart0->inject_data = 0x43        # First injection 
   uart0->inject_data = 0x44        # Second injection (overrun) 
   phys_mem.read 0x1002 -b 1        # Check OVERRUN bit 
   ```

5. **Multiple Operations Test** 
   
   - Sequential TX writes with status checks 
   - Sequential RX injections and reads 
   - Mixed operations 

## 🔌 Method Exposure Explanation

### 🤔 Why We Need Method Exposure

In real hardware, UART devices receive data from external sources (serial cables, other devices, etc.). In simulation, we need a way to inject data into the RX buffer to test the device behavior. This requires exposing internal methods to external interfaces. 

### The Challenge in DML 1.4

Unlike older DML versions, DML 1.4 doesn't directly expose methods to Simics CLI. We needed a bridge mechanism. 

### Solution Architecture

#### 1. Internal Method (`inject_rx_data`)

```dml
method inject_rx_data(uint8 data) { 
    // Handle overrun detection 
    if ((status & 0x02) != 0) { 
        status |= 0x04; // Set overrun bit 
    } 

    // Store new data and set RX ready 
    rx_data = data; 
    status |= 0x02; 
} 
```

#### 2. Export Declaration (Documentation/Interface)

```dml
export inject_rx_data as "inject_rx_data"; 
```

**Purpose:** Documents the method as part of the device's external interface. 

#### 3. Attribute Wrapper (CLI Access)

```dml
attribute inject_data is (int64_attr) { 
    method set(attr_value_t value) throws { 
        local uint8 data = SIM_attr_integer(value); 
        inject_rx_data(data); 
    } 
} 
```

**Purpose:** Provides CLI-accessible interface that internally calls the method. 

### How It Works

1. **User writes:** `uart0->inject_data = 0x42` 
2. **Simics calls:** `inject_data.set(0x42)` 
3. **Attribute converts:** `0x42` to `uint8` 
4. **Attribute calls:** `inject_rx_data(0x42)` 
5. **Method executes:** Data injection logic 
6. **Result:** RX buffer updated, status bits set 

### Benefits of This Approach

- **Clean Interface**: Simple CLI syntax 
- **Type Safety**: Automatic type conversion and validation 
- **Error Handling**: Built-in error reporting for invalid values 
- **Maintainability**: Clear separation between interface and implementation 
- **Documentation**: Self-documenting through attribute description 

## ⭐ Advanced Features

### 🔍 Overrun Detection

**What is Overrun?** 
Overrun occurs when new data arrives before the previous data has been read by software. This is a common issue in real UART hardware. 

**Implementation:** 

```dml
// Check if previous data hasn't been read 
if ((status & 0x02) != 0) { 
    log info: "UART RX_INJECT: Overrun detected!"; 
    status |= 0x04; // Set overrun error bit 
} 
```

**Testing Overrun:** 

```bash
uart0->inject_data = 0x43  # First data 
uart0->inject_data = 0x44  # Second data (causes overrun) 
phys_mem.read 0x1002 -b 1  # Status shows both RX_READY and OVERRUN 
```

### Status Bit Management

**Smart Status Clearing:** 

- TX_READY: Cleared when status register is read (TX acknowledged) 
- RX_READY: Cleared when RX data is actually read (data consumed) 
- OVERRUN: Cleared when status register is read (error acknowledged) 

```dml
// Status register read method 
status &= ~0x05; // Clear TX_READY(0x01) and OVERRUN(0x04) bits 
// RX_READY(0x02) only cleared when RX register is read 
```

### Comprehensive Logging Strategy

**Log Categories:** 

- **Device Lifecycle**: Initialization, configuration 
- **Register Operations**: All reads and writes with data values 
- **Data Flow**: TX transmissions, RX injections 
- **Error Conditions**: Overruns, invalid operations 
- **Status Changes**: All status bit transitions 

**Log Format Consistency:** 

```
UART <COMPONENT>: <ACTION> <DETAILS> 
```

Examples: 

- `UART TX: Writing data 0x42 ('B')` 
- `UART RX: Overrun detected! Previous data 0x41 not read yet` 
- `UART STAT: Status cleared to 0x00` 

## 📖 Usage Examples

### 📡 Basic TX/RX Operations

```bash
# Load and setup device 
load-module uart_core 
@SIM_create_object("uart_core", "uart0") 
phys_mem.add-map uart0.bank.uart_regs 0x1000 0x100 priority = 1 


# Send "Hello" via TX 
phys_mem.write 0x1000 0x48 -b 1  # 'H' 
phys_mem.write 0x1000 0x65 -b 1  # 'e'   
phys_mem.write 0x1000 0x6C -b 1  # 'l' 
phys_mem.write 0x1000 0x6C -b 1  # 'l' 
phys_mem.write 0x1000 0x6F -b 1  # 'o' 


# Receive "World" via RX 
uart0->inject_data = 0x57  # 'W' 
uart0->inject_data = 0x6F  # 'o'  
uart0->inject_data = 0x72  # 'r' 
uart0->inject_data = 0x6C  # 'l' 
uart0->inject_data = 0x64  # 'd' 


# Read received data 
phys_mem.read 0x1001 -b 1  # Read each character 
```

### Error Testing

```bash
# Test overrun condition 
uart0->inject_data = 0x41        # Inject 'A' 
uart0->inject_data = 0x42        # Inject 'B' (overrun!) 
phys_mem.read 0x1002 -b 1        # Check overrun bit 
phys_mem.read 0x1001 -b 1        # Read latest data ('B') 
```

### Integration with Other Devices

```bash
# Create multiple UART instances 
@SIM_create_object("uart_core", "uart1") 
@SIM_create_object("uart_core", "uart2") 


# Map to different addresses 
phys_mem.add-map uart1.bank.uart_regs 0x2000 0x100 priority = 1 
phys_mem.add-map uart2.bank.uart_regs 0x3000 0x100 priority = 1 


# Use different UARTs 
uart1->inject_data = 0x41  # Send to UART1 
uart2->inject_data = 0x42  # Send to UART2 
```

## ❓ Troubleshooting

### 🚨 Build Issues

**Problem:** Module fails to build 
**Solution:** 

```bash
# Check DML syntax 
./bin/project-setup.bat --check-module uart_core 


# Clean and rebuild 
./bin/project-setup.bat --clean-module uart_core 
./bin/project-setup.bat --build-module uart_core 


# Check for missing dependencies 
ls modules/uart_core/  # Verify all files present 
```

### Runtime Issues

**Problem:** Device not responding 
**Checklist:** 

1. Module loaded: `list-modules` should show `uart_core` 
2. Object created: `list-objects uart_core` should show device 
3. Memory mapped: Check memory map with `phys_mem.info` 
4. Correct addresses: Verify register addresses in memory access 

**Problem:** No logging output 
**Solution:** 

```bash
# Enable appropriate log levels 
log-level info      # Enable info level logging 
log-setup -debug   # Enable debug output 
```

### Common Error Messages

**"No such attribute 'inject_data'"** 

- Cause: Module not properly loaded or object not created 
- Solution: Verify module loading and object creation steps 

**"Memory access failed"** 

- Cause: Incorrect memory mapping or address 
- Solution: Check memory map configuration and addresses 

**"Type conversion error"** 

- Cause: Invalid data passed to inject_data attribute 
- Solution: Use integer values 0-255 for byte data 

### Development Tips

1. **Use Incremental Testing**: Test each feature as you add it 
2. **Enable All Logging**: Use comprehensive logging during development 
3. **Save/Restore Testing**: Test device state persistence 
4. **Error Path Testing**: Always test error conditions 
5. **Documentation**: Keep README updated with any changes 

## 🎯 Conclusion

This UART Core implementation demonstrates: 

- **Modern DML 1.4 Development**: Using current best practices 
- **Comprehensive Error Handling**: Robust device behavior 
- **External Interface Design**: Clean CLI integration 
- **Testing Strategy**: Thorough validation approach 
- **Documentation**: Complete development history 

The project serves as a complete example for new developers learning DML device modeling, showing not just the final solution but the entire development journey including challenges and solutions. 

For questions or improvements, refer to the development process documented above and the comprehensive test suite in `targets/vacuum/uart_core.simics`.
---