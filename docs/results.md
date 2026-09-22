# Results and Conclusions

## Summary

This project set out to recover a forgotten alphanumeric passcode on a
personally-owned iPhone 5 (model A1429, chip A6/S5L8950X, iOS 10.3.3). The A6
has no Secure Enclave, so passcode retry throttling (increasing delay, wipe
after 10 attempts) is enforced entirely in software — which is what makes a
bootrom-exploit-based attack theoretically viable on this device at all.

The full attack chain was built and executed successfully end to end. The
conclusion is a legitimate negative result: **the passcode is not
software-recoverable with the hardware and time budget available**, and the
retry counter cannot be permanently disabled without a valid Apple code-signing
certificate. This document explains why, with the numbers behind it.

## What was built and what worked

1. **Bootrom code execution**: `ipwndfu`'s checkm8 exploit (`./ipwndfu -p`)
   against the A6 SecureROM via DFU. Reliable once running as root (an early
   `ValueError: The device has no langid` from pyusb turned out to be a
   permission issue, not an exploit failure — checkm8 itself is well-documented
   as probabilistic and simply needs retrying on failure).
2. **Unsigned ramdisk boot**: Legacy iOS Kit's SSH ramdisk (`./restore.sh
   --sshrd`), built for the device's exact build (`13A452`). This boots a
   minimal, unsigned userland where `amfid`/code-signature enforcement is not
   active — the reason later steps (custom brute-force binaries) can run at
   all without a real Apple signing certificate.
3. **Keybag extraction**: `get_bag1` (from `iphone-dataprotection`'s
   `ramdisk_tools/`) reads the `BAG1` locker out of Effaceable Storage and
   returns the key/IV needed to decrypt `systembag.kb`, the system keybag.
   `systembag.kb`'s own `keybag.py`/`parse_keybag.py` (patched in this project,
   see [`CREDITS.md`](../CREDITS.md)) then parse the per-class wrapped keys.
   See [`crypto-architecture.md`](crypto-architecture.md) for the format.
4. **On-device brute-forcer**: `iphone-dataprotection`'s
   `ramdisk_tools/systemkb_bruteforce.c`, modified in this project (see
   `patches/iphone-dataprotection.diff`) to read candidate passcodes from a
   wordlist file instead of prompting interactively, and to stop cleanly on a
   match instead of writing a results plist. For each candidate it calls
   `IOAESAccelerator` with the passcode-derived key (via `AppleKeyStore`) to
   attempt the class-key unwrap — the actual cryptographic engine is the same
   hardware AES block that holds the UID key, and the UID key itself is never
   read out.
5. **Kernel patch**: `IOAESAccelerator` refuses unprivileged callers unless
   the kernel is patched (unpatched, calls return `e00002c1`). `kernel_patch/do_patch.py`
   applies three byte-pattern replacements to a decrypted kernelcache to lift
   this restriction (see [`kernel_patch/README.md`](../kernel_patch/README.md)).
   `joker` (see [`CREDITS.md`](../CREDITS.md)) was used to locate the
   `IOCryptoAcceleratorFamily` kext offset needed to build/verify the patch.

## Speed: matching and confirming the known baseline

With the kernel patch active, a single brute-force instance ran at **~13
attempts/second** — matching Elcomsoft iOS Forensic Toolkit's own published
number for this exact class of device (13.6 attempts/sec, PBKDF2-derivation-bound
once rate limiting is removed). This is a useful sanity check: it confirms the
approach here reaches the same hardware-imposed ceiling as the commercial tool,
not something worse.

Because the AES engine is one shared hardware unit, running multiple
brute-force processes in parallel does not increase total throughput — but it
does reduce *expected* wait time by covering different sections of a wordlist
concurrently. A combined Italian wordlist (base dictionary + word+year and
word+number variants, 92,690 candidates) run as 4 parallel instances over 4
file splits finished in 37 minutes — **~42 attempts/second aggregate**. No
match was found in that list.

## Why alphanumeric brute-force is infeasible here

At the measured ~42 attempts/sec:

| Charset | Length | Keyspace | Time |
|---|---|---|---|
| digits only | 4 | 10,000 | ~4 min |
| digits only | 6 | 1,000,000 | ~6.6 hours |
| digits only | 8 | 100,000,000 | ~27 days |
| lowercase (26) | 4 | 457k | ~3 hours |
| lowercase (26) | 5 | 11.9M | ~3.3 days |
| lowercase (26) | 6 | 309M | ~85 days |
| lowercase (26) | 7 | 8B | ~6 years |
| upper+lower (52) | 4 | 7.3M | ~2 days |
| upper+lower (52) | 5 | 380M | ~104 days |
| upper+lower (52) | 6 | 19.7B | ~15 years |
| upper+lower+digits (62) | 4 | 14.8M | ~4 days |
| upper+lower+digits (62) | 5 | 916M | ~8 months |
| upper+lower+digits (62) | 6+ | — | decades |

Pure brute-force is only practical for lengths **≤4-5 characters** at this
speed — beyond that the search space grows faster than any realistic time
budget, regardless of parallelism (the shared AES engine is the hard ceiling,
not I/O or software overhead). A dictionary/context-based attack (the 92k
wordlist above) is the only approach that scales past that — and it requires
knowing or guessing something about the real passcode.

## What would change the equation (and why it wasn't pursued)

- **EM side-channel analysis** (Lisovets, Knichel, Moos, Moradi — *"Let's Take
  It Offline: Boosting Brute-Force Attacks on iPhone's User Authentication
  through SCA"*, IACR TCHES 2021, Ruhr University Bochum): extracts the UID
  key itself via power/EM analysis on the AES engine (demonstrated on iPhone 4/A4,
  explicitly stated by the authors to apply to iPhone 5/5c via checkm8 instead
  of SHAtter). Once the UID key is known, brute-force moves entirely offline
  onto a GPU — ~380x faster than on-device. This is the only publicly
  documented technique that removes the on-device speed ceiling entirely. It
  requires lab-grade oscilloscope/CPA equipment and a multi-week acquisition;
  not available for this project, and no open-source A6-specific replication
  exists to build on.
- **NAND mirroring** (Skorobogatov, arXiv 1609.04327, the technique used in
  the FBI/iPhone 5c case): physically desolders/clones the NAND so the retry
  counter can be reset by reflashing the original image whenever it approaches
  the wipe threshold. This removes the *attempt-count* limit but **not** the
  per-attempt AES-engine speed limit — it would make the digit-only rows above
  free to run to completion, but does nothing for the alphanumeric rows. Not
  pursued here: it needs desoldering/hardware equipment and time investment
  disproportionate to the (still capped) benefit for an alphanumeric passcode.
- **CVE-2014-4451** (effaceable-storage race condition, used by IP-Box-style
  tools): patched in iOS 8.1.1. This device runs 10.3.3 — not applicable.
- **Full jailbreak**: Legacy iOS Kit's jailbreak support for 32-bit devices
  covers iOS 3.0–9.3.4 only. iOS 10.3.3 on a 32-bit device has no public
  jailbreak (10.x jailbreaks only ever targeted 64-bit devices). See
  [`springboard-patch-attempt.md`](springboard-patch-attempt.md) for what this
  blocks.

## Conclusion

The exploit chain, keybag extraction, and on-device brute-forcer all work
correctly and reach the same per-attempt speed as commercial forensic tooling
for this device class. The passcode was not recovered because it is
alphanumeric and not present in the ~93k-candidate targeted wordlist tried —
and pure brute-force beyond ~5 characters is computationally out of reach at
the achieved speed, on any hardware short of the SCA or NAND-mirroring
approaches above. The retry-counter/lockout mechanism was separately
investigated for manual-guess attempts; see
[`springboard-patch-attempt.md`](springboard-patch-attempt.md) for why a
permanent bypass isn't possible without a full jailbreak (unavailable for this
iOS/device combination).

This is where the software-only research path ends for this device and
passcode. The device, the full data dump, and the decrypted keybag are kept —
if the passcode is ever recalled, or a new public technique emerges, recovery
can resume from where this project left off.
