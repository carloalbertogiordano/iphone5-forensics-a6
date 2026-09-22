# Credits

All third-party tools used in this project are tracked as git submodules, pinned at
the exact commit used, rather than vendored copies. Run
`git submodule update --init --recursive` after cloning to fetch them.

Where this project modified a submodule's files, the change is kept as a `.diff` in
`patches/` (applies cleanly on top of the pinned commit) instead of re-uploading the
whole tool. Small new files added on top of a submodule live in
`patches/<name>-additions/`.

| Submodule | Author/Org | Upstream | License | Local changes |
|---|---|---|---|---|
| `cctools-port` | tpoechtrager | https://github.com/tpoechtrager/cctools-port | No LICENSE file found upstream as of 2026-09 | none |
| `checkm8_bootkit` | NyanSatan | https://github.com/NyanSatan/checkm8_bootkit | No LICENSE file found upstream as of 2026-09 | none |
| `DataProtection-noSEP` | TurtleARM | https://github.com/TurtleARM/DataProtection-noSEP | No LICENSE file found upstream as of 2026-09 | none |
| `gaster` | 0x7ff | https://github.com/0x7ff/gaster | Apache License 2.0 | none |
| `iphone-dataprotection` | nabla-c0d3 (originally Jean-Baptiste Bédrune / Jean Sigwald) | https://github.com/nabla-c0d3/iphone-dataprotection | No LICENSE file found upstream as of 2026-09 | `patches/iphone-dataprotection.diff` (modified `ramdisk_tools/systemkb_bruteforce.c`, `ramdisk_tools/util.c`); `patches/iphone-dataprotection-additions/dump_eff.c` (new tool: dumps raw effaceable storage via `AppleEffaceableStorage__getBytes`) |
| `ipwndfu` | axi0mX / cfw-project | https://github.com/cfw-project/ipwndfu | GNU GPLv3 | `patches/ipwndfu.diff` (trivial: `#!/usr/bin/python` -> `#!/usr/bin/env python` shebang fix) |
| `ldid` | ProcursusTeam | https://github.com/ProcursusTeam/ldid | No LICENSE file found upstream as of 2026-09 | none (a locally compiled `ldid_linux_x86_64` binary exists in the working tree but is a build artifact, not published) |
| `Legacy-IOS-Kit` | LukeZGD | https://github.com/LukeZGD/Legacy-iOS-Kit | GNU GPLv3 | none tracked in the submodule itself; `patches/legacy-ios-kit-additions/` adds `joker.ELF64`/`joker.universal` (third-party tool, not part of this project — see **joker** below) |
| `systembag.kb` | nt0xa | https://github.com/nt0xa/systembag.kb | No LICENSE file found upstream as of 2026-09 | `patches/systembag.kb.diff` (modified `keybag.py`, `parse_keybag.py`); `patches/systembag.kb-additions/parse_tlv.py` (new tool: generic TLV keybag structure dumper) |
| `xnu` | Apple (apple-oss-distributions) | https://github.com/apple-oss-distributions/xnu | Apple Public Source License (`xnu/APPLE_LICENSE`) | none |
| `binaries/bmwalters-binaries` | bmwalters | https://gist.github.com/bmwalters/8f3cb4bc212231c4a7474938cae4fbd6 | No LICENSE, freely shared gist | none — vendors bmwalters' own precompiled armv7 `bruteforce`/`hello` binaries and several **decrypted, AES-accelerator-UID-patched kernelcaches** (iPhone4,1 / iPhone5,1 / iPhone5,2 / iPod5,1) for the *4-digit* on-device passcode brute-force method; kept as a submodule (pointer only) rather than vendored so this repo never re-hosts the Apple kernelcache bytes itself — they stay hosted in bmwalters' own gist |

## joker

Third-party kernelcache/kext inspection tool by Jonathan Levin, downloaded from
https://newosxbook.com/tools/joker.tar (no formal license, freely distributed
by the author for research use). Used to locate the `IOCryptoAcceleratorFamily`
kext offset inside the decrypted kernelcache — a prerequisite for the kernel
patch in `kernel_patch/README.md`. Vendored as-is (binary, no source available)
in `patches/legacy-ios-kit-additions/`, since it isn't part of Legacy-IOS-Kit's
own upstream history. See that folder's `README.md` for how to place it.

