# Workflow: Dump and Decrypt Keybag

## Purpose
Extract the device's keybag (systembag.kb) and decrypt it to reveal the encryption keys for each data protection class, enabling offline brute-force attacks on the passcode.

## Typical Use Cases
- Obtain the keybag from a locked device to attempt passcode recovery.
- Analyze keybag structure to understand data protection class usage.
- Prepare decrypted keybag for use with tools like checkm8_bootkit or custom scripts.

## Steps
### 1. Gain Access to the Device
- Exploit the device using checkm8 (via ipwndfu or checkm8_bootkit) to achieve pwned DFU mode.
- Optionally load an SSH ramdisk to establish a secure shell connection for easier file transfer.

### 2. Extract the Systembag Keybag
- If you have SSH access:
  ```bash
  scp -P 2222 root@localhost:/private/var/root/Library/Lockdown/systembag.kb ./systembag.kb
  ```
- Alternatively, use tools like `idevicebackup2` or `ifuse` to extract the file from a backup or mounted file system.

### 3. Extract BAG1 Key and IV
- Use the `get_bag1` tool from DataProtection-noSEP:
  - Copy `get_bag1` to the device (e.g., `/usr/local/bin`) and run:
    ```bash
    get_bag1
    iv = <hex string>
    key = <hex string>
    ```
- Save the key and IV for the next step.

### 4. Decrypt the Systembag
- With the extracted keybag (`systembag.kb`), key, and IV, run:
  ```bash
  ./decrypt_systembag.py -k <key> -i <iv> -o decrypted_keybag systembag.kb
  ```
- This produces a decrypted keybag file (`decrypted_keybag`) in binary format.

### 5. Parse the Decrypted Keybag (Optional)
- To inspect the keybag contents:
  ```bash
  ./parse_keybag.py decrypted_keybag
  ```
- Output includes header (version, type, UUID, HMK, salt, iteration count) and details for each protection class (class, wrap type, key type, wrapped key bytes, etc.).

### 6. Use the Decrypted Keybag
- The decrypted keybag contains the class keys wrapped with the device UID key; for offline brute-force, you need to compute the actual class keys by attempting passcodes and computing the key derived from the passcode + salt + iterations, then unwrap the class key.
- Tools like `checkm8_bootkit` can accept a decrypted keybag and attempt passcode brute-force directly.
- Alternatively, feed the wrapped keys and metadata into a custom brute-force script.

## Notes
- The systembag.kb is typically located in `/private/var/root/Library/Lockdown/` on the device.
- Ensure you have extracted the file from a locked state (before passcode entry) to protect the keybag with the user's passcode.
- The keybag uses PBKDF2 with iOS-specific parameters (iteration count often 10000 or 50000) to derive the key from the passcode.
- Some devices may have multiple keybags (e.g., bag1, bag2); the systembag is the primary one.

## References
- DataProtection-noSEP tools: `DataProtection-noSEP/get_bag1`, `DataProtection-noSEP/decrypt_systembag.py`, `DataProtection-noSEP/parse_keybag.py`
- Legacy iOS Kit keybag extraction scripts.
- checkm8_bootkit kbag verb: `checkm8_bootkit/README.md`