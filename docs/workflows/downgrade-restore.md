# Workflow: Downgrade or Restore iOS Firmware

## Purpose
Downgrade to a signed or unsigned iOS version, or restore to a specific firmware version, using tools like Legacy iOS Kit or the iphone-dataprotection ramdisk approach.

## Typical Use Cases
- Downgrade a device to an older iOS version for jailbreaking or security research.
- Restore a device to a known good state after experimentation.
- Install unsigned firmware using SHSH blobs to bypass Apple's signing window.
- Prepare a device for exploitation by putting it on a vulnerable iOS version.

## Prerequisites
- A compatible iOS device (typically 32-bit or certain 64-bit models) connected via USB.
- Depending on the method:
  - **Legacy iOS Kit**: Requires macOS or Linux with dependencies (libusb, libimobiledevice, etc.), and optionally SHSH blobs for unsigned restores.
  - **iphone-dataprotection**: Requires macOS 10.8/10.9, Xcode with iOS SDK, redsn0w, and the appropriate IPSW files.
- The target IPSW file (iOS firmware) for the desired version, unless using OTA signed versions fetched automatically.
- If restoring to an unsigned version, the corresponding SHSH blobs for that device and iOS version.
- A computer with sufficient disk space for downloading firmware and building ramdisks.

## Steps
### Using Legacy iOS Kit (Recommended for Broad Support)
1. **Prepare the Environment**
   - Install dependencies: libusb, libimobiledevice, libirecovery, ideviceinstaller, etc., via package manager.
   - Ensure git is available to update submodules if needed.
   - On macOS, install Xcode command-line tools.

2. **Clone or Update Legacy iOS Kit**
   ```bash
   git clone https://github.com/LukeZGD/Legacy-iOS-Kit.git
   cd Legacy-iOS-Kit
   # Optionally update submodules
   git submodule update --init --recursive
   ```

3. **Choose the Operation**
   - **Restore to Signed OTA Version**: Use the built-in downloading for iOS 8.4.1, 6.1.3, or 10.3.3 (where applicable).
   - **Restore to Unsigned Version with SHSH Blobs**: Place your SHSH blobs in the appropriate directory (typically `shsh/`).
   - **Blobless Restore (32-bit only)**: Use tools like powdersn0w included in the kit.

4. **Run the Appropriate Command**
   - For guided restoration, follow the interactive prompts or use command-line flags.
   - Example to restore to iOS 10.3.3 on an A7 device (if supported):
     ```bash
     ./legless.sh   # or the specific script for your device/version
     ```
   - Refer to the wiki for specific commands:
     - ["Restore/Downgrade"](https://github.com/LukeZGD/Legacy-iOS-Kit/wiki/Restore-Downgrade)
     - ["Saving SHSH blobs"](https://github.com/LukeZGD/Legacy-iOS-Kit/wiki/Saving-SHSH-blobs)
     - ["Jailbreaking"](https://github.com/LukeZGD/Legacy-iOS-Kit/wiki/Jailbreaking)

5. **Follow On-Screen Instructions**
   - The tool will guide you through putting the device into DFU or recovery mode, downloading necessary components, and flashing the firmware.
   - Monitor progress and address any errors as prompted.

### Using iphone-dataprotection (Alternative for Older Devices)
1. **Set Up the Environment**
   - Install macOS 10.8 or 10.9 with Xcode and iOS SDK.
   - Ensure redsn0w_mac_0.9.15b3 is available (will be downloaded by build.py).
   - Place the appropriate IPSW file in `data/ipsw/` (or let build.py download it).

2. **Build the Custom Ramdisk**
   ```bash
   ./build.py DEVICE_NAME
   ```
   Replace `DEVICE_NAME` with the target model (e.g., `iPhone4,1`).

3. **Exploit and Load the Ramdisk**
   - Run `./boot.py` to launch redsn0w with correct parameters.
   - Put the device into DFU mode when prompted.
   - The script will load the custom ramdisk and patched kernel.

4. **Establish SSH Access**
   - Run `./tcprelay.sh` in a separate terminal.
   - Connect via SSH: `ssh -p 2222 root@localhost` (password: `alpine`).

5. **Perform Desired Actions**
   - With SSH access, you can extract data, install tools, or prepare for further exploitation.

## Notes
- Legacy iOS Kit supports a wider range of devices and operations, including jailbreaking, SHSH blob management, and app/data management.
- iphone-dataprotection is more limited to specific older devices and focuses on creating a forensic ramdisk for SSH access.
- Always verify that the selected iOS version is signable (if not using SHSH blobs) or that you possess valid blobs for the target version.
- The process may involve downloading large firmware files; ensure a stable internet connection.
- After a successful restore, the device will be in the setup assistant screen unless customizations were applied.

## References
- Legacy iOS Kit README: `Legacy-IOS-Kit/README.md`
- Legacy iOS Kit Wiki: https://github.com/LukeZGD/Legacy-iOS-Kit/wiki
- iphone-dataprotection README: `iphone-dataprotection/README.txt`
- External tools integrated: redsn0w, futurerestore, tsschecker, libimobiledevice, etc.