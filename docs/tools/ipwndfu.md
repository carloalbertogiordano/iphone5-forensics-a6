# ipwndfu

## Purpose
Open-source jailbreaking and exploitation tool for many iOS devices, with primary focus on the checkm8 bootrom exploit. Enables SecureROM dumping, keybag decryption, device demotion, and pwned DFU mode access.

## Key Features
- Permanent unpatchable bootrom exploit (checkm8) for hundreds of millions of iOS devices.
- Supports dumping SecureROM, decrypting keybags using GID/UID keys, and demoting devices for JTAG.
- Includes legacy exploits for older devices (alloc8, limera1n, SHAtter, steaks4uce, 24Kpwn).
- Provides pwned DFU mode for USB control.
- Compatible with macOS and Linux (not usable in virtual machines due to USB access).
- No compilation required for basic usage; optional make for assembly modifications.

## Core Functionality
- Exploit device via checkm8 (`./ipwndfu -p`).
- Dump SecureROM (`./ipwndfu --dump-rom`).
- Decrypt keybag (`./ipwndfu --decrypt-gid KEYBAG`).
- Demote device (`./ipwndfu --demote`).
- Additional features: NOR dump/flash, GID/UID encryption/decryption, custom boot logos, verbose boot.

## Dependencies
- libusb (install via package manager: `apt-get install libusb-1.0-0-dev` or `brew install libusb`).
- For assembly modifications: ARM toolchain (binutils, gcc-arm-embedded).
- On macOS with Homebrew: `brew install binutils` and `brew cask install gcc-arm-embedded`.

## Usage
1. Connect device and enter DFU mode.
2. Run exploit: `./ipwndfu -p` (repeat if fails).
3. Dump SecureROM: `./ipwndfu --dump-rom`.
4. Decrypt a keybag: `./ipwndfu --decrypt-gid <hex KBAG>`.
5. Demote for JTAG: `./ipwndfu --demote`.

## Building (Optional)
If modifying assembly source files in `src/`:
```bash
make
```
Requires ARM cross-compilation toolchain.

## References
- Original README: `iHack/ipwndfu/README.md`
- JAILBREAK-GUIDE: https://github.com/axi0mX/ipwndfu/blob/master/JAILBREAK-GUIDE.md
- alloc8 exploit write-up: https://github.com/axi0mX/alloc8