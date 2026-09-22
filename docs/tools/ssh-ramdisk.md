# 32-bit SSH Ramdisk

## Purpose
Create and load custom RAM disks to gain SSH access on 32-bit iOS devices (iPhone 5 and similar). The ramdisk provides a minimal environment with SSH server enabled, allowing file transfer and command execution on the device.

## Key Features
- Supports iOS 6.0 through 10.3.4 on 32-bit devices.
- Includes utilities to create, load, and mount the ramdisk.
- Provides SSH access on port 2222 with default password `alpine`.
- Includes patches for macOS SSH host key negotiation issues.

## Core Scripts
- `create.sh`: Builds the ramdisk for a specific device type and iOS version.
- `load.sh`: Loads the prepared ramdisk onto the device via ipwndfu or similar.
- `mount.sh`: Mounts the device's internal partitions after ramdisk boot.
- `tcprelay.sh`: Sets up TCP relay to forward local port 2222 to the device's SSH server.

## Usage
1. **Build the ramdisk**:
   ```bash
   bash create.sh -d [devicetype] -i [iOS version]
   ```
   Replace `[devicetype]` with the device model (e.g., `iPhone5,1`) and `[iOS version]` with a supported version (e.g., `9.0.1`).

2. **Load the ramdisk**:
   Keep the terminal from step 1 open, then run:
   ```bash
   bash load.sh -d [devicetype]
   ```
   This sends the ramdisk to the device in pwned DFU mode.

3. **Establish SSH connection**:
   - Run `./tcprelay.sh` in a separate terminal to forward port 2222.
   - Connect via SSH: `ssh root@localhost -p 2222` (password: `alpine`).

4. **Mount file systems**:
   After SSH login, execute `mount.sh` to mount the device's partitions under `/mnt2`.

## Notes
- For macOS SSH host key mismatches, add `HostKeyAlgorithms=+ssh-rsa` to `~/.ssh/config`.
- The ramdisk includes essential binaries; additional tools can be copied over SSH.
- Ensure the device is in DFU mode before running the exploit/load steps.

## Dependencies
- ipwndfu or similar checkm8 exploitation tool.
- Basic shell utilities (bash, coreutils).
- TCP relay tool (tcprelay.sh included).

## References
- Original README: `32bit-SSH-Ramdisk-0.2-Brute/README.md`