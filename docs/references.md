# References

Research and tools actually used or evaluated in this project. See
[`CREDITS.md`](../CREDITS.md) for the submodule/license table.

## Academic / research

- Lisovets, Knichel, Moos, Moradi — *"Let's Take It Offline: Boosting
  Brute-Force Attacks on iPhone's User Authentication through SCA"*, IACR
  Transactions on Cryptographic Hardware and Embedded Systems (TCHES) 2021,
  issue 3, pp. 496–519, Ruhr University Bochum. EM side-channel extraction of
  the UID key on iPhone 4/A4 via the SHAtter bootrom exploit (using ipwndfu);
  the authors state the same procedure applies to iPhone 4s/5/5c using
  checkm8 instead. The only public technique that removes the on-device
  AES-engine speed ceiling entirely — see
  [`results.md`](results.md#what-would-change-the-equation-and-why-it-wasnt-pursued).
  https://eprint.iacr.org/2021/460 (also indexed at
  https://tches.iacr.org/index.php/TCHES/article/view/8984).
- Skorobogatov — NAND mirroring on iPhone 5c, arXiv:1609.04327. The
  technique used in the FBI/iPhone 5c case: physically clone the NAND so the
  retry counter can be reset by reflashing. https://arxiv.org/abs/1609.04327
- CVE-2014-4451 — effaceable-storage race condition (used by IP-Box-style
  tools), patched in iOS 8.1.1. Not applicable to this project's device
  (iOS 10.3.3).

## Tools used directly

- **checkm8 / ipwndfu** (axi0mX) — https://github.com/axi0mX/ipwndfu — the
  bootrom exploit this whole project is built on. See also the alloc8
  writeup: https://github.com/axi0mX/alloc8
- **Legacy iOS Kit** (LukeZGD) — https://github.com/LukeZGD/Legacy-iOS-Kit —
  SSH ramdisk, restore/downgrade tooling.
- **iphone-dataprotection** (nabla-c0d3, originally Jean-Baptiste Bédrune /
  Jean Sigwald) — https://github.com/nabla-c0d3/iphone-dataprotection — base
  for this project's brute-forcer, see `patches/`.
- **systembag.kb** (nt0xa) — https://github.com/nt0xa/systembag.kb — keybag
  parsing.
- **joker** (Jonathan Levin, newosxbook.com) —
  https://newosxbook.com/tools/joker.tar — kernelcache/kext offset lookup,
  used to find `IOCryptoAcceleratorFamily`.
- **bmwalters' 4-digit brute-force binaries and guide** —
  https://gist.github.com/bmwalters/8f3cb4bc212231c4a7474938cae4fbd6 (binaries
  + precompiled/patched kernelcaches) and
  https://gist.github.com/bmwalters/aff476d87dc750f4a7e49357e3c4596b (guide).
  Evaluated and partly used as a starting point before extending to
  alphanumeric wordlist support.
- **MDX-Tom's bruteforce gist** —
  https://gist.github.com/MDX-Tom/b9ac6209d36fce1a652e08e9fab60e61 — confirmed
  the stock Legacy iOS Kit ramdisk (build 13A452) works without a separate
  kernel patch for the numeric-only case.
- **iwannabrute** (platinumstufff) —
  https://github.com/platinumstufff/iwannabrute — evaluated for its
  full-speed (unpatched-kernel) AES engine access approach; macOS-only and
  numeric-only, not adopted, but informative.
- **paroleitaliane** (napolux) —
  https://github.com/napolux/paroleitaliane — base Italian word dictionary
  used to build the targeted wordlist (not published in this repo, see
  [`CREDITS.md`](../CREDITS.md)).
- **SecLists** (danielmiessler) —
  https://github.com/danielmiessler/SecLists — evaluated as an alternative
  English-language credential list.

## Abandoned tooling

- **32bit-SSH-Ramdisk-0.2-Brute** ("SSH Ramdisk_Maker 2.0") — macOS-only
  (`hdiutil`, and Mach-O x86_64 `xpwntool`/`iBoot32Patcher` binaries), never
  ran on Linux. Superseded by Legacy iOS Kit's own SSH ramdisk. See
  [`CREDITS.md`](../CREDITS.md) for details on what it bundles and why it's
  excluded from this repo.

## Commercial forensic tooling (benchmark reference, not used)

- **Elcomsoft iOS Forensic Toolkit** — published figures used throughout
  [`results.md`](results.md) as a benchmark: 13.6 attempts/sec on iPhone
  5/5c-class devices (with escalating time-delay protections disabled), i.e.
  under 12 minutes to exhaust all 4-digit PINs and up to 21 hours for all
  6-digit PINs. Confirmed against
  https://blog.elcomsoft.com/2020/08/behind-the-iphone-5-and-5c-passcode-cracking/
  and product page https://www.elcomsoft.com/eift.html. Alphanumeric passcode
  recovery is not offered by the vendor for this device class.
