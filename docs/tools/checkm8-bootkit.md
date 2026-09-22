# checkm8_bootkit

## Purpose
Utility to exploit the checkm8 bootrom vulnerability, allowing booting of custom iBoot images, decryption of keybags, and device demotion for JTAG access.

## Key Features
- Supports a wide range of SoCs: S5L8940X (A5), S5L8942X, S5L8945X (A5X), S5L8947X (A5 single-core), S5L8950X (A6), S5L8955X (A6X), S5L8747X, S7002 (S1), T8002, T8004 (S2/T1/S3).
- Can boot raw iBoot/iBSS images.
- Decrypts keybags (KBAG) using derived keys.
- Demotes device to enable JTAG debugging.
- Batch processing of multiple keybags via JSON input.
- Utilizes ipwndfu's custom USB protocol, requiring no modifications to ipwndfu/gaster shellcodes.

## Core Components
- `checkm8_bootkit` binary (built for host and optionally iOS).
- Build system based on Makefile.
- Dependencies: lilirecovery (included as submodule), vmacho (for rebuilding payloads).

## Usage
After building (`make`), the binary supports these verbs:

- `boot <bootloader>`: Boots a raw iBoot/iBSS image.
- `kbag <kbag>`: Decrypts a hex-encoded keybag.
- `demote`: Demotes the device to enable JTAG.
- `batch <input> <output>`: Processes a JSON array of keybag objects, adding decrypted keys.

Example:
```bash
# Boot iBSS
./build/checkm8_bootkit boot /path/to/iBSS.img3

# Decrypt keybag
./build/checkm8_bootkit kabg 0123456789abcdef...

# Demote device
./build/checkm8_bootkit demote

# Batch process keybags
./build/checkm8_bootkit batch input.json output.json
```

## Building
Requirements:
- lilirecovery submodule (already included).
- vmacho (only needed if rebuilding payloads).

```bash
make          # Builds host and iOS versions
make WITH_ARMV7=1   # Also build armv7 iOS version (may be broken with Xcode 16)
```

## Dependencies
- libusb (for USB communication)
- make, gcc/clang
- git (to update submodules)

## References
- Original README: `checkm8_bootkit/README.md`