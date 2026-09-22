# gaster

## Purpose
Exploit tool targeting specific iOS devices (particularly A9-based) for gaining low-level control, likely used for bootrom exploitation, payload delivery, or device debugging.

## Key Features
- Provides a Mach-O binary (`gaster`) for host-based exploitation.
- Includes source code (`gaster.c`) and Makefile for building.
- Contains precompiled payloads for various scenarios (e.g., `payload_handle_checkm8_request*.bin` and `.S`).
- Utilizes LZFSE compression (`lzfse.c`, `lzfse.h`) for payload efficiency.
- Supports loading custom ramdisks or bootrom patches.

## Core Components
- `gaster`: Main executable.
- `gaster.c`: Source code.
- `Makefile`: Build instructions.
- Payload binaries and assembly source files (e.g., `payload_handle_checkm8_request.bin`, `payload_notA9.bin`).
- LZFSE compression library (`lzfse.c`, `lzfse.h`).
- Property list (`ent.plist`) possibly for entitlements.

## Usage
Typical usage involves running the gaster binary with appropriate arguments to deliver exploits or payloads to a connected iOS device in DFU or recovery mode. Specific command-line options are not documented in the available README; users should refer to the source code or associated build scripts.

## Building
```bash
make
```
Compiles the gaster binary and links required libraries.

## Dependencies
- Standard C development environment (gcc/clang, make).
- libusb likely required for USB communication (inferred from similar tools).
- No additional external dependencies beyond standard libraries.

## References
- No separate README; information derived from source files and Makefile in `gaster/`.