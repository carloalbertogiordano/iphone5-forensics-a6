# DataProtection-noSEP

## Purpose
Collection of tools to decrypt and parse the systembag.kb file and related iOS data protection records, enabling extraction of encryption keys from the device's Effaceable Storage without requiring the Secure Enclave Processor (SEP).

## Key Features
- Extracts BAG1 key and initialization vector (IV) from Effaceable Storage via `get_bag1` binary.
- Decrypts `systembag.kb` using the extracted key and IV with `decrypt_systembag.py`.
- Parses decrypted keybag to reveal class keys, wrappers, and metadata via `parse_keybag.py`.
- Includes auxiliary tools for keybag parsing, encryption operations, and device interaction.
- Based on the original iphone-dataprotection project.

## Core Components
- `get_bag1`: Built binary to extract bag1 key and iv from the device.
- `decrypt_systembag.py`: Python script to decrypt systembag.kb.
- `parse_keybag.py`: Python script to parse the decrypted keybag.
- Auxiliary tools: `dpclass`, `emf_decrypter`, `IOKit`, `LockerManager`, `keybag_parser.py`, `ldid2`.
- Configuration and key files: `bag1iv.txt`, `bag1k.txt`, `dkey.txt`, `lwvmk.txt`, `outkbag`, `systembag.kb`, `tfpent.xml`, `volumeoffset.txt`.
- Source code for various utilities (e.g., `AppleEffaceableStorage.c`, `dpclass.c`, `IOKit.c`, `LockerManager.c`).
- Scripts for compilation and code signing: `compile-emfd.sh`, `compile-sign.sh`.

## Usage
1. **Extract bag1 key and iv**:
   - Copy `get_bag1` to the device (e.g., `/usr/local/bin`) and execute:
     ```bash
     get_bag1
     iv = <hex>
     key = <hex>
     ```
2. **Decrypt systembag.kb**:
   - Retrieve `systembag.kb` from the device.
   - Run:
     ```bash
     ./decrypt_systembag.py -k <key> -i <iv> -o output_keybag systembag.kb
     ```
3. **Parse the keybag**:
   - Run:
     ```bash
     ./parse_keybag.py output_keybag
     ```
   - Output includes header details (version, type, UUID, HMK, salt, iteration count) and key entries for each protection class.

## Building
- For `get_bag1`: Run `make` in the repository root; optional codesign step with `CER="<certificate>" make codesign`.
- Other tools include their own build scripts (e.g., `compile-emfd.sh`, `compile-sign.sh`).

## Dependencies
- Python 2.x or 3.x (for parsing scripts).
- Standard C compiler and build tools.
- libimobiledevice, libirecovery, libideviceactivation (inferred from related projects).
- OpenSSL for cryptographic operations.

## References
- Original README.txt (not present; information gathered from source files and scripts).
- Related projects: iphone-dataprotection, Legacy iOS Kit.
- External references:
  - iPhone data protection in depth: http://esec-lab.sogeti.com/static/publications/11-hitbamsterdam-iphonedataprotection.pdf
  - A (not-so-quick) Primer on iOS Encryption: https://darthnull.org/media/presentations/2016-BSidesROC-iOSCrypto.pdf