## Wordlist base dictionary

The Italian base dictionary used for generating candidate passwords was sourced from
[napolux/paroleitaliane](https://github.com/napolux/paroleitaliane) (no LICENSE file
found upstream; author notes some included lists are of unknown/recovered
provenance). The generated wordlists themselves are **not** published in this repo —
see `wordlist/README.md`.

## Resolved (checked against the original planning chat, 2026-09-14)

- **`iHack/ipwndfu`**: NOT a second experiment branch. `~/Code/iHack` was this
  project's original directory name before it was renamed/moved to
  `~/Code/iHack2` early in the session (the chat log shows `~/Code/iHack/ipwndfu`
  only in the very first troubleshooting exchange, then every later path is
  under `~/Code/iHack2/...`). It's a stale pre-rename copy, fully superseded by
  the top-level `ipwndfu/` submodule. Stays out of the repo (`.gitignore`'d
  `/iHack/`); safe to delete locally whenever, no merge needed.
- **`32bit-SSH-Ramdisk-0.2-Brute/`**: confirmed abandoned. This is "SSH
  Ramdisk_Maker 2.0", tried early on to build a custom SSH ramdisk with kernel
  patch support, but its `create.sh` depends on macOS-only `hdiutil` plus
  Mach-O x86_64 macOS binaries (`xpwntool`, `iBoot32Patcher`) in `bin/` — none
  of it runs on Linux/Fedora. The session explicitly dropped it ("non ha senso
  inseguire questa strada su Fedora") in favor of Legacy-IOS-Kit's own built-in
  SSH ramdisk, which was already working, plus `joker` (see above) for the
  kernel patch and bmwalters' precompiled `bruteforce` binary for the actual
  brute-force. It bundles **real Apple-signed iBSS firmware blobs**
  (`resources/iBSS/*.bin`, one per device: iPhone5/5c, iPad3, iPad4) plus
  compiled macOS x86_64 tool binaries — stays wholesale excluded via
  `.gitignore` (dead-end tooling, never produced anything used in the final
  pipeline; the iBSS blobs must never be redistributed regardless of origin).
- **`Legacy-IOS-Kit/joker`, `joker.ELF64`, `joker.universal`**: resolved, see
  **joker** section above — public tool from newosxbook.com, not a mystery
  binary. Now vendored in `patches/legacy-ios-kit-additions/`.
- **`binaries/bmwalters-binaries/`**: resolved, see submodule table above —
  it's bmwalters' own git-backed gist, now tracked as a submodule (pointer
  only, no re-hosting of the decrypted kernelcaches it contains).

## Still open

- **`cctools-port/apple-libdispatch`, `apple-libtapi`**: not registered as
  upstream submodules of `cctools-port` (no `.gitmodules` there) — manually
  cloned build dependencies, both from the same author (tpoechtrager):
  https://github.com/tpoechtrager/apple-libdispatch and
  https://github.com/tpoechtrager/apple-libtapi. Nested git repos, so git
  won't pull their contents into this repo automatically; if `cctools-port`
  needs them to build, document cloning them separately rather than vendoring.
  No action needed otherwise.
- **`IOCryptoAcceleratorFamily.bin`** (repo root): an extracted Apple kext
  binary (armv7s), same copyright class as the kernelcache. Excluded via
  `.gitignore`, no further action needed.
- **`binaries/bruteforce`, `binaries/device_infos`, `binaries/restored_external`,
  `binaries/lzssdec`**: loose compiled binaries at the root of `binaries/`,
  predating (timestamped Jan 2025 / Dec 2021, vs this session's Sept 2026 work)
  or duplicating already-credited source. `device_infos`/`restored_external`
  are just compiled output of `iphone-dataprotection/ramdisk_tools/{device_infos,restored_external}.c`,
  already covered by that submodule — no separate credit needed. `bruteforce`
  and `lzssdec` have no traceable source in this project's chat history.
  Excluded via `.gitignore`; if they turn out to matter, re-derive them from
  their real source instead of publishing the loose binaries.
