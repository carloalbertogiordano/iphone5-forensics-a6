# systembag.kb Tools

## Purpose
Set of utilities to decrypt and parse the systembag.kb file, which contains the device's keybag holding encryption keys for data protection classes.

## Key Features
- Extracts BAG1 key and IV from Effaceable Storage.
- Decrypts systembag.kb using extracted cryptographic material.
- Parses the decrypted keybag to expose key hierarchy, wrappers, and metadata.
- Includes both compiled binaries and Python scripts for flexibility.

## Core Components
- `get_bag1` binary: Extracts bag1 key and iv from the device.
- `decrypt_systembag.py`: Decrypts systembag.kb with given key and IV.
- `parse_keybag.py`: Parses decrypted keybag output.
- Supporting tools: `dpclass`, `emf_decrypter`, `IOKit`, `LockerManager`, `keybag_parser.py`, `ldid2`.
- Data files: example keybags, IV/key texts, XML entitlements.

## Usage
Refer to the DataProtection-noSEP documentation for detailed steps:
1. Run `get_bag1` on the device to obtain key and IV.
2. Use `decrypt_systembag.py` to decrypt the extracted systembag.kb.
3. Parse the result with `parse_keybag.py` to view keybag contents.

## Building
- `make` compiles `get_bag1`.
- Optional code signing step available.
- Other tools have individual build scripts.

## Dependencies
- Python, standard C toolchain.
- libimobiledevice stack (likely).

## References
- README: `systembag.kb/README.md`