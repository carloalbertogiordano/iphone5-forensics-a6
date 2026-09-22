# iOS Data Protection Crypto (as relevant to this device)

This is the technical background for how [`results.md`](results.md)'s attack
chain actually works at the byte level, specific to a pre-A7 device (no Secure
Enclave) on iOS 10.3.3.

## The UID key

Every iOS device has a 256-bit UID key fused into the SoC at manufacturing.
It's wired directly into the hardware AES engine (`IOAESAccelerator`/
`AppleKeyStore` on pre-A7 devices) — software can *select* it as the active
key for an AES operation, but there is no instruction or register that reads
its value out. This is true whether or not the device has a Secure Enclave;
the difference the SEP introduces (from the A7 onward) is *where* the
passcode-delay/retry-counter enforcement lives, not whether the UID key is
extractable. On the A6 that enforcement is ordinary software, which is the
whole reason this project's approach (bootrom exploit → own code → call the
same hardware AES engine the OS would've called) is viable at all.

Every passcode candidate is combined with this hardware-bound key via
`AppleKeyStore_unlockKeybagFromUserland`, which is what
`ramdisk_tools/systemkb_bruteforce.c` calls per candidate — so brute-force
speed is capped by the AES engine's throughput, not by anything CPU-bound.
The single-instance rate measured here (~13 attempts/sec) is set by
this hardware cycle, not the C code.

## Effaceable Storage and BAG1

Effaceable Storage is a small, separately-addressable NOR flash region used
for anything that needs to be instantly and cryptographically "shredded"
(wiped) independent of the main NAND — this is how "Erase All Content" can
be fast and unrecoverable without physically overwriting gigabytes of flash.
It's addressed by 4-byte tags (`AppleEffaceableStorage__getLocker(tag, buf,
len)`), each holding a small (≤256 byte) blob.

`myscripts/dump_lockers.c` (this project's own tool, built against
`iphone-dataprotection/ramdisk_tools/AppleEffaceableStorage.{c,h}`) enumerates
the tags known from public iOS security research:

```
BAG1  0x42414731   — system keybag wrapping key (this is the one that matters)
EMF!  0x454d4621   — EMF! volume-level encryption key
DYKE  0x44594b45   — (purpose not confirmed)
LWMV  0x4c574d56
FRLE  0x46524c45
SCNT  0x53434e54
LWRN  0x4c57524e
PASS  0x50415353
LOCK  0x4c4f434b
CNTR  0x434e5452   — candidate retry-counter locker (not confirmed accessible, see below)
BLFK  0x424c464b
FUNT  0x46554e54
DFKY  0x44464b59
RETR  0x52455452   — candidate retry-counter locker (not confirmed accessible, see below)
FALS  0x46414c53
CTRR  0x43545252
```

`get_bag1` (from `iphone-dataprotection`) successfully reads `BAG1` and
returns the key+IV that decrypts `systembag.kb`. Reading the other tags
(specifically to find where a hardware/Effaceable-Storage-level retry counter
might live, as opposed to the SpringBoard-plist-level one documented in
[`springboard-patch-attempt.md`](springboard-patch-attempt.md)) turned out to
require **specific code-signing entitlements**: a generic tool signed with the
brute-forcer's entitlements gets `e00002f0` (`kIOReturnNotPermitted`) from
`IOConnectCallMethod` on `AppleEffaceableStorage` selector 5, and re-signing
with `get_bag1`'s own entitlement set (`systembag.kb/entitlements.xml`) instead
got the process killed outright (`Killed: 9`). This avenue was left
unresolved — it's a legitimate follow-up if someone wants to determine whether
a hardware-level retry counter exists independent of the SpringBoard plist.

## The system keybag (`systembag.kb`)

`systembag.kb` is a binary TLV (tag-length-value) structure: an outer `DATA` +
`SIGN` pair, where `DATA` unpacks into a header followed by one entry per
Data Protection class, each carrying:

- `UUID` — the keybag's own UUID
- `CLAS` — the protection class number (`NSFileProtectionComplete`,
  `CompleteUnlessOpen`, `CompleteUntilFirstUserAuthentication`, etc.)
- `WRAP` — the wrapping method (passcode-derived vs UID-only)
- `WPKY` — the wrapped (encrypted) class key itself
- `KTYP` — key type

`patches/systembag.kb-additions/parse_tlv.py` (added in this project) is a
generic dumper for this structure, independent of `systembag.kb`'s own
Kaitai-Struct-generated parser — useful for eyeballing raw TLV fields the
generated parser doesn't expose a friendly accessor for.

Class keys wrapped with `WRAP` type "passcode-derived" are the ones a
brute-force attack targets: for each candidate, the tool derives a key from
the passcode (combined with the UID key in hardware, never in software) and
attempts to AES-unwrap the class key with it. A successful unwrap (checked via
the standard RFC 3394 key-wrap integrity check) means the candidate is the
passcode.

## Why this only works Before First Unlock (BFU) has to stay true

Once a device is unlocked at least once after boot ("After First Unlock",
AFU), iOS keeps Class A/C keys decrypted in kernel memory for the rest of the
session — even after the screen re-locks. If this device had ever been
unlocked since its last reboot, a live memory dump could recover those keys
without needing the passcode at all. This device has always shown the "Enter
Passcode" screen on normal boot, i.e. it has stayed in Before First Unlock
(BFU) state the entire time, which is why no memory-based shortcut was
available — every recovery avenue had to go through the passcode itself.

## What "Erase All" would destroy (and why the dump was made first)

`Erase All Content` does not wipe the NAND — it deletes the Effaceable
Storage keys (`BAG1`/`EMF!` and friends) that everything else is wrapped
under, which makes all NAND ciphertext permanently unrecoverable noise, even
with a full physical NAND image. This is also why re-pairing the device with
a new passcode after an erase can't help recover the old data: erase
generates entirely new UID-derived key material, so there is nothing to
compare the old ciphertext against. This is the reason a full raw dump
(`iphone5_data_enc.img`, the encrypted data partition, plus the decrypted
keybag) was taken **before** any risky operation on the device — it's the
only thing that survives if something goes wrong.
