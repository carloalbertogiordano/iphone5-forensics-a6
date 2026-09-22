# Legacy iOS Kit

## Purpose
All-in-one toolkit for restoring, downgrading, jailbreaking, and managing legacy iOS devices (32-bit and select 64-bit). Combines numerous utilities, scripts, and patches to support a wide range of operations on devices vulnerable to bootrom exploits (checkm8 and older).

## Key Features
- **Restore/Downgrade**: Restore to signed OTA versions (iOS 8.4.1, 6.1.3, 10.3.3) on supported devices; restore to unsigned versions using SHSH blobs; blobless restoring for certain 32-bit devices via tools like powdersn0w.
- **Jailbreak**: Jailbreak all 32-bit iOS devices on many iOS versions (3.0–9.3.4 with exceptions); includes tethered and untethered methods.
- **SSH Ramdisk**: Boot SSH ramdisk for secure shell access on supported 32-bit and 64-bit devices.
- **SHSH Blob Management**: Save onboard SHSH blobs, extract blobs from Cydia servers, and use blobs for restoring unsigned firmware.
- **Activation & Baseband**: Hacktivation (activate without SIM), baseband flashing and extraction, activation record handling.
- **App & Data Management**: Install IPA files (AppSync), dump apps as IPA, backup/restore data, mount device, erase content.
- **Misc Utilities**: Pair device, export battery info, shutdown/restart, clear NVRAM, ideviceactivation for older iOS.
- **TrollStore Installation**: Install TrollStore via SSH ramdisk on supported 64-bit devices (iOS 14/15).
- **Extensive Tool Integration**: Leverages and forks many open-source projects (ipwndfu, gaster, powdersn0w, De-Rebus-Antiquis-v6, libimobiledevice, futurerestore, etc.) and includes numerous patches and bundles from the community.

## Supported Devices
- **32-bit Devices**: iPhone 2G, 3G, 3GS, 4, 4S, 5, 5C; iPad 1, 2, 3, 4, mini 1; iPod touch 1–5.
- **64-bit Devices (limited)**: iPhone 5S, 6, 6S, SE 2016, 7 (Plus variants); iPad Air 1, 2; iPad mini 2, 3, 4; iPod touch 6, 7.
- **Additional 64-bit with futurerestore**: iPhone 8, X; iPad 5; iPad Pro 9.7/12.9 1st gen (for restoring with SHSH blobs, SSH ramdisk not supported).
- **OTA Downgrade Limitations**: iPhone 5C and iPad mini 3 not supported for OTA downgrades; other restrictions apply per version.

## Supported Host OS
- macOS 10.11+ (12.6+ recommended).
- Ubuntu 22.04+, Fedora 40+, Debian 12+, Arch Linux, and derivatives.
- Other Linux distributions (openSUSE Tumbleweed, Gentoo, Void Linux) less tested but may work.

## Core Tools and Dependencies
The kit integrates or forks the following components:
- **Exploitation**: ipwndfu (checkm8), gaster, primepwn, a6meowing, daibutsuCFW, daibutsu.
- **Blob Handling**: tsschecker, futurerestore (various forks).
- **Device Communication**: libimobiledevice, libirecovery, libideviceactivation, ideviceinstaller, ifuse.
- **SSH Ramdisk**: Based on Ralph0045's SSH-Ramdisk-Maker-and-Loader and msftguy's ssh-rd.
- **Exploit Ramdisks**: Numerous community-provided ramdisks for various exploits and devices.
- **Patch Sources**: Bundle-Creator (Merculous), OdysseusOTA, datautils0, A7 patches, etc.
- **Utilities**: curl, bspatch, jq, zenity, sshpass, darkhttpd, Motrix, usbmuxd2, anisette-server, AltServer-Linux, Plumesign, static-cross-openssh, zip, unzip.
- **Verification**: tsschecker, futurerestore nightly builds.

## Usage
Refer to the official wiki pages for detailed instructions:
- ["How to Use"](https://github.com/LukeZGD/Legacy-iOS-Kit/wiki/How-to-Use)
- ["Restore/Downgrade"](https://github.com/LukeZGD/Legacy-iOS-Kit/wiki/Restore-Downgrade)
- ["Saving SHSH blobs"](https://github.com/LukeZGD/Legacy-iOS-Kit/wiki/Saving-SHSH-blobs)
- ["Jailbreaking"](https://github.com/LukeZGD/Legacy-iOS-Kit/wiki/Jailbreaking)
- ["Troubleshooting"](https://github.com/LukeZGD/Legacy-iOS-Kit/wiki/Troubleshooting)

## Building
Most components are provided as pre-built binaries or scripts; no widespread compilation is required. Specific tools may need make or platform-specific build steps (e.g., ARM toolchain for ipwndfu assembly modifications).

## References
- Original README: `Legacy-IOS-Kit/README.md`
- Wiki: https://github.com/LukeZGD/Legacy-iOS-Kit/wiki
- External links embedded in README for various tools and patches.