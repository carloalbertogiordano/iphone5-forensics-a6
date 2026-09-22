# Retry-Counter / SpringBoard Patch Attempt (Postmortem)

This documents a separate line of investigation from the main brute-force
described in [`results.md`](results.md): whether the passcode retry
lockout/wipe counter could be reset or disabled **from within normal iOS**
(not the ramdisk-side `IOAESAccelerator` brute-forcer, which never goes
through SpringBoard or the lock-screen UI at all and so isn't subject to this
counter). The motivation was to allow unlimited *manual* passcode-guess
attempts through the actual lock screen — useful for muscle-memory/recall
attempts by hand, and for typing a handful of high-confidence dictionary
guesses without risking the 10-attempt wipe.

## What was found

The counter and lockout state live in an ordinary preferences plist,
`/private/var/mobile/Library/Preferences/com.apple.springboard.plist`
(readable/writable from the ramdisk at `/mnt2/mobile/Library/Preferences/`,
since that partition mounts unencrypted-at-the-filesystem-level once the
class keys are available — see [`crypto-architecture.md`](crypto-architecture.md)).
Relevant keys observed:

```
SBDeviceLockFailedAttempts                       : 8      (or 10 once fully locked out)
SBDeviceLockBlockStateGeneration                 : 183790
SBDeviceLockBlockTimeIntervalSinceReferenceDate  : 552747319.241306   (Apple reference-date timestamp to wait until)
```

A short Python script (`reset.py`, using `plistlib`) downloads this plist via
`scp`, zeroes `SBDeviceLockFailedAttempts`/`SBDeviceLockBlockStateGeneration`,
removes the `BlockTimeIntervalSinceReferenceDate` key entirely, and pushes it
back. **This works** — verified across multiple reboot cycles, the counter and
lockout timer both reset. The catch: SpringBoard rewrites this file on every
failed attempt, so the reset has to be re-applied from the ramdisk each time
the count approaches 10. It gives roughly 9 usable manual attempts per
ramdisk cycle — workable for a short, high-confidence guess list, not a
brute-force substitute.

Reverse-engineering the actual delay schedule (not just resetting the
counter, but removing the escalating wait entirely) led to the SpringBoard
binary itself. A lookup table was found at offset `0x00695c60` in
`/mnt1/System/Library/CoreServices/SpringBoard.app/SpringBoard`:

```
15, 30, 60, 300, 600, 1800, 3600, 2147483647   (seconds; last value is INT_MAX — permanent lockout)
```

This is the delay-per-attempt-count schedule. All eight values were patched
to `1` (near-instant) and the binary was pushed back to `/mnt1` (the *system*
partition, `disk0s1s1` — unlike `/mnt2`'s user data partition, this one is
read-only-by-default but not passcode-encrypted, since it only carries
EMF!-volume-level encryption that's already transparent inside the ramdisk;
this is why the SpringBoard binary itself was readable/writable at all).

## Why it failed

Rebooting normally after pushing the patched `SpringBoard` binary **hung on
the Apple logo** — boot never completed. Restoring the original binary fixed
it immediately, confirming the patched binary itself was the cause, not
something else.

The reason: **`amfid` (Apple Mobile File Integrity Daemon)** verifies that
every executable's code signature matches a certificate Apple trusts before
letting it run, at every normal boot — not just for security-sensitive
binaries, all of them, including SpringBoard. Modifying even a single byte
invalidates the original Apple signature embedded in the binary. Re-signing
with `ldid` (used successfully earlier to get the brute-force binary running
*inside the ramdisk*) doesn't help here: `ldid` signs with a locally-generated
key, and `amfid` in normal boot mode specifically checks for an **Apple**
certificate, not just "a valid signature of some kind." The brute-force
binary never hit this check because it only ever ran from the ramdisk, where
`amfid` enforcement is off entirely (the ramdisk environment is unsigned by
design — that's what makes booting it in the first place a bootrom exploit
in the first place). SpringBoard, by contrast, runs as part of the normal
signed-boot chain, where `amfid` is very much active.

Fixing this properly — patching `amfid` itself to accept unsigned/locally-signed
binaries — is exactly what a jailbreak does. And there is no public jailbreak
for iOS 10.3.3 on a 32-bit device: Legacy iOS Kit's own 32-bit jailbreak
support tops out at iOS 9.3.4, and the public iOS 10 jailbreaks (Yalu,
Meridian) only ever targeted 64-bit devices, since Apple dropped 32-bit
support entirely with iOS 11 and the jailbreak community had no reason to
backport further. This is a hard wall for this exact iOS/device combination,
not a bug in the approach.

## Net result

- **Retry-counter reset via plist**: works, but per-cycle (must be redone
  from the ramdisk each time), giving ~9 manual attempts per cycle.
- **Permanent delay/lockout removal via SpringBoard binary patch**: not
  possible without a full jailbreak (unavailable for this iOS/device
  combination), because it requires bypassing `amfid`'s Apple-certificate
  check at normal boot, which `ldid`-style local re-signing cannot satisfy.
- A parallel attempt to find a *hardware-level* (Effaceable Storage) retry
  counter, as opposed to this software/plist one, hit a code-signing
  entitlement wall of its own — see the note in
  [`crypto-architecture.md`](crypto-architecture.md#effaceable-storage-and-bag1).

None of this affects the core on-device brute-forcer's applicability, since
that path never goes through SpringBoard or the retry counter at all — see
[`results.md`](results.md) for why the actual blocker is search-space size,
not attempt-count throttling.
