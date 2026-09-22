# iPhone5-forensics-a6

This repository aggregates various open-source tools and scripts for forensic analysis and security research on iPhone 5 (and other legacy iOS devices). The collection includes utilities for creating custom RAM disks, exploiting the checkm8 bootrom vulnerability, decrypting keybags, brute-forcing passcodes, and extracting device data.

The tools are intended for security researchers, digital forensics examiners, and developers working on iOS security assessments. They support a range of iOS versions and device models, focusing on devices vulnerable to bootrom exploits (checkm8 and earlier).

## Contents

Third-party tools live as git submodules (see [`CREDITS.md`](../CREDITS.md) for
authors/licenses/what was modified) — run `git submodule update --init --recursive`
after cloning to fetch them.

- **checkm8_bootkit**: utility to boot iBoot, decrypt keybags, and demote devices via checkm8.
- **DataProtection-noSEP**: tools to decrypt and parse `systembag.kb` and related data protection files.
- **gaster**: checkm8-family exploit tool.
- **ipwndfu**: open-source checkm8 bootrom exploit / DFU jailbreaking tool.
- **Legacy iOS Kit**: all-in-one tool for restoring, downgrading, and running an SSH ramdisk on legacy iOS devices.
- **systembag.kb**: tools to decrypt and parse the `systembag.kb` file.
- **cctools-port**: port of Apple's cctools/ld64 for building toolchains on Linux.
- **xnu**: the XNU kernel source, for reference.
- **iphone-dataprotection**: iOS data protection research tools — this project's brute-forcer is built on top of it (see `patches/`).
- **kernel_patch**: `do_patch.py`, the byte-level kernel patch used before brute-forcing (raw kernelcache itself is never published — copyrighted Apple firmware — see `kernel_patch/README.md`).
- **patches/**: this project's own modifications/additions to the submodules above, kept as diffs instead of re-uploading whole repos.
- **docs/**: this documentation, plus the findings/crypto/bruteforce write-ups.

Not published in this repo (see [`CREDITS.md`](../CREDITS.md) for why): the full
device filesystem dump, decrypted key material, personal wordlists, and raw
kernelcache binaries.

## Motivation

The tools in this repository enable security professionals to conduct controlled security research, forensic data acquisition, and vulnerability analysis on iOS devices. By providing a unified collection of scripts, binaries, and documentation, researchers can streamline their workflows for device exploitation, data extraction, and security assessment.

## Disclaimer

These tools are provided for educational and research purposes only. Use them only on devices you own or have explicit permission to test. The authors assume no liability for any damage, data loss, or legal consequences resulting from misuse.

## A note on the docs

Reverse-engineering a bootrom exploit chain turned out to be less exhausting than writing five Markdown files about it — so this documentation was drafted and polished with the help of Claude (Anthropic), because pure human laziness is also a valid engineering constraint. All the actual research, exploitation, and code is 100% human-made (mistakes included).