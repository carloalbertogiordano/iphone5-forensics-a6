# Workflow: Brute-Force Passcode

## Purpose
Attempt to recover the iOS device passcode by brute-forcing using wordlists, numeric sequences, or specialized dictionaries, leveraging the device's keybag or direct hardware interaction.

## Typical Use Cases
- Recover a forgotten passcode on a device you own.
- Perform a security assessment to evaluate passcode strength.
- Unlock a device for forensic analysis when the passcode is unknown but the device is accessible via exploitation.

## Prerequisites
- A decrypted keybag (see `dump-keybag.md`) or the ability to interact with the device's secure enclave via exploitation tools.
- A wordlist suitable for passcode guessing (e.g., the provided `bruteforce.txt` from the wordlist collection, or custom lists).
- Brute-force capability: either a dedicated binary (e.g., from the `binaries/` directory) or a script that computes PBKDF2 attempts and validates against the keybag.

## Steps
### 1. Prepare the Keybag or Device Access
- **Option A (Offline)**: Obtain the decrypted keybag as described in `dump-keybag.md`. You will need the wrapped class keys, salt, iteration count, and other metadata.
- **Option B (Online)**: Maintain an exploitable connection to the device (e.g., via SSH ramdisk or checkm8_bootkit) to test passcodes directly against the device's Secure Enclave.

### 2. Choose a Brute-Force Method
#### Using the Provided Binaries
- The `binaries/bmwalters-binaries/` directory contains a `bruteforce` binary built for ARMv7 iOS, designed to test passcodes against the device's keybag.
- Copy the binary to the device (e.g., `/mnt2/tmp`) and make it executable:
  ```bash
  scp -P 2222 binaries/bmwalters-binaries/bruteforce root@localhost:/mnt2/tmp/
  ssh -p 2222 root@localhost 'chmod +x /mnt2/tmp/bruteforce'
  ```
- Run the binary with the `-u` flag (important for A5 iOS 9) and optionally specify the wordlist:
  ```bash
  ssh -p 2222 root@localhost '/mnt2/tmp/bruteforce -u < /path/to/wordlist.txt'
  ```
- The binary will iterate through each line in the wordlist, attempt to derive the key, and unwind the class keys; success is indicated by output beyond initial error checking.

#### Using a Custom Script
- If you have the decrypted keybag metadata, you can write a script (Python, etc.) that:
  1. Reads a candidate passcode from a wordlist.
  2. Computes the salt-extended passcode and runs PBKDF2 with the stored iteration count to derive the key.
  3. Attempts to unwrap each class key using the derived key as the UID key.
  4. Validates the unwrapped keys against known constants (e.g., checking for proper decryption of a known key).
- This approach is more flexible and can be run on the host machine.

### 3. Select or Generate a Wordlist
- The `wordlist/paroleitaliane/bruteforce.txt` file is specifically crafted for iOS passcode brute-forcing and includes:
  - All six-digit birthdate combinations (DDMMYY).
  - All six-digit numeric combinations (000000-999999).
  - Italian dictionary words.
  - Profanity and common English terms used in Italy.
  - Frequently observed passwords (e.g., `qwertyuio`).
- Additional wordlists in the same directory (e.g., `60000_parole_italiane.txt`, `lista_badwords.txt`) can be combined or used separately.
- You may also create custom wordlists based on target demographics (e.g., common passwords, dates, names).

### 4. Execute the Brute-Force Attack
- **Online (via device)**: Stream the wordlist to the device-bound brute-force binary.
  ```bash
  cat /path/to/wordlist.txt | ssh -p 2222 root@localhost '/mnt2/tmp/bruteforce -u'
  ```
- **Offline (host-based)**: Run your script against the decrypted keybag, iterating through the wordlist.
- Monitor output for signs of success (e.g., the binary prints progress or a success message; a script can detect when a candidate unwraps all class keys correctly).

### 5. Verify Success
- If the passcode is found, you can:
  - Use it to unlock the device normally.
  - Use it to derive the actual class keys for full decryption of the file system.
  - Use it to verify that the keybag decryption matches expectations.

## Notes
- The `-u` flag is required for certain configurations (especially A5 devices running iOS 9) to ensure proper key derivation.
- Brute-force speed depends on the implementation and hardware; optimized binaries on the device are faster than host-based scripts due to avoiding transfer overhead.
- Consider rate limiting and device defenses: repeated incorrect passcode attempts may introduce delays or trigger data wipe after too many failures (if enabled).
- For numeric-only passcodes (4-6 digits), the `bruteforce.txt` already includes all combinations; for alphanumeric, larger wordlists are needed.
- The wordlist collection also includes verb conjugations and other linguistic data that may be useful for generating passphrase-based guesses.

## References
- Binaries README: `binaries/bmwalters-binaries/README.md`
- Wordlist README: `wordlist/paroleitaliane/README.md`
- Legacy iOS Kit brute-force utilities.
- checkm8_bootkit integration with brute-force (see its README for batch processing).