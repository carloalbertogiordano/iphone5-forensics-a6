# Troubleshooting

## Common Issues and Solutions

### SSH Connection Problems
- **Error**: `Unable to negotiate with 127.0.0.1 port 2222: no matching host key type found. Their offer: ssh-rsa,ssh-dss`
  - **Solution**: On macOS 13+, add `HostKeyAlgorithms=+ssh-rsa` to `~/.ssh/config` (see 32-bit SSH ramdisk README).
- **Error**: Connection refused or timeout.
  - **Solutions**:
    - Ensure the TCP relay script (`tcprelay.sh`) is running.
    - Verify the device is connected and trusted.
    - Check that the ramdisk has booted successfully and the SSH server is running.
    - Try a different USB cable or port.
    - Restart the device and re-exploit.

### Exploit Reliability (checkm8/ipwndfu)
- **Issue**: Exploit fails intermittently (`./ipwndfu -p` reports failure).
  - **Solution**: The checkm8 exploit is probabilistic; repeat the command until success. Ensure the device is in proper DFU mode and the cable is reliable.
- **Issue**: Device not entering DFU mode correctly.
  - **Solution**: Follow the exact button timing for your model; use tools like `irecovery` to check state. Some devices may require specific timing variations.

### Ramdisk Creation and Loading
- **Issue**: `create.sh` fails with missing dependencies.
  - **Solution**: Ensure bash and coreutils are installed. The script uses standard Unix tools.
- **Issue**: After loading ramdisk, device shows no screen or hangs.
  - **Solution**: Verify the ramdisk image is not corrupt. Try a different iOS version for the ramdisk (must be compatible with the device). Ensure the device is supported (32-bit for this ramdisk).
- **Issue**: macOS warns about unidentified developer when running binaries.
  - **Solution**: Right-click and choose "Open", or adjust security preferences.

### Data Protection and Keybag Extraction
- **Issue**: `get_bag1` returns no output or errors.
  - **Solution**: Ensure the binary is running on the device with sufficient permissions (may need to be placed in `/usr/local/bin` and executed). Check that the device is jailbroken or exploited to allow access to Effaceable Storage.
- **Issue**: Decrypted keybag appears malformed or parsing fails.
  - **Solution**: Verify the key and IV extracted from `get_bag1` are correct (hex strings, correct length). Ensure the systembag.kb file is complete and not truncated.
- **Issue**: Python scripts complain about missing modules.
  - **Solution**: Install required Python packages (`pycrypto`, `construct`, etc.) as listed in the dependencies.

### Legacy iOS Kit Specific
- **Issue**: Stuck at "Waiting for device" or "Downloading IPSW".
  - **Solution**: Check internet connection; the tool may be attempting to download firmware. Ensure you have legitimate access to download Apple IPSW files.
  - **Solution**: Place required IPSW files manually in the `data/ipsw/` directory to avoid download.
- **Issue**: Error about missing SHSH blobs when trying to restore to unsigned version.
  - **Solution**: Obtain the correct SHSH blobs for your device's ECID and the target iOS version (via saved blobs or online repositories if still available).
- **Issue**: Powersn0w or other blobless restore fails.
  - **Solution**: Ensure the device is supported for blobless restoring (certain 32-bit devices only). Check that the required files are present and the device is in the correct mode.

### cctools-port Build Issues
- **Issue**: `configure` fails complaining about missing TAPI library.
  - **Solution**: Install the TAPI library from https://github.com/tpoechtrager/apple-libtapi and point to it with `--with-libtapi`.
- **Issue**: Link errors about missing libdispatch or libblocksruntime.
  - **Solution**: Install libdispatch-dev and libblocksruntime (or equivalents).
- **Issue**: Build fails on musl-based systems without musl-fts.
  - **Solution**: Install musl-fts from https://github.com/pullmoll/musl-fts.

### Wordlist Regeneration
- **Issue**: `genera_parole_uniche.sh` fails due to missing locale.
  - **Solution**: Ensure the `it_IT.UTF-8` locale is installed on your system. On Ubuntu, run `sudo locale-gen it_IT.UTF-8` and reboot or restart the session.
- **Issue**: ZIP creation fails.
  - **Solution**: Ensure `zip` and `unzip` are installed.

### General Tips
- Always use a reliable USB cable; many issues stem from faulty connections.
- Keep your tools updated; check for newer versions of ipwndfu, Legacy iOS Kit, etc.
- When in doubt, consult the specific tool's README or wiki for detailed troubleshooting sections.
- For device-specific errors, search for the exact error message along with the device model and iOS version.
- If a tool requires root/administrator privileges (e.g., for kernel module loading), run with appropriate permissions.
- Backup important data before attempting exploits or restores that could lead to data loss.

## When to Seek Further Help
- If an error persists after trying the listed solutions.
- If you encounter a crash or panic not documented here.
- For device-specific issues that may require custom patches or timing adjustments.
- Consider opening an issue on the respective tool's GitHub repository with detailed logs and reproduction steps.

## References
- Individual tool READMEs and wiki pages (especially Legacy iOS Kit's Troubleshooting wiki).
- Community forums and issue tracks for specific tools.