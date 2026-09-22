# joker

Third-party kernelcache/kext inspection tool, downloaded from
https://newosxbook.com/tools/joker.tar (Jonathan Levin, newosxbook.com — no
formal license file, freely distributed by the author for research use).

Used in this project to locate the offset of the `IOCryptoAcceleratorFamily`
kext inside the decrypted kernelcache, as a prerequisite step for the kernel
patch documented in `kernel_patch/README.md`.

`joker.ELF64` (Linux x86_64) and `joker.universal` (macOS x86_64/arm64) are
vendored here as-is, since they are not part of the `Legacy-IOS-Kit` upstream
repository (this submodule only points at LukeZGD/Legacy-iOS-Kit, so files
that don't belong to that project's own history are kept out of it).

To use: copy the binary matching your platform into `Legacy-IOS-Kit/` (or
anywhere on your `$PATH`) and symlink/rename it to `joker`, e.g.:

```
cp patches/legacy-ios-kit-additions/joker.ELF64 Legacy-IOS-Kit/joker
chmod +x Legacy-IOS-Kit/joker
```

Alternatively, download a fresh copy directly from the source above.
