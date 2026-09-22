# Workflow: Create a Custom RAM Disk

## Purpose
Create a custom RAM disk to load onto an iOS device, providing a minimal environment with SSH access for forensic analysis or jailbreaking.

## Typical Use Cases
- Prepare a ramdisk for SSH access to extract keybags or file system images.
- Load a ramdisk that includes forensic tools (e.g., data protection utilities).
- Create a ramdisk tailored to a specific device model and iOS version.

## Steps
### 1. Identify Device and iOS Version
- Determine the device model (e.g., `iPhone5,1` for iPhone 5 GSM).
- Choose an iOS version compatible with the device and the ramdisk tool (typically iOS 6.0–10.3.4 for 32-bit devices).

### 2. Obtain RAM Disk Tool
- Use the 32-bit SSH ramdisk tool (`32bit-SSH-Ramdisk-0.2-Brute`) or the ramdisk functionality within Legacy iOS Kit.
- Ensure you have the necessary dependencies (bash, coreutils, ipwndfu or similar for loading).

### 3. Build the Ramdisk
With the 32-bit SSH ramdisk tool:
```bash
bash create.sh -d [devicetype] -i [iOS version]
```
Replace `[devicetype]` and `[iOS version]` accordingly.
The script will generate a disk image (e.g., `ramdisk.dmg`) in the current directory.

### 4. Verify Output
- Check that the ramdisk image file exists and is non-zero size.
- Optionally inspect the contents with `hdiutil attach` (macOS) or `mount` (Linux) to confirm structure.

### 5. Next Step: Load the Ramdisk
Proceed to the workflow for loading the ramdisk onto the device (see `load-ramdisk.md`).

## Notes
- Some ramdisk tools may require additional patches for newer macOS SSH host key agreements.
- Ensure the device is in DFU mode before attempting to load the ramdisk.
- The ramdisk typically includes an SSH server running on port 2222 with default password `alpine`.

## References
- 32-bit SSH Ramdisk README: `32bit-SSH-Ramdisk-0.2-Brute/README.md`
- Legacy iOS Kit SSH ramdisk section: `Legacy-IOS-Kit/README.md` (look for "Boot SSH Ramdisk")