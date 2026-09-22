# Changelog

Dated milestones for this project (dates from terminal timestamps visible in
the original research session).

## 2026-09-10 — Bootrom exploit and initial extraction

- Confirmed target device: iPhone 5, model A1429 (A6/S5L8950X, CPID 0x8950),
  no Secure Enclave.
- `ipwndfu`'s checkm8 exploit (`./ipwndfu -p`) achieved reliably against the
  device in DFU mode (root privileges required — an initial "no langid" pyusb
  error was a permissions issue, not an exploit failure).
- Legacy iOS Kit SSH ramdisk booted successfully for build `13A452`.
- Encrypted data partition dumped (`iphone5_data_enc.img`, 28.6GB) and system
  partition dumped (`iphone5_system.img`).

## 2026-09-11 — Keybag extraction and brute-forcer

- System keybag (`systembag.kb`) extracted and decrypted via `get_bag1` +
  `iphone-dataprotection` tooling.
- `iphone-dataprotection/ramdisk_tools/systemkb_bruteforce.c` cross-compiled
  for armv7s on Linux (Theos toolchain), signed with `ldid`, and run
  successfully against the device from the ramdisk.
- Confirmed the passcode is alphanumeric, not purely numeric — ruled out pure
  numeric brute-force as a fast path.
- Built and ran a targeted Italian wordlist (base dictionary + word+year/word+number
  variants) against the on-device brute-forcer; no match in the initial pass.

## 2026-09-12 — Kernel patch, scaling, retry-counter investigation, conclusion

- Located `IOCryptoAcceleratorFamily` kext offset in the decrypted kernelcache
  using `joker`; built and verified the `IOAESAccelerator`-unlock kernel patch
  (`kernel_patch/do_patch.py`).
- Multiplexed the wordlist brute-force across 4 parallel SSH sessions:
  92,690 candidates in 37 minutes (~42 attempts/sec aggregate) — no match.
- Computed keyspace/time tables for alphanumeric brute-force at the achieved
  speed; concluded pure brute-force is only practical for ≤4-5 character
  passcodes.
- Researched public techniques covering this device/scenario (Elcomsoft EIFT,
  Skorobogatov NAND mirroring, Lisovets et al. IACR TCHES 2021 SCA attack) —
  none applicable without hardware not available for this project.
- Investigated resetting the passcode retry counter: found and automated a
  working `SBDeviceLockFailedAttempts`/`SBDeviceLockBlockTimeIntervalSinceReferenceDate`
  reset via the SpringBoard preferences plist (works per-cycle from the
  ramdisk).
- Located the SpringBoard binary's delay-schedule lookup table
  (`15, 30, 60, 300, 600, 1800, 3600, INT_MAX` seconds) and patched it to
  remove delays; pushing the patched binary broke normal boot (`amfid`
  code-signature enforcement — no valid Apple signature, no jailbreak
  available for this iOS/device combination). Reverted to the original binary.
- Reached the project's conclusion: passcode not software-recoverable with
  available tooling/time; retry-counter cannot be permanently disabled
  without a full jailbreak. Decided to document the project and publish it.
- Original planning conversation exported to PDF for reference.

## 2026-09-13 — 2026-09-14 — Repository preparation

- Audited all vendored/cloned tool directories for licensing and authorship;
  converted them to pinned git submodules with local modifications captured
  as `patches/*.diff` (see [`CREDITS.md`](../CREDITS.md)).
- Identified and excluded sensitive material from publication: the full
  device dump, decrypted key material, personal wordlists (built from
  identifying personal data), and raw/patched Apple kernelcache binaries.
- Resolved provenance of ambiguous binaries (`joker`, `bmwalters-binaries`)
  and dead-end tooling (`32bit-SSH-Ramdisk-0.2-Brute`, a stale pre-rename
  `iHack/` directory copy).
- Wrote this documentation set: `README.md`, `CREDITS.md`, `LICENSE` (MIT for
  original work), and the `docs/` write-ups (`results.md`,
  `crypto-architecture.md`, `springboard-patch-attempt.md`, this changelog,
  and `references.md`).
