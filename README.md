<!-- title: iPhone5-forensics-a6 -->
# iPhone5-forensics-a6

A security-research project on a personally-owned, locked iPhone 5 (model
A1429, A6/S5L8950X, no Secure Enclave) whose passcode was forgotten. The goal
was never just "get back into the phone" — iCloud remote erase would have
done that in five minutes. The goal was to see how far a bootrom-exploit-based
recovery chain could actually go on real hardware, end to end, and document
it properly either way.

## What's here

A full exploit-to-brute-force chain built from public research and tooling:
checkm8 bootrom exploit (DFU) → unsigned SSH ramdisk → system keybag
extraction and decryption → a custom on-device brute-forcer calling the
hardware AES engine directly, plus a kernel patch required to unlock that
engine for unprivileged use. Short version, with all the technical detail, in
[`docs/results.md`](docs/results.md).

## Current status

**Not recovered — and that's a documented, legitimate result.** The exploit
chain, keybag extraction, and brute-forcer all work correctly and reach the
same per-attempt speed as commercial forensic tooling (Elcomsoft) for this
device class. The passcode is alphanumeric and wasn't in the ~93k-candidate
targeted wordlist tried; pure brute-force beyond ~5 characters is
computationally out of reach at the achieved speed on any hardware short of
lab-grade side-channel analysis or NAND mirroring — neither available here.
Full numbers and reasoning: [`docs/results.md`](docs/results.md).

A separate attempt to disable the retry-counter/lockout permanently (by
patching SpringBoard itself, not just the on-device brute-force path) hit
Apple's code-signature verification (`amfid`) — no public jailbreak exists for
iOS 10.3.3 on a 32-bit device, so there's no way to make `amfid` accept a
locally-resigned binary. Full postmortem:
[`docs/springboard-patch-attempt.md`](docs/springboard-patch-attempt.md).

## Repo layout

- **Third-party tools** live as git submodules, pinned at the exact commit
  used — see [`CREDITS.md`](CREDITS.md) for every author, license, and what
  (if anything) was modified. Run `git submodule update --init --recursive`
  after cloning.
- **`patches/`** — this project's own modifications to those tools, kept as
  `.diff`s (plus small new files in `patches/<name>-additions/`) instead of
  re-uploading whole repos.
- **`kernel_patch/`** — the kernel patch logic (`do_patch.py`) used to unlock
  `IOAESAccelerator` for unprivileged use. The raw kernelcache itself is never
  published (copyrighted Apple firmware) — see
  [`kernel_patch/README.md`](kernel_patch/README.md).
- **`docs/`** — setup/dependency/troubleshooting guides, per-tool notes, and
  the actual research write-ups ([`results.md`](docs/results.md),
  [`crypto-architecture.md`](docs/crypto-architecture.md),
  [`springboard-patch-attempt.md`](docs/springboard-patch-attempt.md)).
- **Not published** (see [`CREDITS.md`](CREDITS.md) for the full reasoning on
  each): the full device filesystem dump, decrypted key material, personal
  wordlists built from real personal data, and raw kernelcache binaries.

## Reproducing this

See [`docs/getting-started.md`](docs/getting-started.md) for prerequisites and
the overall workflow, and [`docs/tools/`](docs/tools) /
[`docs/workflows/`](docs/workflows) for per-tool and per-task detail.

## License

This project's own original work (patches, docs, scripts) is
[MIT-licensed](LICENSE). Every third-party tool included as a submodule keeps
its own upstream license — see [`CREDITS.md`](CREDITS.md).

## Disclaimer

Educational and research use only. Everything here was run against a device
the author owns. Don't run bootrom exploits, keybag extraction, or passcode
brute-forcing against a device you don't own or don't have explicit
permission to test.

---

*A confession: writing five Markdown files about a bootrom exploit turned out
to be more tedious than actually pulling off the bootrom exploit, so this
documentation was drafted and polished with Claude's help, purely out of
laziness. The DFU timing, the crypto, the kernel patch, the 37-minute
multiplexed brute-force run, the SpringBoard binary staring back at an Apple
logo that refused to boot — all of that is 100% hand-done human work, mistakes
and all.*
