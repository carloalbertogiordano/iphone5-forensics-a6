# Kernel Patch

`do_patch.py` applies three byte-pattern replacements over a given range of a
decrypted iOS kernelcache:

```
do_patch1: 0x8082f000 -> 0x0135f640
do_patch2: 0xff77f003 -> 0x20402040
do_patch3: 0x68bad370 -> 0x68ba2864
```

Usage: `python do_patch.py <infile> <offset_hex> <length_hex> <outfile>` — patches
every occurrence of the three patterns found within `data[offset:offset+length]`,
leaving the rest of the file untouched.

## What it was for

This was one of the project's attempts (alongside the SpringBoard binary patch
attempt, see the project findings docs) to interfere with the passcode-retry
throttling/counter logic enforced by the kernel, as part of trying to speed up
brute-force recovery. The exact instructions being patched were not fully
reverse-engineered/documented beyond the byte patterns above — treat this as an
experimental patch, not a verified fix. See the project's findings doc for the
overall conclusion (retry-counter reset requires a valid Apple signature, which
this approach does not provide).

The specific `offset_hex`/`length_hex` values used against this project's
kernelcache aren't recorded in the script; if you need exact reproducibility,
document the values you use when you run it.

## Getting your own kernelcache

**Raw and patched kernelcache binaries are intentionally excluded from this repo**
(`.gitignore`) — they are decrypted Apple firmware and redistributing them is a
copyright/DMCA concern, independent of any research use.

To reproduce this locally, extract and decrypt a kernelcache from your own device's
firmware (e.g. via the IPSW for your device/iOS version, decrypted using the
appropriate keys, or dumped live from a jailbroken/exploited device). This project
does not currently have a documented step-by-step extraction workflow — if you
add one, put it under `docs/workflows/`.
